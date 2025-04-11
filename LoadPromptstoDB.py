import os
import re
import psycopg2
from psycopg2.extras import execute_values
import ast
import datetime
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
        logging.FileHandler("neo4j_to_postgres.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("neo4j2postgres")

# Database connection parameters - customize these for your environment

SQL_DB_NAME_AUTH: str = "KG-Extractor"
SQL_DB_USER_AUTH: str = "postgres1dev" if not LOCAL else "postgres"
SQL_DB_PASSWORD_AUTH: str = "dev4023TcupSoda" if not LOCAL else "root"
SQL_DB_HOST_AUTH: str = "legawritesql.postgres.database.azure.com" if not LOCAL else "localhost"
SQL_DB_PORT_AUTH: str = "5432"

PROMPT_DIR = r'C:\_Repo\KGW-Extractor\Prompts'

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
    
PROMPT_DIR = r'C:\_Repo\KGW-Extractor\Prompts'


def create_prompts_table_if_not_exists(conn):
    with conn.cursor() as cur:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS prompts (
                id SERIAL PRIMARY KEY,
                functional_area TEXT UNIQUE,
                system_prompt TEXT,
                extraction_prompt TEXT,
                confirmation_prompt TEXT
            )
        ''')
    conn.commit()
    logger.info("Updated 'prompts' table structure ensured.")

def extract_functional_area_and_type(filename):
    """
    Extracts base functional area and prompt type from filename.
    Expects: S0 CaseCreatePartiesSystem.txt -> ('CaseCreateParties', 'System')
    """
    match = re.match(r"S\d+\s?([A-Za-z]+)(System|Extractor|Assistant)\.txt", filename)
    if match:
        return match.group(1), match.group(2)
    return None, None

def load_prompts_grouped_to_db():
    logger.info("Starting grouped prompt import process...")
    try:
        conn = connect_to_db()
        create_prompts_table_if_not_exists(conn)
        cursor = conn.cursor()

        grouped_prompts = {}

        for filename in os.listdir(PROMPT_DIR):
            if not filename.endswith(".txt"):
                continue

            functional_area, prompt_type = extract_functional_area_and_type(filename)
            if not functional_area or not prompt_type:
                logger.warning(f"Filename skipped (bad format): {filename}")
                continue

            file_path = os.path.join(PROMPT_DIR, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if functional_area not in grouped_prompts:
                grouped_prompts[functional_area] = {"system": None, "extraction": None, "confirmation": None}

            prompt_type_key = {
                "System": "system",
                "Extractor": "extraction",
                "Assistant": "confirmation"
            }.get(prompt_type)

            grouped_prompts[functional_area][prompt_type_key] = content
            logger.info(f"Processed {prompt_type} for {functional_area}")

        for fa, prompts in grouped_prompts.items():
            cursor.execute('''
                INSERT INTO prompts (functional_area, system_prompt, extraction_prompt, confirmation_prompt)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (functional_area) DO UPDATE
                SET system_prompt = EXCLUDED.system_prompt,
                    extraction_prompt = EXCLUDED.extraction_prompt,
                    confirmation_prompt = EXCLUDED.confirmation_prompt
            ''', (fa, prompts["system"], prompts["extraction"], prompts["confirmation"]))
            logger.info(f"Inserted/Updated prompts for: {fa}")

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        logger.error(f"Error during grouped prompt import: {e}")
        
        raise
    logger.info("Grouped prompt import process completed.")

if __name__ == "__main__":
    load_prompts_grouped_to_db()