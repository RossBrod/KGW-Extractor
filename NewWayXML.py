import os
import re
import psycopg2
from psycopg2.extras import execute_values
import ast
#import datetime
from datetime import datetime
import logging
import xml.etree.ElementTree as ET
import json
from typing import Dict, List
from dateutil import parser as date_parser  # Make sure to install with: pip install python-dateutil

LOCAL = False

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/NewWayXML.log", encoding='utf-8'),
        #fh = logging.FileHandler(f'logs/worker_{worker_id}.log', encoding='utf-8')
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("NewWayXML")

# Database connection parameters - customize these for your environment

SQL_DB_NAME_AUTH: str = "CaseGraph2"
SQL_DB_USER_AUTH: str = "postgres1dev" if not LOCAL else "postgres"
SQL_DB_PASSWORD_AUTH: str = "dev4023TcupSoda" if not LOCAL else "root"
SQL_DB_HOST_AUTH: str = "legawritesql.postgres.database.azure.com" if not LOCAL else "localhost"
SQL_DB_PORT_AUTH: str = "5432"


def get_db_connection():
    return psycopg2.connect(
        dbname=SQL_DB_NAME_AUTH,
        user=SQL_DB_USER_AUTH,
        password=SQL_DB_PASSWORD_AUTH,
        host=SQL_DB_HOST_AUTH,
        port=SQL_DB_PORT_AUTH
    )
