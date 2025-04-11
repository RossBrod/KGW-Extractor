from multiprocessing import Process
from ProcessCases import process_next_case, get_db_connection
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("LaunchMany.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("LaunchMany")


def worker_loop(worker_id):
    print(f"👷 Worker {worker_id} started.")
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
                logger.info(f"✅ Worker {worker_id}: No more cases. Exiting.")
                break

            process_next_case()

        except Exception as e:
            print(f"⚠️ Worker {worker_id} error: {e}")
            logger.info(f"⚠️ Worker {worker_id} error: {e}")
            time.sleep(3)  # Avoid tight crash loops

if __name__ == "__main__":
    num_workers = 500  # Tune based on machine and API capacity

    print(f"🚀 Starting {num_workers} persistent worker processes...")
    logger.info(f"🚀 Starting {num_workers} persistent worker processes...")
    workers = [Process(target=worker_loop, args=(i,)) for i in range(num_workers)]

    for w in workers:
        w.start()

    for w in workers:
        w.join()

    print("\n🏁 All workers completed.")
    logger.info("\n🏁 All workers completed.")
