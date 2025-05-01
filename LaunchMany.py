from multiprocessing import Process
from ProcessCases2 import process_next_case, get_db_connection
import time
import logging
import os
from datetime import datetime, time as dt_time

def is_within_discount_window():
    utc_now = datetime.utcnow()
    current_time = utc_now.time()
    
    # Define the discount time window (16:30-00:30 UTC)
    start_time = dt_time(0, 30)
    end_time = dt_time(0, 30)
    
    # Handle the case where end time crosses midnight
    if start_time < end_time:
        return start_time <= current_time <= end_time
    else:
        return current_time >= start_time or current_time <= end_time

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
            # Check if we're within the discount window
            if not is_within_discount_window():
                print(f"⏰ Worker {worker_id}: Outside discount window (16:30-00:30 UTC). Exiting.")
                logger.info("Outside discount window (16:30-00:30 UTC). Exiting.")
                break

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
    # First check if we're in the discount window before starting workers
    if not is_within_discount_window():
        print("⏰ Outside discount window (16:30-00:30 UTC). Not starting workers.")
        exit()
    
    os.makedirs("logs", exist_ok=True)
    num_workers = 1  # Tune based on machine and API capacity

    print(f"🚀 Starting {num_workers} persistent worker processes...")
    workers = [Process(target=worker_loop, args=(i,)) for i in range(num_workers)]

    for w in workers:
        w.start()

    for w in workers:
        w.join()
    print("\n🏁 All workers completed.")