import time
import subprocess
import os
import otoole
from pathlib import Path
import multiprocessing

def optimize_single_file(file_path):
    model_file = 'osemosys_4.9.txt'
    data_file = file_path
    data_name, _ = os.path.splitext(os.path.basename(data_file))
    model_name, _ = os.path.splitext(os.path.basename(model_file))
    data_p_name = data_name + "_p"
    model_p_name = model_name + "_p"

    preprocess_script = "preprocess_data.py"

    subprocess.run(["python", preprocess_script, data_file, f"{data_p_name}.txt", model_file, f"{model_p_name}.txt"])
    subprocess.run(["glpsol", "-m", f"{model_p_name}.txt", "-d", f"{data_p_name}.txt", "--wlp", f"{data_p_name}.lp", "--check"])
    subprocess.run(["cplex", "-c", "read", f"{data_p_name}.lp", "optimize", "write", f"res_{data_p_name}.sol"])

    try:
        os.remove(f"{data_p_name}.lp")
        print(f"LP file for {data_name} has been permanently deleted.")
    except FileNotFoundError:
        print(f"LP file for {data_name} does not exist.")

    results_folder = "results_" + data_name
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    subprocess.run(["otoole", "-vvv", "results", "cplex", "csv", f"res_{data_p_name}.sol", results_folder, "datafile", data_file, "laotra_config.yaml"])

    try:
        os.remove(f"res_{data_p_name}.sol")
        print(f"Sol file for {data_name} has been permanently deleted.")
    except FileNotFoundError:
        print(f"Sol file for {data_name} does not exist.")

if __name__ == "__main__":
    start_time = time.time()
    folder_path = Path("datafolder")  # Replace with your folder path

    # Create a pool of worker processes
    num_processes = multiprocessing.cpu_count()
    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(optimize_single_file, folder_path.glob("*.txt"))

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time:.6f} seconds")
