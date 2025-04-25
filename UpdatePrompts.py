import os
import re
import psycopg2
from psycopg2 import sql
#from flask import flash
# Import any additional necessary libraries based on your project's structure

def get_db_connection():
    return psycopg2.connect(
        dbname="KG-Extractor",
        user="postgres1dev",
        password="dev4023TcupSoda",
        host="legawritesql.postgres.database.azure.com",
        port="5432"
    )

def update_prompts_from_files():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get all functional areas from the database
    cursor.execute("SELECT functional_area FROM prompts")
    functional_areas = [row[0] for row in cursor.fetchall()]
    
    prompts_dir = "Prompts"  # Update with actual path
    updated_count = 0
    errors = []
    
    for area in functional_areas:
        try:
            # Look for system prompt file
            system_prompt_pattern = re.compile(f"S\\d+\\s+{area}(Assistant)?\\.txt$", re.IGNORECASE)
            # Look for extraction prompt file
            extraction_prompt_pattern = re.compile(f"S\\d+\\s+{area}Extractor\\.txt$", re.IGNORECASE)
            # Look for confirmation prompt file
            confirmation_prompt_pattern = re.compile(f"S\\d+\\s+{area}Confirmation\\.txt$", re.IGNORECASE)
            
            system_prompt_file = None
            extraction_prompt_file = None
            confirmation_prompt_file = None
            
            # Find the matching files
            for filename in os.listdir(prompts_dir):
                if system_prompt_pattern.match(filename):
                    system_prompt_file = os.path.join(prompts_dir, filename)
                elif extraction_prompt_pattern.match(filename):
                    extraction_prompt_file = os.path.join(prompts_dir, filename)
                elif confirmation_prompt_pattern.match(filename):
                    confirmation_prompt_file = os.path.join(prompts_dir, filename)
            
            # Build SQL update statement based on which files were found
            update_fields = []
            update_values = []
            
            if system_prompt_file and os.path.isfile(system_prompt_file):
                with open(system_prompt_file, 'r', encoding='utf-8') as f:
                    update_fields.append("system_prompt")
                    update_values.append(f.read())
            
            if extraction_prompt_file and os.path.isfile(extraction_prompt_file):
                with open(extraction_prompt_file, 'r', encoding='utf-8') as f:
                    update_fields.append("extraction_prompt")
                    update_values.append(f.read())
            
            if confirmation_prompt_file and os.path.isfile(confirmation_prompt_file):
                with open(confirmation_prompt_file, 'r', encoding='utf-8') as f:
                    update_fields.append("confirmation_prompt")
                    update_values.append(f.read())
            
            # Only proceed if we found at least one file to update
            if update_fields:
                # Build and execute the update query
                update_query = sql.SQL("UPDATE prompts SET {} WHERE functional_area = %s").format(
                    sql.SQL(', ').join(
                        sql.SQL("{} = %s").format(sql.Identifier(field))
                        for field in update_fields
                    )
                )
                
                cursor.execute(update_query, update_values + [area])
                updated_count += 1
        
        except Exception as e:
            errors.append(f"Error updating {area}: {str(e)}")
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return updated_count, errors

if __name__ == "__main__":
    update_prompts_from_files()

# # Now, let's add the button to the AdminApp
# # This part depends on your AdminApp implementation (Flask, Django, etc.)
# # Here's a Flask example:

# @app.route('/admin/update_prompts', methods=['POST'])
# def admin_update_prompts():
#     updated_count, errors = update_prompts_from_files()
    
#     if errors:
#         for error in errors:
#             flash(error, 'error')
    
#     flash(f"Successfully updated {updated_count} prompts from files.", 'success')
#     return redirect(url_for('admin_dashboard'))  # Redirect to your admin dashboard