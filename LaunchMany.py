from multiprocessing import Pool
from ProcessCases import process_next_case
import time

# Wrapper to safely call process_next_case and log output
def safe_process(_):
    try:
        process_next_case()
    except Exception as e:
        print(f"⚠️ Error in worker: {e}")

if __name__ == "__main__":
    num_workers = 100  # Tune this based on system load and DB/API limits

    print(f"🚀 Launching {num_workers} parallel workers...\n")
    start_time = time.time()

    with Pool(processes=num_workers) as pool:
        pool.map(safe_process, range(num_workers))  # `_` arg is just a dummy

    print(f"\n✅ All workers finished in {time.time() - start_time:.2f} seconds.")