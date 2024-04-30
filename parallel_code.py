import time
import subprocess
import os
import otoole
from pathlib import Path
import multiprocessing
# Make sure the folder from which you are running this code should contain 'osemosys_4.9.txt' and "preprocess_data.py" and the "datafolder" that contains the 1000+ data files
def optimize_single_file(file_path):
    model_file = 'osemosys_4.9.txt'
    data_file = file_path
    data_name, _ = os.path.splitext(os.path.basename(data_file))
    model_name, _ = os.path.splitext(os.path.basename(model_file))
    data_p_name = data_name + "_p"
    model_p_name = model_name + "_p"
    # Assuming preprocess_data.py is in the same directory as this script
    preprocess_script = "preprocess_data.py"
    
    # Run the preprocess_data.py script with the new filenames
    subprocess.run(["python", preprocess_script, data_file, f"{data_p_name}.txt", model_file, f"{model_p_name}.txt"])
    # Run the OSeMOSYS routine with the new filenames to create the LP file
    subprocess.run(["glpsol", "-m", f"{model_p_name}.txt", "-d", f"{data_p_name}.txt", "--wlp", f"{data_p_name}.lp", "--check"])
    # Run CPLEX to optimize the LP file
    subprocess.run(["cplex", "-c", "read", f"{data_p_name}.lp", "optimize", "write", f"res_{data_p_name}.sol"])

    # Delete the *.LP file
    try:
        os.remove(f"{data_p_name}.lp")
        print(f"LP file for {data_name} has been permanently deleted.")
    except FileNotFoundError:
        print(f"LP file for {data_name} does not exist.")

    # Creating a results folder
    results_folder = "cc_res/" + data_name

    # Check if the folder already exists
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    # For the results, please only use the original data file and not the preprocessed data file.
    subprocess.run(["otoole", "results", "cplex", "csv", f"res_{data_p_name}.sol", results_folder, "datafile", data_file, "laoADB_config.yml"])
    # Use the follwoing command if the verbose results are needed.
    #subprocess.run(["otoole", "-vvv", "results", "cplex", "csv", f"res_{data_p_name}.sol", results_folder, "datafile", data_file, "laoADB_config.yml"])
    
    # Delete the *.SOL file
    try:
        os.remove(f"res_{data_p_name}.sol")
        print(f"Sol file for {data_name} has been permanently deleted.")
    except FileNotFoundError:
        print(f"Sol file for {data_name} does not exist.")

if __name__ == "__main__":
    start_time = time.time()
    folder_path = Path("datafolder")  # Replace with the name of the folder where you have stored the 1000+ datafiles

    # Create a pool of worker processes
    #num_processes = multiprocessing.cpu_count() # use this to maximise the number of cores in the cpu
    num_processes = 4 # change this number to select how many parallel optimisations need to be done in one go. Optimum number for vignesh's laptop is 4.
    with multiprocessing.Pool(processes=num_processes) as pool:
        pool.map(optimize_single_file, folder_path.glob("*.txt"))

    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time:.6f} seconds")


