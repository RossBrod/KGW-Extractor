import os
import shutil

import psycopg2
from psycopg2.extras import DictCursor

from datetime import datetime
import logging


DEEPSEEK_API_KEY =  os.environ.get("DEEPSEEK_API_KEY", "DEEPSEEK-KG_Extractor")  # Added Anthropic API key
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "KG_Extractor")  # Added Anthropic API key
OUTPUT_DIR = "output"



def get_db_connection():
    return psycopg2.connect(
        dbname="KG-Extractor",
        user="postgres1dev",
        password="dev4023TcupSoda",
        host="legawritesql.postgres.database.azure.com",
        port="5432"
    )

def update_case_status_from_folders(output_base, conn):
    cursor = conn.cursor(cursor_factory=DictCursor)

    for folder_name in os.listdir(output_base):
        folder_path = os.path.join(output_base, folder_name)

        if os.path.isdir(folder_path):
            case_id = folder_name  # Assuming folder name is the case_id

            try:
                cursor.execute(
                    "UPDATE cases SET status = %s WHERE case_id = %s",
                    ('queued', case_id)
                )
                print(f"Updated case_id={case_id} to status='queued'")
            except Exception as e:
                print(f"Failed to update case_id={case_id}: {e}")

    conn.commit()
    cursor.close()
    
# Define paths
prod_base = r'C:\__Repo\_LegaWrite\KGW-Extractor\output_LP_fix1\output'
output_base = r'C:\__Repo\_LegaWrite\KGW-Extractor\output'

# conn = get_db_connection()
# update_case_status_from_folders(output_base, conn)
# conn.close()

# Iterate through subfolders in the PROD folder
for folder_name in os.listdir(prod_base):
    prod_folder = os.path.join(prod_base, folder_name)
    output_folder = os.path.join(output_base, folder_name)

    # Only proceed if both are directories and output folder exists
    if os.path.isdir(prod_folder) and os.path.isdir(output_folder):
        for file_name in os.listdir(prod_folder):
            src_file = os.path.join(prod_folder, file_name)
            dest_file = os.path.join(output_folder, file_name)

            if os.path.isfile(src_file):
                shutil.copy2(src_file, dest_file)
                print(f"Copied: {src_file} -> {dest_file}")



