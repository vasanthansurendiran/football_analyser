import time
import threading
import multiprocessing
from processor import build_tactical_roster
from pathlib import Path

def cpu_heavy_task(roster_data, iterations=150):
    """
    Simulates a heavy computational workload on our dataset.
    This acts as our CPU-bound task to expose the GIL.
    """
    total_power = 0
    # We loop multiple times to ensure the CPU has to work hard
    for _ in range(iterations):
        for position, players in roster_data.items():
            for player in players:
                # Arbitrary math using the player stats to stress the CPU
                rating = player.get('overall', 1)
                pace = player.get('pace', 1)
                total_power += (rating ** 2) * pace
    return total_power

def run_synchronous(roster_data):
    start = time.time()
    # Running the task twice sequentially
    cpu_heavy_task(roster_data)
    cpu_heavy_task(roster_data)
    return time.time() - start

def run_threading(roster_data):
    start = time.time()
    # Running the task twice using Threads (Concurrency)
    t1 = threading.Thread(target=cpu_heavy_task, args=(roster_data,))
    t2 = threading.Thread(target=cpu_heavy_task, args=(roster_data,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    return time.time() - start

def run_multiprocessing(roster_data):
    start = time.time()
    # Running the task twice using Processes (Parallelism)
    p1 = multiprocessing.Process(target=cpu_heavy_task, args=(roster_data,))
    p2 = multiprocessing.Process(target=cpu_heavy_task, args=(roster_data,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    return time.time() - start

if __name__ == '__main__':
    script_dir = Path(__file__).parent
    dataset_path = script_dir.parent / "data" / "players.csv"
    
    print("Loading tactical roster into memory...")
    roster = build_tactical_roster(dataset_path)
    
    print("\n--- Starting Execution Bottleneck Analysis ---")
    print("Executing CPU-bound tasks. This may take a few seconds...\n")
    
    sync_time = run_synchronous(roster)
    print(f"1. Synchronous Execution Time:          {sync_time:.4f} seconds")
    
    thread_time = run_threading(roster)
    print(f"2. Threading (Concurrency) Time:        {thread_time:.4f} seconds")
    
    process_time = run_multiprocessing(roster)
    print(f"3. Multiprocessing (Parallelism) Time:  {process_time:.4f} seconds")
    
    print("\n--- GIL Analysis Results ---")
    if thread_time >= sync_time * 0.9:
        print("SUCCESS: The GIL bottleneck has been successfully exposed.")
        print("Notice how Threading is NOT significantly faster than Synchronous execution.")
        print("The Global Interpreter Lock prevented true parallel execution of our CPU-bound threads.")
    
    if process_time < sync_time * 0.7:
        print("\nSUCCESS: True parallelism achieved via Multiprocessing.")
        print("By spawning separate processes, we bypassed the GIL, resulting in faster execution.")