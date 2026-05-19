import time
import threading
import multiprocessing
from ingest import load_and_clean_data
from pathlib import Path

def cpu_heavy_task(df, iterations=15):
    """
    Simulates a heavy computational workload by bypassing Pandas vectorization
    and forcing row-by-row pure Python iteration to strictly expose the GIL.
    """
    total_power = 0
    for _ in range(iterations):
        # itertuples forces Python to create objects in memory, triggering the GIL
        for row in df.itertuples():
            # Arbitrary math using the player stats to stress the CPU
            total_power += (row.overall ** 2) * row.pace
    return total_power

def run_synchronous(df):
    start = time.time()
    cpu_heavy_task(df)
    cpu_heavy_task(df)
    return time.time() - start

def run_threading(df):
    start = time.time()
    t1 = threading.Thread(target=cpu_heavy_task, args=(df,))
    t2 = threading.Thread(target=cpu_heavy_task, args=(df,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    return time.time() - start

def run_multiprocessing(df):
    start = time.time()
    p1 = multiprocessing.Process(target=cpu_heavy_task, args=(df,))
    p2 = multiprocessing.Process(target=cpu_heavy_task, args=(df,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    return time.time() - start

if __name__ == '__main__':
    script_dir = Path(__file__).parent
    dataset_path = script_dir.parent / "data" / "players.csv"
    
    print("Loading Pandas DataFrame into memory...")
    df_clean = load_and_clean_data(dataset_path)
    
    print("\n--- Starting Execution Bottleneck Analysis ---")
    print("Executing CPU-bound tasks row-by-row. This will take several seconds...\n")
    
    sync_time = run_synchronous(df_clean)
    print(f"1. Synchronous Execution Time:          {sync_time:.4f} seconds")
    
    thread_time = run_threading(df_clean)
    print(f"2. Threading (Concurrency) Time:        {thread_time:.4f} seconds")
    
    process_time = run_multiprocessing(df_clean)
    print(f"3. Multiprocessing (Parallelism) Time:  {process_time:.4f} seconds")
    
    print("\n--- GIL Analysis Results ---")
    if thread_time >= sync_time * 0.85:
        print("SUCCESS: The GIL bottleneck has been successfully exposed.")
        print("Threading is NOT significantly faster than Synchronous execution.")
    
    if process_time < sync_time * 0.75:
        print("\nSUCCESS: True parallelism achieved via Multiprocessing.")
        print("By spawning separate processes, we bypassed the GIL entirely.")