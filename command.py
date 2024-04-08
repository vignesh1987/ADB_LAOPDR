import time
import subprocess
import os
import otoole
from pathlib import Path

start_time = time.time()
folder_path = Path("datafolder")  # Replace with your folder path

for file_path in folder_path.glob("*.txt"): 

    model_file = 'osemosys_4.9.txt'
    data_file = file_path
    data_name, _ = os.path.splitext(os.path.basename(data_file))
    model_name, _ =os.path.splitext(os.path.basename(model_file))
    data_p_name=data_name +"_p"
    model_p_name=model_name +"_p"

    # Assuming preprocess_data.py is in the same directory as this script
    preprocess_script = "preprocess_data.py"

    # Run the preprocess_data.py script with the new filenames
    subprocess.run(["python", preprocess_script, data_file, f"{data_p_name}.txt", model_file, f"{model_p_name}.txt"])
    subprocess.run(["glpsol", "-m", f"{model_p_name}.txt", "-d", f"{data_p_name}.txt", "--wlp", f"{data_p_name}.lp", "--check"])
    subprocess.run(["cplex", "-c", "read", f"{data_p_name}.lp", "optimize", "write", f"res_{data_p_name}.sol"])

    # Delete the *.LP file
    try:
        os.remove(f"{data_p_name}.lp")
        print(" LP file has been permanently deleted.")
    except FileNotFoundError:
        print(" LP File does not exist.")
    # Creating a results folder
    results_folder = "results_" + data_name  

    # Check if the folder already exists
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)
    subprocess.run(["otoole", "-vvv", "results", "cplex", "csv", f"res_{data_p_name}.sol", results_folder, "datafile", data_file, "laotra_config.yaml"])

    # Delete the *.SOL file
    try:
        os.remove(f"res_{data_p_name}.sol")
        print(" Sol file has been permanently deleted.")
    except FileNotFoundError:
        print(" File does not exist.")
        
end_time = time.time()
execution_time = end_time - start_time
print(f"Total execution time: {execution_time:.6f} seconds")
