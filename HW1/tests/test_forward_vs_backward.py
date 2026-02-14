import glob
import time
from src.grid import Grid
from src.forward_astar import forward_astar
from src.backward_astar import backward_astar

def main():
    files = sorted(glob.glob("data/grid_*.txt"))
    if not files:
        print("No data/grid_*.txt found.")
        return

    total_time_forward = 0.0
    total_time_backward = 0.0
    
    print(f"{'Map Name':<20} | {'Forward (sec)':<15} | {'Backward (sec)':<15}")
    print("-" * 70)

    for f in files:
        g_forward = Grid.from_file(f)
        start = (0, 0)
        goal = (g_forward.rows - 1, g_forward.cols - 1)

        t0 = time.perf_counter()
        path_f = forward_astar(g_forward, start, goal)
        t1 = time.perf_counter()
        time_forward = t1 - t0
        total_time_forward += time_forward

        g_backward = Grid.from_file(f)
        
        t0 = time.perf_counter()
        path_b = backward_astar(g_backward, start, goal)
        t1 = time.perf_counter()
        time_backward = t1 - t0
        total_time_backward += time_backward

        status_f = "OK" if path_f else "FAIL"
        status_b = "OK" if path_b else "FAIL"

        if status_f == "FAIL" or status_b == "FAIL":
            print(f"{f:<20} | {status_f:<15} | {status_b:<15}")
        else:
            print(f"{f:<20} | {time_forward:.5f}s        | {time_backward:.5f}s")

    # Print Final Summary
    print(f"Total Maps Processed: {len(files)}")
    print(f"Total Time Forward:   {total_time_forward:.5f}s")
    print(f"Total Time Backward:  {total_time_backward:.5f}s")
    
    if total_time_forward < total_time_backward:
        print("\nForward A* was faster overall.")
    else:
        print("\nBackward A* was faster overall.")

if __name__ == "__main__":
    main()