def connect_to_db():
    """Create and return a connection to the PostgreSQL database."""
    try:
        connection = get_db_connection()
        connection.autocommit = False  # Use transactions for better data integrity
        return connection
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise
def ensure_case_exists(case_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO cases (case_id) VALUES (%s) ON CONFLICT DO NOTHING", (case_id,))
        connection.commit()
    except Exception as e:
        print("✅ case exists ganagsta 🍷")        
    finally:
        cursor.close()
        connection.close()    
def case_exists(case_id, table_name=None):
    """
    Check if a case exists in a specific table or across all relevant tables.
    Args:
        case_id: The case ID to check
        table_name: Optional specific table to check. If None, checks all relevant tables.
    """
    if table_name:
        tables_to_check = [table_name]
    else:
        tables_to_check = [
            "cases",
            "case_summaries",
            "facts",
            "legal_principles",
            "case_rulings",
            "case_issues",
            "case_law_domains",
            "case_causes"
        ]

    try:
        connection = connect_to_db()
        cursor = connection.cursor()

        for table in tables_to_check:
            cursor.execute(f"SELECT 1 FROM {table} WHERE case_id = %s LIMIT 1", (case_id,))
            if cursor.fetchone():
                return True

        return False
    except Exception as e:
        logger.error(f"Error checking if case exists in table(s) for {case_id}: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

########## CasePartyJurispridiction
def extract_tag_content(content, tag_name):
    """Extract content between specified XML tags."""
    match = re.search(f'<{tag_name}>(.*?)</{tag_name}>', content, re.DOTALL)
    return match.group(1).strip() if match else ""
def get_or_create_party(cursor, party_name):
    """Get or create a party record and return its ID."""
    cursor.execute(
        "INSERT INTO parties (name) VALUES (%s) ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name RETURNING party_id",
        (party_name,)
    )
    return cursor.fetchone()[0]
def get_or_create_jurisdiction(cursor, name, level, location, district=None):
    """Get or create a jurisdiction record and return its ID."""
    # If district is provided, append it to the name
    if district:
        full_name = f"{name} - {district}"
    else:
        full_name = name
        
    cursor.execute(
        """
        INSERT INTO jurisdictions (name, level, location) 
        VALUES (%s, %s, %s) 
        ON CONFLICT (name, level, location) DO UPDATE 
        SET name = EXCLUDED.name 
        RETURNING jurisdiction_id
        """,
        (full_name, level, location)
    )
    return cursor.fetchone()[0]
def process_case_create_parties(file_path, case_id):
    """Process a CaseCreateParties XML file and update the database."""
    connection = connect_to_db()
    cursor = connection.cursor()
    
    try:
        # Ensure the case exists in the database
        ensure_case_exists(case_id)
        
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        # Extract case information
        case_element = root.find(".//Case")
        if case_element is None:
            logger.warning(f"No Case element found in {file_path}")
            return
            
        case_name = case_element.get("name", "")
        
        # Update case name if it exists
        if case_name:
            cursor.execute(
                "UPDATE cases SET name = %s WHERE case_id = %s",
                (case_name, case_id)
            )
            logger.info(f"Updated case name for {case_id}: {case_name}")
        
        # Process parties
        parties_element = case_element.find("Parties")
        if parties_element is not None:
            for party_element in parties_element.findall("Party"):
                party_name = party_element.get("name", "")
                party_role = party_element.get("role", "")
                
                if party_name and party_role:
                    # Get or create the party
                    party_id = get_or_create_party(cursor, party_name)
                    
                    # Link the party to the case with the specified role
                    cursor.execute(
                        """
                        INSERT INTO case_parties (case_id, party_id, role)
                        VALUES (%s, %s, %s)
                        ON CONFLICT (case_id, party_id, role) DO NOTHING
                        """,
                        (case_id, party_id, party_role)
                    )
                    logger.info(f"Added party {party_name} as {party_role} to case {case_id}")
        
        # Process jurisdiction
        jurisdiction_element = case_element.find("Jurisdiction")
        if jurisdiction_element is not None:
            jurisdiction_name = jurisdiction_element.get("name", "")
            jurisdiction_level = jurisdiction_element.get("level", "")
            jurisdiction_location = jurisdiction_element.get("location", "")
            jurisdiction_district = jurisdiction_element.get("district", None)
            
            if jurisdiction_name and jurisdiction_level and jurisdiction_location:
                # Get or create the jurisdiction
                jurisdiction_id = get_or_create_jurisdiction(
                    cursor, 
                    jurisdiction_name, 
                    jurisdiction_level, 
                    jurisdiction_location,
                    jurisdiction_district
                )
                
                # Link the jurisdiction to the case
                cursor.execute(
                    """
                    INSERT INTO case_jurisdictions (case_id, jurisdiction_id)
                    VALUES (%s, %s)
                    ON CONFLICT (case_id, jurisdiction_id) DO NOTHING
                    """,
                    (case_id, jurisdiction_id)
                )
                logger.info(f"Added jurisdiction {jurisdiction_name} to case {case_id}")
        
        # Commit the transaction
        connection.commit()
        logger.info(f"Successfully processed case parties for case: {case_id}")
        
    except Exception as e:
        connection.rollback()
        logger.error(f"Error processing case parties for {case_id}: {str(e)}")
        raise
    finally:
        cursor.close()
        connection.close()
def process_case_create_parties_files(root_dir):
    """Process all CaseCreateParties files in the given directory."""
    connection = connect_to_db()
    cursor = connection.cursor()
    
    try:
        folder_count = 0
        success_count = 0
        
        for folder_name in os.listdir(root_dir):
            folder_path = os.path.join(root_dir, folder_name)
            
            # Skip if not a directory
            if not os.path.isdir(folder_path):
                continue
                
            folder_count += 1
            parties_file = os.path.join(folder_path, "CaseCreateParties.XML")
            
            # Skip if parties file doesn't exist
            if not os.path.exists(parties_file):
                logger.warning(f"CaseCreateParties.XML not found in folder: {folder_name}")
                continue
            
            try:
                # Start a transaction
                logger.info(f"Processing case parties for: {folder_name}")
                
                # Process the case parties file
                process_case_create_parties(parties_file, folder_name)
                
                success_count += 1
                logger.info(f"Successfully processed parties for case: {folder_name}")
                
            except Exception as e:
                logger.error(f"Error processing case parties {folder_name}: {str(e)}")
        
        logger.info(f"Processed {folder_count} folders, successfully loaded {success_count} case parties files")
    
    finally:
        print(f"🍸Lets get this Party Started!🍷 at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        cursor.close()
        connection.close()
########## CasePartyJurispridiction
######### case_summary
def process_case_summary_files(root_dir):
    """Process all case summary files in the given directory."""
    connection = connect_to_db()
    cursor = connection.cursor()
    
    try:
        # Get list of all folders in root directory
        folder_count = 0
        success_count = 0
        
        for folder_name in os.listdir(root_dir):
            folder_path = os.path.join(root_dir, folder_name)
            
            # Skip if not a directory
            if not os.path.isdir(folder_path):
                continue
                
            folder_count += 1
            summary_file = os.path.join(folder_path, "Summary.XML")
            
            # Skip if summary file doesn't exist
            if not os.path.exists(summary_file):
                logger.warning(f"Summary.XML not found in folder: {folder_name}")
                continue
            
            try:
                # Start a transaction
                logger.info(f"Processing case summary for: {folder_name}")
                
                # Extract and load the case summary data
                load_case_summary(summary_file, folder_name, cursor)
                
                # Commit the transaction if everything succeeded
                connection.commit()
                success_count += 1
                logger.info(f"Successfully processed summary for case: {folder_name}")
                
            except Exception as e:
                # Rollback the transaction if an error occurred
                connection.rollback()
                logger.error(f"Error processing case summary {folder_name}: {str(e)}")
        
        logger.info(f"Processed {folder_count} folders, successfully loaded {success_count} case summaries")
    
    finally:
        print(r"🐸 summary Loaded at :{}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        cursor.close()
        connection.close()
def parse_case_summary(content):
    """Parse case summary content using regex instead of XML libraries."""
    summary_data = {}
    
    # Extract basic fields
    summary_data['case_name'] = extract_tag_content(content, "Casename")
    summary_data['overview'] = extract_tag_content(content, "Overview")
    summary_data['legal_domain'] = extract_tag_content(content, "LegalDomain")
    summary_data['applicability'] = extract_tag_content(content, "ApplicabilityOfTheCase")
    
    # Extract arguments sections
    both_sides_section = extract_tag_content(content, "BothSidesArgumentsAndReasoning")
    if both_sides_section:
        summary_data['plaintiff_arguments'] = extract_tag_content(both_sides_section, "PlaintiffArguments")
        summary_data['plaintiff_arguments_type'] = extract_tag_content(both_sides_section, "PlaintiffArgumentsType")
        summary_data['defendant_arguments'] = extract_tag_content(both_sides_section, "DefendantArguments")
        summary_data['defendant_arguments_type'] = extract_tag_content(both_sides_section, "DefendantArgumentsType")
    
    # Extract winning party
    findings_section = extract_tag_content(content, "FindingsFavoredParty")
    if findings_section:
        summary_data['winning_party'] = extract_tag_content(findings_section, "WinningParty")
    
    return summary_data
def load_case_summary(file_path, case_id, cursor):
    
    ensure_case_exists(case_id) ### this give flexibility to test potential changes in some of the later XML files without running them sequentialy
        
    """Extract data from a case summary file and load it into PostgreSQL."""
    if case_exists(case_id, "case_summaries"):
        logger.info(f"!!!!!!!!!!!!!!!!!!!!!!!! Case {case_id} already exists. Skipping creation!!!!!!!!!!!!!!!!!!!!!!")
        return        
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extract content between CaseSummary tags
        summary_match = re.search(r'<CaseSummary>(.*?)</CaseSummary>', content, re.DOTALL)
        if not summary_match:
            logger.warning(f"No CaseSummary content found in {file_path}")
            return

        summary_data = parse_case_summary(summary_match.group(1))
        
        # Insert the case summary
        insert_case_summary(cursor, case_id, summary_data)
            
    except Exception as e:
        logger.error(f"Error in load_case_summary for {file_path}: {str(e)}")
        raise
def insert_case_summary(cursor, case_id, summary_data):
    """Insert a case summary into the case_summaries table."""
    query = """
        INSERT INTO case_summaries (
            case_id, case_name, overview, legal_domain, 
            plaintiff_arguments, plaintiff_arguments_type,
            defendant_arguments, defendant_arguments_type,
            applicability, winning_party
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (case_id) DO UPDATE SET
            case_name = EXCLUDED.case_name,
            overview = EXCLUDED.overview,
            legal_domain = EXCLUDED.legal_domain,
            plaintiff_arguments = EXCLUDED.plaintiff_arguments,
            plaintiff_arguments_type = EXCLUDED.plaintiff_arguments_type,
            defendant_arguments = EXCLUDED.defendant_arguments,
            defendant_arguments_type = EXCLUDED.defendant_arguments_type,
            applicability = EXCLUDED.applicability,
            winning_party = EXCLUDED.winning_party
        RETURNING summary_id
    """
    
    cursor.execute(query, (
        case_id,
        summary_data.get('case_name', ''),
        summary_data.get('overview', ''),
        summary_data.get('legal_domain', ''),
        summary_data.get('plaintiff_arguments', ''),
        summary_data.get('plaintiff_arguments_type', ''),
        summary_data.get('defendant_arguments', ''),
        summary_data.get('defendant_arguments_type', ''),
        summary_data.get('applicability', ''),
        summary_data.get('winning_party', '')
    ))
    
    return cursor.fetchone()[0]
######### /case_summary   
########## taxonomy
def process_taxonomy_folder(root_dir):
    """Process all taxonomy files (LawDomain.XML) in the given directory."""
    connection = connect_to_db()
    cursor = connection.cursor()
    
    try:
        # Get list of all folders in root directory
        folder_count = 0
        success_count = 0
        
        for folder_name in os.listdir(root_dir):
            folder_path = os.path.join(root_dir, folder_name)
            
            # Skip if not a directory
            if not os.path.isdir(folder_path):
                continue
                
            folder_count += 1
            taxonomy_file = os.path.join(folder_path, "LawDomain.XML")
            
            # Skip if taxonomy file doesn't exist
            if not os.path.exists(taxonomy_file):
                logger.warning(f"LawDomain.XML not found in folder: {folder_name}")
                continue
            
            try:
                # Start a transaction
                logger.info(f"Processing taxonomy for case: {folder_name}")
                
                # Extract and load the taxonomy data
                load_taxonomy_data(taxonomy_file, folder_name, cursor)
                
                # Commit the transaction if everything succeeded
                connection.commit()
                success_count += 1
                logger.info(f"Successfully processed taxonomy for case: {folder_name}")
                
            except Exception as e:
                # Rollback the transaction if an error occurred
                connection.rollback()
                logger.error(f"Error processing taxonomy for case {folder_name}: {str(e)}")
        
        logger.info(f"Processed {folder_count} folders, successfully loaded {success_count} taxonomies")
    
    finally:
        print(f"🧬 taxonomy saved at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        cursor.close()
        connection.close()
def extract_taxonomy_section(content, section_name):
    """Extract a specific taxonomy section using regex."""
    pattern = f"<{section_name}>(.*?)</{section_name}>"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None
def parse_taxonomy_relationships(section_text):
    """Parse taxonomy relationships from text into structured data."""
    if not section_text:
        return []
    
    relationships = []
    
    # Split by lines and process each relationship
    lines = section_text.strip().split('\n')
    for line in lines:
        # Remove any brackets and extra whitespace
        line = line.strip()
        if not line:
            continue
            
        # Parse relationship path like [A] -> [B] -> [C]
        elements = re.findall(r'\[(.*?)\]', line)
        
        if len(elements) >= 2:
            # Handle different formats (2 or 3 elements)
            if len(elements) >= 3:
                # 3 elements: broad -> subdomain -> specific
                broad, subdomain, specific = elements[0], elements[1], elements[2]
            else:
                # 2 elements: null broad, subdomain -> specific
                broad, subdomain, specific = None, elements[0], elements[1]
                
            relationships.append({
                'broad': broad,
                'subdomain': subdomain,
                'specific': specific
            })
    
    return relationships
def load_taxonomy_data(file_path, case_id, cursor):
    """Extract taxonomy data from a file and load it into PostgreSQL."""
    if case_exists(case_id, "case_law_domains"):
        logger.info(f"Case {case_id} already exists. Skipping creation.")
        return    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extract each taxonomy section
        sections = {
            'LawDomain': extract_taxonomy_section(content, 'LawDomain'),
            'LegalIssues': extract_taxonomy_section(content, 'LegalIssues'),
            'LegalSubcategories': extract_taxonomy_section(content, 'LegalSubcategories'),
            'LegalConcepts': extract_taxonomy_section(content, 'LegalConcepts')
        }
        
        # Process each section
        all_relationships = []
        
        # LawDomain is required
        if not sections['LawDomain']:
            logger.warning(f"No LawDomain content found in {file_path}")
            return
            
        all_relationships.extend(parse_taxonomy_relationships(sections['LawDomain']))
        
        # Process optional sections
        for section_name in ['LegalIssues', 'LegalSubcategories', 'LegalConcepts']:
            if sections[section_name]:
                all_relationships.extend(parse_taxonomy_relationships(sections[section_name]))
        
        # Insert all relationships and link to case
        for relationship in all_relationships:
            domain_id = insert_law_domain(cursor, relationship['broad'], relationship['subdomain'], relationship['specific'])
            link_case_to_domain(cursor, case_id, domain_id)
            
    except Exception as e:
        logger.error(f"Error in load_taxonomy_data for {file_path}: {str(e)}")
        raise
def insert_law_domain(cursor, broad, subdomain, specific):
    """Insert a law domain and return its ID."""
    query = """
        INSERT INTO law_domains (broad, subdomain, specific)
        VALUES (%s, %s, %s)
        ON CONFLICT (broad, subdomain, specific) DO UPDATE SET
            broad = EXCLUDED.broad
        RETURNING domain_id
    """
    
    cursor.execute(query, (
        broad,  # Could be None for 2-element relationships
        subdomain,
        specific
    ))
    
    return cursor.fetchone()[0]
def link_case_to_domain(cursor, case_id, domain_id):
    """Create a relationship between a case and a law domain."""
    query = """
        INSERT INTO case_law_domains (case_id, domain_id)
        VALUES (%s, %s)
        ON CONFLICT (case_id, domain_id) DO NOTHING
    """
    
    cursor.execute(query, (case_id, domain_id))
########## /taxonomy
########## LegalPrinciples
def process_LegalPrinciples(root_dir):
        """Process all legal principles files in the given directory."""
        connection = connect_to_db()
        cursor = connection.cursor()
        
        try:
            # Get list of all folders in root directory
            folder_count = 0
            success_count = 0
            
            for folder_name in os.listdir(root_dir):
                folder_path = os.path.join(root_dir, folder_name)
                
                # Skip if not a directory
                if not os.path.isdir(folder_path):
                    continue
                    
                folder_count += 1
                principles_file = os.path.join(folder_path, "LegalPrinciples.XML")
                
                # Skip if principles file doesn't exist
                if not os.path.exists(principles_file):
                    logger.warning(f"LegalPrinciples.XML not found in folder: {folder_name}")
                    continue
                
                try:
                    # Start a transaction
                    logger.info(f"Processing legal principles for case: {folder_name}")
                    
                    # Extract and load the legal principles data
                    load_legal_principles(principles_file, folder_name, cursor)
                    
                    # Commit the transaction if everything succeeded
                    connection.commit()
                    success_count += 1
                    logger.info(f"Successfully processed legal principles for case: {folder_name}")
                    
                except Exception as e:
                    # Rollback the transaction if an error occurred
                    connection.rollback()
                    logger.error(f"Error processing legal principles for case {folder_name}: {str(e)}")
            
            logger.info(f"Processed {folder_count} folders, successfully loaded {success_count} legal principles sets")
        
        finally:
            print(f"📚⚖️🧠  LegalPrinciples perserved at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            cursor.close()
            connection.close()

def extract_legal_principles(content): 
        """Extract legal principles from the CaseElements section using regex."""
        principles = []
        
        # First extract the CaseElements section
        case_elements_match = re.search(r'<CaseElements>(.*?)</CaseElements>', content, re.DOTALL)
        if not case_elements_match:
            return principles
        
        case_elements_content = case_elements_match.group(1)
        
        # Find all cLPX sections
        clp_pattern = re.compile(r'<cLP\d+>(.*?)</cLP\d+>', re.DOTALL)
        clp_matches = clp_pattern.findall(case_elements_content)
        
        for clp_content in clp_matches:
            principle = {}
            
            # Extract each field
            name_match = re.search(r'<Name>(.*?)</Name>', clp_content, re.DOTALL)
            if name_match:
                principle['name'] = name_match.group(1).strip()
            
            type_match = re.search(r'<Type>(.*?)</Type>', clp_content, re.DOTALL)
            if type_match:
                principle['type'] = type_match.group(1).strip()
            
            doctrine_match = re.search(r'<DoctrinePrinciple>(.*?)</DoctrinePrinciple>', clp_content, re.DOTALL)
            if doctrine_match:
                principle['DoctrinePrinciple'] = doctrine_match.group(1).strip()
            
            description_match = re.search(r'<Description>(.*?)</Description>', clp_content, re.DOTALL)
            if description_match:
                principle['description'] = description_match.group(1).strip()
            
            relationship_match = re.search(r'<Relationship>(.*?)</Relationship>', clp_content, re.DOTALL)
            if relationship_match:
                principle['relationship'] = relationship_match.group(1).strip()
            
            principles.append(principle)
    
        return principles

def load_legal_principles(file_path, case_id, cursor):
    """Extract legal principles from a file and load them into PostgreSQL."""
    if case_exists(case_id, "legal_principles"):
        logger.info(f"<<<<<<<<<<<<<<<<<<<<<<Case {case_id} already exists. Skipping creation.>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>********************************************************************************************")
        return    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extract the legal principles
        principles = extract_legal_principles(content)
        
        if not principles:
            logger.warning(f"No legal principles found in {file_path}")
            return
        
        # Insert each principle
        for principle in principles:
            insert_legal_principle(cursor, case_id, principle)
            
    except Exception as e:
        logger.error(f"Error in load_legal_principles for {file_path}: {str(e)}")
        raise
def insert_legal_principle(cursor, case_id, principle):    
    """Insert a legal principle into the legal_principles table."""
    query = """
        INSERT INTO legal_principles (
            case_id, name, type, "DoctrinePrinciple", description, relationship_type
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (case_id, name) DO UPDATE SET
            type = EXCLUDED.type,
            "DoctrinePrinciple" = EXCLUDED."DoctrinePrinciple",
            description = EXCLUDED.description,
            relationship_type = EXCLUDED.relationship_type
        RETURNING principle_id
    """
    
    try:
        cursor.execute(query, (
            case_id,
            principle.get('name', ''),
            principle.get('type', ''),
            principle.get('DoctrinePrinciple', ''),
            principle.get('description', ''),
            principle.get('relationship', '')
        ))
    except psycopg2.Error as e:
        # If the conflict clause has an issue (perhaps case_id, name is not a unique constraint),
        # fall back to a simpler insert
        logger.warning(f"Failed with ON CONFLICT clause, using simple insert: {str(e)}")
        
        # Alternative query without conflict handling
        query = """
            INSERT INTO legal_principles (
                case_id, name, type, "DoctrinePrinciple", description, relationship_type
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING principle_id
        """
        cursor.execute(query, (
            case_id,
            principle.get('name', ''),
            principle.get('type', ''),
            principle.get('DoctrinePrinciple', ''),
            principle.get('description', ''),
            principle.get('relationship', '')
        ))
    return cursor.fetchone()[0]


########## /LegalPrinciples
########## FACTS
def process_Facts(root_dir):
    """Process all FactualBackgrounds.XML files in the given directory."""
    connection = connect_to_db()
    cursor = connection.cursor()
    
    try:
        # Get list of all folders in root directory
        folder_count = 0
        success_count = 0
        
        for folder_name in os.listdir(root_dir):
            folder_path = os.path.join(root_dir, folder_name)
            
            # Skip if not a directory
            if not os.path.isdir(folder_path):
                continue
                
            folder_count += 1
            facts_file = os.path.join(folder_path, "Fact.XML")
            
            # Skip if facts file doesn't exist
            if not os.path.exists(facts_file):
                logger.warning(f"FactualBackgrounds.XML not found in folder: {folder_name}")
                continue
            
            try:
                # Start a transaction
                logger.info(f"Processing facts for case: {folder_name}")
                
                # Extract and load the facts data
                load_facts_data(facts_file, folder_name, cursor)
                
                # Commit the transaction if everything succeeded
                connection.commit()
                success_count += 1
                logger.info(f"Successfully processed facts for case: {folder_name}")
                
            except Exception as e:
                # Rollback the transaction if an error occurred
                connection.rollback()
                logger.error(f"Error processing facts for case {folder_name}: {str(e)}")
        
        logger.info(f"Processed {folder_count} folders, successfully loaded facts for {success_count} cases")
    
    finally:
        print(f"🗣️💯 FACTS done stating at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        cursor.close()
        connection.close()
def load_facts_data(file_path, case_id, cursor):
    """Extract facts data from a file and load it into PostgreSQL."""
    if case_exists(case_id, "facts"):
        logger.info(f"Case {case_id} already exists. Skipping creation.")
        return
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extract content between FactualBackgrounds tags
        facts_match = re.search(r'<FactualBackgrounds>(.*?)</FactualBackgrounds>', content, re.DOTALL)
        if not facts_match:
            logger.warning(f"No FactualBackgrounds content found in {file_path}")
            return

        facts_content = facts_match.group(1)
        
        # Extract each fact section
        fact_sections = re.findall(r'<fact>(.*?)</fact>', facts_content, re.DOTALL)
        
        if not fact_sections:
            logger.warning(f"No fact sections found in {file_path}")
            return
        
        # Process each fact
        for fact_section in fact_sections:
            fact_data = parse_fact_section(fact_section)
            insert_fact(cursor, case_id, fact_data)
            
    except Exception as e:
        logger.error(f"Error in load_facts_data for {file_path}: {str(e)}")
        raise
def parse_fact_section(section_text):
    """Parse a fact section into a dictionary of fact attributes."""
    fact_data = {}
    
    # Extract each field using regex
    type_match = re.search(r'<Type>(.*?)</Type>', section_text, re.DOTALL)
    if type_match:
        fact_data['type'] = type_match.group(1).strip()
    
    name_match = re.search(r'<Name>(.*?)</Name>', section_text, re.DOTALL)
    if name_match:
        fact_data['name'] = name_match.group(1).strip()
    
    description_match = re.search(r'<Description>(.*?)</Description>', section_text, re.DOTALL)
    if description_match:
        fact_data['description'] = description_match.group(1).strip()
    
    concept_match = re.search(r'<Concept>(.*?)</Concept>', section_text, re.DOTALL)
    if concept_match:
        fact_data['concept'] = concept_match.group(1).strip()
    
    symbol_match = re.search(r'<Symbol>(.*?)</Symbol>', section_text, re.DOTALL)
    if symbol_match:
        fact_data['symbol'] = symbol_match.group(1).strip()
    
    relationship_match = re.search(r'<Relationship>(.*?)</Relationship>', section_text, re.DOTALL)
    if relationship_match:
        fact_data['relationship_type'] = relationship_match.group(1).strip()
    
    return fact_data
def insert_fact(cursor, case_id, fact_data):
    """Insert a fact into the facts table."""
    query = """
        INSERT INTO facts (
            case_id, type, name, concept, symbol, description, relationship_type
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (case_id, type, name) DO UPDATE SET
            concept = EXCLUDED.concept,
            symbol = EXCLUDED.symbol,
            description = EXCLUDED.description,
            relationship_type = EXCLUDED.relationship_type
        RETURNING fact_id
    """
    
    # Note: The ON CONFLICT assumes there's a unique constraint on (case_id, type, name)
    # If that's not the case, you might need to modify this logic
    
    try:
        cursor.execute(query, (
            case_id,
            fact_data.get('type', ''),
            fact_data.get('name', ''),
            fact_data.get('concept', ''),
            fact_data.get('symbol', ''),
            fact_data.get('description', ''),
            fact_data.get('relationship_type', '')
        ))
        
        return cursor.fetchone()[0]
    except psycopg2.Error as e:
        # If the error is related to the ON CONFLICT constraint, try a different approach
        if "there is no unique or exclusion constraint" in str(e):
            # Alternative approach: Check if record exists first
            logger.warning(f"No unique constraint found for facts table. Using alternative approach.")
            
            check_query = """
                SELECT fact_id FROM facts 
                WHERE case_id = %s AND type = %s AND name = %s
            """
            
            cursor.execute(check_query, (
                case_id,
                fact_data.get('type', ''),
                fact_data.get('name', '')
            ))
            
            result = cursor.fetchone()
            
            if result:
                # Record exists, update it
                update_query = """
                    UPDATE facts
                    SET concept = %s, symbol = %s, description = %s, relationship_type = %s
                    WHERE fact_id = %s
                    RETURNING fact_id
                """
                
                cursor.execute(update_query, (
                    fact_data.get('concept', ''),
                    fact_data.get('symbol', ''),
                    fact_data.get('description', ''),
                    fact_data.get('relationship_type', ''),
                    result[0]
                ))
                
                return result[0]
            else:
                # Record doesn't exist, insert it
                insert_query = """
                    INSERT INTO facts (
                        case_id, type, name, concept, symbol, description, relationship_type
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING fact_id
                """
                
                cursor.execute(insert_query, (
                    case_id,
                    fact_data.get('type', ''),
                    fact_data.get('name', ''),
                    fact_data.get('concept', ''),
                    fact_data.get('symbol', ''),
                    fact_data.get('description', ''),
                    fact_data.get('relationship_type', '')
                ))
                
                return cursor.fetchone()[0]
        else:
            # If it's a different error, re-raise it
            raise
########## /FACTS
########## /additionalinfo_folder
def get_additional_info(case_id, root_dir):
    folder_path = os.path.join(root_dir, case_id)
    file_path = os.path.join(folder_path, "additional_info.json")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        court = data.get("court", "") or ""
        citation = data.get("citation", "") or ""
        date_published_raw = data.get("datePublished", "") or ""
        date_published = ""

        if date_published_raw:
            try:
                parsed_date = date_parser.parse(date_published_raw)
                date_published = parsed_date.date().isoformat()
            except Exception as e:
                print(f"[WARN] Could not parse datePublished '{date_published_raw}' for {case_id}: {e}")
        return court, date_published, citation
    except FileNotFoundError:
        print(f"[INFO] File not found for {case_id}: {file_path}")
        return "", "", ""
    except json.JSONDecodeError:
        print(f"[ERROR] Invalid JSON in file: {file_path}")
        return "", "", ""
    except Exception as e:
        print(f"[ERROR] Unexpected error reading {file_path}: {str(e)}")
        return "", "", ""
def save_courtinfo(case_id, court, date_published, citation):
    query = """
        UPDATE cases 
        SET court = %s,
            date_published = %s,
            citation = %s
        WHERE case_id = %s
    """
    connection = None
    cursor = None
    try:
        # Convert empty string to None for proper SQL NULL insertion
        citation_value = citation if citation else None

        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute(query, (court, date_published, citation_value, case_id))
        connection.commit()
    except Exception as e:
        print(f"[ERROR] Failed to update court info for case {case_id}: {e}")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
def process_additionalinfo_folder(root_dir):
    for folder_name in os.listdir(root_dir):
        print("AdditionalInfo starting: " + folder_name)
        court, date_published, citation = get_additional_info(folder_name, root_dir)
        save_courtinfo(folder_name, court, date_published,citation)
        print(f"📎✨ {folder_name} AdditionalInfo finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
########## /additionalinfo_folder
######### RULING
def process_Ruling(root_dir):
    """Process all Ruling.XML files in the given directory structure."""
    connection = connect_to_db()
    cursor = connection.cursor()
    
    try:
        # Get list of all folders in root directory
        folder_count = 0
        success_count = 0
        
        for folder_name in os.listdir(root_dir):
            folder_name="abbott-v-crown-motor-co-inc"
            folder_path = os.path.join(root_dir, folder_name)
            
            # Skip if not a directory
            if not os.path.isdir(folder_path):
                continue
                
            folder_count += 1
            ruling_file = os.path.join(folder_path, "Ruling.XML")
            
            # Skip if ruling file doesn't exist
            if not os.path.exists(ruling_file):
                logger.warning(f"Ruling.XML not found in folder: {folder_name}")
                continue
            
            try:
                # Start a transaction
                logger.info(f"Processing ruling for case: {folder_name}")
                
                # Extract and load the ruling data
                load_ruling_data(ruling_file, folder_name, connection)
                
                # Commit the transaction if everything succeeded
                connection.commit()
                success_count += 1
                logger.info(f"Successfully processed ruling for case: {folder_name}")
                
            except Exception as e:
                # Rollback the transaction if an error occurred
                connection.rollback()
                logger.error(f"Error processing ruling for case {folder_name}: {str(e)}")
        
        logger.info(f"Processed {folder_count} folders, successfully loaded {success_count} rulings")
    
    finally:
        print(f"📢🔨 Ruling finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        cursor.close()
        connection.close()
def extract_ruling_section(content, section_name):
    """Extract a specific ruling section using regex."""
    pattern = f"<{section_name}>(.*?)</{section_name}>"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None
def extract_issues(issues_section):
    """Extract individual issues from the IssuesList section."""
    issues = []
    if not issues_section:
        return issues
    
    # Use regex to find all issue elements (issue1, issue2, etc.)
    issue_pattern = r"<issue\d+>(.*?)</issue\d+>"
    matches = re.findall(issue_pattern, issues_section, re.DOTALL)
    
    for match in matches:
        issues.append(match.strip())
    
    return issues
def load_ruling_data(file_path, case_id, connection):
    """Extract ruling data from a file and load it into PostgreSQL."""
    if case_exists(case_id, "case_rulings"):
        logger.info(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>Case {case_id} already exists. Skipping creation.<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        return
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extract the Ruling section
        ruling_match = re.search(r'<Ruling>(.*?)</Ruling>', content, re.DOTALL)
        if not ruling_match:
            logger.warning(f"No Ruling content found in {file_path}")
            return
        
        ruling_content = ruling_match.group(1)
        
        # Extract IssuesList and Holding sections
        issues_section = extract_ruling_section(ruling_content, 'IssuesList')
        holding_section = extract_ruling_section(ruling_content, 'Holding')
        
        # Process issues
        issues = extract_issues(issues_section)
        for idx, issue_text in enumerate(issues, 1):
            insert_case_issue(connection, case_id, issue_text, idx)
        
        # Process legal principles (holdings)
        principles = extract_LP_ruling(holding_section)
        for idx, principle_text in enumerate(principles, 1):
            insert_case_ruling(connection, case_id, principle_text, idx)
            
    except Exception as e:
        logger.error(f"Error in load_ruling_data for {file_path}: {str(e)}")
        raise
def insert_case_issue(connection, case_id, issue_text, issue_number):
    """Insert or update a case issue into the case_issues table."""
    query = """
        INSERT INTO case_issues (case_id, issue_text, issue_number)
        VALUES (%s, %s, %s)
        ON CONFLICT (case_id, issue_number) DO UPDATE SET
            issue_text = EXCLUDED.issue_text
        RETURNING issue_id
    """
    with connection.cursor() as cur:
        cur.execute(query, (case_id, issue_text, issue_number))
        return cur.fetchone()[0]
def insert_case_ruling(connection, case_id, principle_text, principle_number):
    with connection.cursor() as cur:
        cur.execute("""
            INSERT INTO case_rulings (case_id, legal_principle_text, principle_number)
            VALUES (%s, %s, %s)
            ON CONFLICT (case_id, principle_number) DO UPDATE
                SET legal_principle_text = EXCLUDED.legal_principle_text
            RETURNING ruling_id
        """, (case_id, principle_text["text"], principle_number))
        return cur.fetchone()[0]
def extract_LP_ruling(content):
    """Extract legal principles from content using regex."""
    principles = []
    
    # Find all LP tags with numbers (e.g., LP1, LP2, etc.)
    lp_pattern = re.compile(r'<LP(\d+)>(.*?)</LP\1>', re.DOTALL)
    lp_matches = lp_pattern.findall(content)
    
    for lp_number, lp_content in lp_matches:
        principle = {
            'number': int(lp_number),
            'text': lp_content.strip()
        }
        principles.append(principle)
   
    return principles

######### /RULING
######## CauseOfAction
def process_CausesOfAction(root_dir):
    """Process all CausesOfAction.XML files in the given directory."""
    connection = connect_to_db()
    cursor = connection.cursor()
    
    try:
        # Get list of all folders in root directory
        folder_count = 0
        success_count = 0
        
        for folder_name in os.listdir(root_dir):
            folder_path = os.path.join(root_dir, folder_name)
            
            # Skip if not a directory
            if not os.path.isdir(folder_path):
                continue
                
            folder_count += 1
            causes_file = os.path.join(folder_path, "CausesOfAction.XML")
            
            # Skip if causes of action file doesn't exist
            if not os.path.exists(causes_file):
                logger.warning(f"CausesOfAction.XML not found in folder: {folder_name}")
                continue
            
            try:
                # Start a transaction
                logger.info(f"Processing causes of action for case: {folder_name}")
                
                # Extract and load the causes of action data
                load_causes_of_action(causes_file, folder_name, cursor)
                
                # Commit the transaction if everything succeeded
                connection.commit()
                success_count += 1
                logger.info(f"Successfully processed causes of action for case: {folder_name}")
                
            except Exception as e:
                # Rollback the transaction if an error occurred
                connection.rollback()
                logger.error(f"Error processing causes of action for case {folder_name}: {str(e)}")
        
        logger.info(f"Processed {folder_count} folders, successfully loaded {success_count} causes of action sets")
    
    finally:
        print(f"🚨📄  Finished COA at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        cursor.close()
        connection.close()
def extract_cause_of_action(content, index):
    """Extract a specific cause of action section using regex."""
    pattern = f"<cause_of_action{index}>(.*?)</cause_of_action{index}>"
    match = re.search(pattern, content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None
def extract_field_from_cause(cause_text, field_name):
    """Extract a specific field from a cause of action text."""
    pattern = f"<{field_name}>(.*?)</{field_name}>"
    match = re.search(pattern, cause_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None
def extract_legal_basis(cause_text):
    """Extract legal basis section from a cause of action text."""
    pattern = r"<LegalBasis>(.*?)</LegalBasis>"
    match = re.search(pattern, cause_text, re.DOTALL)
    if match:
        legal_basis = match.group(1).strip()
        return {
            'name': extract_field_from_cause(legal_basis, 'name'),
            'type': extract_field_from_cause(legal_basis, 'type'),
            'description': extract_field_from_cause(legal_basis, 'description')
        }
    return None
def load_causes_of_action(file_path, case_id, cursor):
    """Extract causes of action data from a file and load it into PostgreSQL."""
    if case_exists(case_id, "case_causes"):
        logger.info(f"Case {case_id} already exists. Skipping creation.")
        return    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extract the entire causes_of_action section
        causes_section_match = re.search(r'<causes_of_action>(.*?)</causes_of_action>', content, re.DOTALL)
        if not causes_section_match:
            logger.warning(f"No causes_of_action content found in {file_path}")
            return
            
        causes_section = causes_section_match.group(1)
        
        # Find all cause of action entries (flexible approach to handle any number)
        index = 1
        causes_processed = 0
        
        while True:
            cause_text = extract_cause_of_action(causes_section, index)
            if not cause_text:
                break
                
            # Extract fields for this cause of action
            cause_data = {
                'name': extract_field_from_cause(cause_text, 'name'),
                'type': extract_field_from_cause(cause_text, 'type'),
                'description': extract_field_from_cause(cause_text, 'description'),
                'legal_basis': extract_legal_basis(cause_text)
            }
            
            # Insert the cause of action
            if cause_data['name']:
                cause_id = insert_cause_of_action(cursor, cause_data)
                
                # Link to the case
                link_cause_to_case(cursor, case_id, cause_id)
                
                # If legal basis exists, insert and link it
                if cause_data['legal_basis'] and cause_data['legal_basis']['name']:
                    legal_basis_id = insert_legal_basis(cursor, cause_data['legal_basis'])
                    link_cause_to_legal_basis(cursor, cause_id, legal_basis_id)
                
                causes_processed += 1
            
            index += 1
        
        logger.info(f"Processed {causes_processed} causes of action for case {case_id}")
            
    except Exception as e:
        logger.error(f"Error in load_causes_of_action for {file_path}: {str(e)}")
        raise
def insert_cause_of_action(cursor, cause_data):
    """Insert a cause of action and return its ID."""
    query = """
        INSERT INTO causes_of_action (name, type, description)
        VALUES (%s, %s, %s)
        ON CONFLICT (name, type) DO UPDATE SET
            description = EXCLUDED.description
        RETURNING cause_id
    """
    
    cursor.execute(query, (
        cause_data['name'],
        cause_data['type'],
        cause_data['description']
    ))
    
    return cursor.fetchone()[0]
def insert_legal_basis(cursor, legal_basis_data):
    """Insert a legal basis and return its ID."""
    query = """
        INSERT INTO legal_bases (name, type, description)
        VALUES (%s, %s, %s)
        ON CONFLICT (name, type) DO UPDATE SET
            description = EXCLUDED.description
        RETURNING basis_id
    """
    
    cursor.execute(query, (
        legal_basis_data['name'],
        legal_basis_data['type'],
        legal_basis_data['description']
    ))
    
    return cursor.fetchone()[0]
def link_cause_to_case(cursor, case_id, cause_id):
    """Create a relationship between a case and a cause of action."""
    query = """
        INSERT INTO case_causes (case_id, cause_id)
        VALUES (%s, %s)
        ON CONFLICT (case_id, cause_id) DO NOTHING
    """
    
    cursor.execute(query, (case_id, cause_id))
def link_cause_to_legal_basis(cursor, cause_id, legal_basis_id):
    """Create a relationship between a cause of action and its legal basis."""
    query = """
        INSERT INTO cause_legal_bases (cause_id, basis_id)
        VALUES (%s, %s)
        ON CONFLICT (cause_id, basis_id) DO NOTHING
    """
    
    cursor.execute(query, (cause_id, legal_basis_id))

    query = "SELECT 1 FROM cases WHERE case_id = %s"
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute(query, (case_id,))
        return cursor.fetchone() is not None
    except Exception as e:
        logger.error(f"Error checking if case exists in 'cases' for {case_id}: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

######## CauseOfAction
def main():
    """Main function to run the script."""
    try:
        # Replace with your actual directory path
        root_directory = "C:\\__Repo\\_LegaWrite\\KGW-Extractor\\output"
        # process_case_create_parties_files(root_directory)
        # process_case_summary_files(root_directory)
        # process_taxonomy_folder(root_directory)
        process_LegalPrinciples(root_directory)
        # process_Facts(root_directory)
        # root_directory = "C:\\__Repo\\AdditionalInfo"
        # process_additionalinfo_folder(root_directory) 
        root_directory = "C:\\__Repo\\_LegaWrite\\KGW-Extractor\\output"
        #process_Ruling(root_directory)
        #process_CausesOfAction(root_directory)
        
        logger.info("🏁 Processing completed successfully🏁")
    except Exception as e:
        logger.error(f"An error occurred in main: {str(e)}")

if __name__ == "__main__":
    main()
    