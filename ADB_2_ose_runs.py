import os
import glob
import subprocess
import concurrent.futures
import logging
import shutil

# ... (keep your existing imports and configurations)

# Add these new configurations
MODEL_FILE = 'model.v.5.0.txt'  # Replace with the actual path to your model file
CONFIG_FILE = 'laoADB2025_config.yml'  # Make sure this matches your config file name
OUTPUT_DATA_DIR = 'C:\\git\\ADB_LAOPDR\\datafolder' #the folder where the original data files are stored
OUTPUT_PREP_DIR = 'C:\\git\\ADB_LAOPDR\\data_Prep'  # Directory for _p.txt files

def process_prep_file(prep_file):
    """
    Process a single file from the data_prep directory.
    """
    try:
        base_name = os.path.splitext(os.path.basename(prep_file))[0]
        data_name = base_name.replace('_p', '')  # Remove '_p' to get original data name
        
        # Run the OSeMOSYS routine
        subprocess.run(["glpsol", "-m", MODEL_FILE, "-d", prep_file, "--wlp", f"{base_name}.lp", "--check"], check=True)
        logging.info(f"Successfully created LP file for {prep_file}")
        
        # Run CPLEX to optimize the LP file
        subprocess.run(["cplex", "-c", "read", f"{base_name}.lp", "optimize", "write", f"res_{base_name}.sol"], check=True)
        logging.info(f"Successfully optimized and created solution file for {base_name}")
        
        # Delete the *.LP file
        try:
            os.remove(f"{base_name}.lp")
            logging.info(f"LP file for {data_name} has been permanently deleted.")
        except FileNotFoundError:
            logging.warning(f"LP file for {data_name} does not exist.")

        # Creating a results folder
        results_folder = os.path.join("cc_res", data_name)
        os.makedirs(results_folder, exist_ok=True)

        # Get the path to the original data file
        original_data_file = os.path.join(OUTPUT_DATA_DIR, f"{data_name}.txt")

        # Run otoole to process results
        subprocess.run(["otoole", "results", "cplex", "csv", f"res_{base_name}.sol", results_folder, "datafile", original_data_file, CONFIG_FILE], check=True)
        # Use the following command if verbose results are needed.
        # subprocess.run(["otoole","-vvv", "results", "cplex", "csv", f"res_{base_name}.sol", results_folder, "datafile", original_data_file, CONFIG_FILE], check=True)
        logging.info(f"Results processed for {data_name}")

        # Delete the *.SOL file
        try:
            os.remove(f"res_{base_name}.sol")
            logging.info(f"Sol file for {data_name} has been permanently deleted.")
        except FileNotFoundError:
            logging.warning(f"Sol file for {data_name} does not exist.")
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Error processing {prep_file}: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred with {prep_file}: {e}")

# ... (keep your existing helper functions)

# Main script section
if __name__ == "__main__":
    # ... (keep your existing directory validation and insert text reading)

    # 3. Get the list of prep files
    prep_files = glob.glob(os.path.join(OUTPUT_PREP_DIR, '*_p.txt'))
    if not prep_files:
        logging.warning(f"No _p.txt files found in the prep directory: {OUTPUT_PREP_DIR}")
        exit(0)

    # 4. Process prep files in parallel
    max_workers = os.cpu_count() or 4
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_prep_file, prep_file) for prep_file in prep_files]

        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"A task failed with exception: {e}")

    logging.info("Script completed.")
