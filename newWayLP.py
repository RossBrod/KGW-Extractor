import os
import re
import psycopg2
from psycopg2.extras import execute_values
import ast
from datetime import datetime
import logging
import xml.etree.ElementTree as ET
import json
from typing import Dict, List
from dateutil import parser as date_parser  # Make sure to install with: pip install python-dateutil

LOCAL = False

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

SQL_DB_NAME_AUTH: str = "CaseGraph2"
SQL_DB_USER_AUTH: str = "postgres1dev" if not LOCAL else "postgres"
SQL_DB_PASSWORD_AUTH: str = "dev4023TcupSoda" if not LOCAL else "root"
SQL_DB_HOST_AUTH: str = "legawritesql.postgres.database.azure.com" if not LOCAL else "localhost"
SQL_DB_PORT_AUTH: str = "5432"

class LegalPrinciples:
    SQL_DB_NAME_AUTH: str = "CaseGraph2"
    SQL_DB_USER_AUTH: str = "postgres1dev"
    SQL_DB_PASSWORD_AUTH: str = "dev4023TcupSoda"
    SQL_DB_HOST_AUTH: str = "legawritesql.postgres.database.azure.com"
    SQL_DB_PORT_AUTH: str = "5432"
    LOCAL = False    

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

    
def get_db_connection(self):
        return psycopg2.connect(
            dbname=self.SQL_DB_NAME_AUTH,
            user=self.SQL_DB_USER_AUTH,
            password=self.SQL_DB_PASSWORD_AUTH,
            host=self.SQL_DB_HOST_AUTH,
            port=self.SQL_DB_PORT_AUTH
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
        clp_pattern = re.compile(r'<LP\d+>(.*?)</LP\d+>', re.DOTALL)
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
            case_id, name, type, doctrineprinciple, description, relationship_type
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (case_id, name) DO UPDATE SET
            type = EXCLUDED.type,
            doctrineprinciple = EXCLUDED.doctrineprinciple,
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
                case_id, name, type, doctrineprinciple, description, relationship_type
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