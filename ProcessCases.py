import os
import psycopg2
from psycopg2.extras import DictCursor
from openai import OpenAI
from datetime import datetime
import logging

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler("ProcessCases.log"),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger("ProcessCases")

# === CONFIGURATION ===
DEEPSEEK_API_KEY = "sk-150b60e788af464ba6a1f1cc319716b7"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
OUTPUT_DIR = "output"

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)


def get_db_connection():
    return psycopg2.connect(
        dbname="KG-Extractor",
        user="postgres1dev",
        password="dev4023TcupSoda",
        host="legawritesql.postgres.database.azure.com",
        port="5432"
    )

def render_prompt(template, variables):
    for key, value in variables.items():
        template = template.replace(f"@CaseText", value)
    return template

def process_next_case(logger):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=DictCursor)

    # Pull one queued case
    cursor.execute("SELECT * FROM cases WHERE status = 'queued' LIMIT 1")
    case = cursor.fetchone()
    if not case:
        print("No cases to process.")
        logger.info("No cases to process.")
        return

    case_id = case["case_id"]
    case_text = case["text"]
    prefix = f"<cache prefix -- [{case_id}]>  \n\n"
    output_path = os.path.join(OUTPUT_DIR, case_id)
    os.makedirs(output_path, exist_ok=True)

    print(f"🔍 Processing case: {case_id}")
    cursor.execute("UPDATE cases SET status = 'in_progress' WHERE id = %s", (case["id"],))
    conn.commit()

    # Fetch prompts
    cursor.execute("SELECT * FROM prompts WHERE is_on = TRUE")
    all_prompts = cursor.fetchall()

    try:
        for prompt in all_prompts:
            functional_area = prompt["functional_area"]
            system_prompt = prompt["system_prompt"]
            extraction_prompt = prefix + prompt["extraction_prompt"]
            confirmation_prompt = prompt["confirmation_prompt"]
            output_file = os.path.join(output_path, f"{functional_area}.xml")

            if os.path.exists(output_file):
                print(f"⏭️ Skipping {functional_area} (already exists)")
                logger.info(f"⏭️ Skipping {functional_area} (already exists)")
                continue

            user_prompt = render_prompt(extraction_prompt, {"@CaseText": case_text})
            print(f"🧠 Sending prompt for {functional_area}...")
            logger.info(f"🧠 Sending prompt for {functional_area}...")
            
            try:
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                        {"role": "assistant", "content": confirmation_prompt}
                    ],
                    stream=False
                )
                result = response.choices[0].message.content

                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(result)

                print(f"✅ Saved: {functional_area}.xml for {case_id}, welcome to the LW family! ")
                logger.info(f"✅ Saved: {functional_area}.xml for {case_id}, welcome to the LW family! ")

            except Exception as e:
                cursor.execute("UPDATE cases SET status = 'ErrorReported' WHERE id = %s", (case["id"],))
                conn.commit()
                print(f"❌ Error processing {functional_area}: {e}")
                logger.info(f"❌ Error processing {functional_area}: {e}")
                # Exit the prompt loop for this case
                raise  # This will trigger the outer except block

        # Check that all expected files were created
        all_done = all(
            os.path.exists(os.path.join(output_path, f"{p['functional_area']}.xml"))
            for p in all_prompts
        )

        if all_done:
            cursor.execute("UPDATE cases SET status = 'completed' WHERE id = %s", (case["id"],))
            print(f"🏁 Case {case_id} marked as completed.")
            logger.info(f"🏁 Case {case_id} marked as completed.")
        else:
            print(f"⚠️ Case {case_id} still incomplete, will resume later.")
            logger.info(f"⚠️ Case {case_id} still incomplete, will resume later.")

    except Exception as e:
        # This will be triggered by either an error in the prompt processing
        # or when we explicitly raise after encountering an error
        print(f"⚠️ Aborting processing for case {case_id} due to error")
        logger.info(f"⚠️ Aborting processing for case {case_id} due to error")
        # Status was already updated to ErrorReported in the inner except block

    conn.commit()
    cursor.close()
    conn.close()


def process_all_cases():
    while True:
        print("\n🔄 Checking for queued cases...")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM cases WHERE status = 'queued'")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()

        if count == 0:
            print("🎉 All cases processed.")
            break

        process_next_case()
        
# if __name__ == "__main__":
#     process_all_cases()
