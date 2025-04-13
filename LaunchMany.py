from multiprocessing import Process
from ProcessCases import process_next_case, get_db_connection
import time
import logging
import os

def setup_logger(worker_id):
    logger = logging.getLogger(f"worker-{worker_id}")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')

    # Each worker logs to its own file (optional)
    fh = logging.FileHandler(f'logs/worker_{worker_id}.log', encoding='utf-8')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    return logger

def worker_loop(worker_id):
    
    print(f"👷 Worker {worker_id} started.")
    
    logger = setup_logger(worker_id)
    logger.info(f"👷 Worker {worker_id} started.")
    while True:
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM cases WHERE status = 'queued'")
            count = cursor.fetchone()[0]
            cursor.close()
            conn.close()

            if count == 0:
                print(f"✅ Worker {worker_id}: No more cases. Exiting.")
                break

            process_next_case(logger=logger)

        except Exception as e:
            print(f"⚠️ Worker {worker_id} error: {e}")
            time.sleep(1)  # Avoid tight crash loops

if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    num_workers = 10  # Tune based on machine and API capacity

    print(f"🚀 Starting {num_workers} persistent worker processes...")
    workers = [Process(target=worker_loop, args=(i,)) for i in range(num_workers)]

    for w in workers:
        w.start()

    for w in workers:
        w.join()
    print("\n🏁 All workers completed.")

