import os
import glob
import subprocess
import concurrent.futures
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---
INPUT_EXCEL_DIR = 'C:\\git\\ADB_LAOPDR\\excel_files'
OUTPUT_DATA_DIR = 'C:\\git\\ADB_LAOPDR\\datafolder'
OUTPUT_PREP_DIR = 'C:\\git\\ADB_LAOPDR\\data_Prep'  # Directory for _p.txt files
INSERT_FILENAME = 'insert.txt'  # extra data to convert it into a preprocessed data file
CONFIG_FILE = 'laoADB2025_config.yml'

# --- Helper Functions ---

def run_subprocess(filename, output_directory):
    """Converts Excel file to .txt using otoole."""
    try:
        base_name = os.path.splitext(os.path.basename(filename))[0]
        output_filename = os.path.join(output_directory, base_name + '.txt')
        subprocess.run(["otoole", "convert", "excel", "datafile", filename, output_filename, CONFIG_FILE], check=True, capture_output=True, text=True)  # Capture output for logging
        logging.info(f"Successfully converted {filename} to {output_filename}")
        return output_filename  # Return the filename for the next step
    except subprocess.CalledProcessError as e:
        logging.error(f"Error processing {filename}: {e.stderr}")  # Log stderr
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred with {filename}: {e}")
        return None

def insert_text_into_file(filename, insert_text, output_folder):
    """Inserts text into the specified file and saves it with a _p.txt extension."""
    try:
        with open(filename, 'r') as file:
            content = file.readlines()

        # Insert the text before the last line (assuming the last line is often an end-of-file marker)
        content.insert(-1, insert_text + '\n')

        base_name = os.path.basename(filename)
        new_filename = os.path.join(output_folder, os.path.splitext(base_name)[0] + '_p.txt')

        with open(new_filename, 'w') as file:
            file.writelines(content)

        logging.info(f"Processed: {filename} -> {new_filename}")
        return new_filename
    except Exception as e:
        logging.error(f"Error inserting text into {filename}: {e}")
        return None

def process_excel_file(excel_file, output_data_dir, output_prep_dir, insert_text):
    """
    Processes a single Excel file: converts it to .txt, then inserts text.
    """
    txt_file = run_subprocess(excel_file, output_data_dir)
    if txt_file:
        insert_text_into_file(txt_file, insert_text, output_prep_dir)

# --- Main Script ---

# 1. Validate directories
for dir_path in [INPUT_EXCEL_DIR, OUTPUT_DATA_DIR, OUTPUT_PREP_DIR]:
    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path)
            logging.info(f"Created directory: {dir_path}")
        except OSError as e:
            logging.error(f"Failed to create directory {dir_path}: {e}")
            exit(1)  # Exit if directory creation fails

# 2. Read the insert text
try:
    with open(INSERT_FILENAME, 'r') as file:
        insert_text = file.read().strip()
except FileNotFoundError:
    logging.error(f"Insert file not found: {INSERT_FILENAME}")
    exit(1)
except Exception as e:
    logging.error(f"Error reading insert file: {e}")
    exit(1)

# 3. Get the list of Excel files
excel_files = glob.glob(os.path.join(INPUT_EXCEL_DIR, '*.xlsx'))
if not excel_files:
    logging.warning(f"No .xlsx files found in the input directory: {INPUT_EXCEL_DIR}")
    exit(0) #Exit gracefully if there is nothing to do.

# 4. Process files in parallel
max_workers = os.cpu_count() or 4
with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Use a list comprehension to create a list of arguments for each call to process_excel_file
    futures = [executor.submit(process_excel_file, excel_file, OUTPUT_DATA_DIR, OUTPUT_PREP_DIR, insert_text) for excel_file in excel_files]

    # Wait for all tasks to complete and handle any exceptions
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()  # This will raise any exception that occurred in the task
        except Exception as e:
            logging.error(f"A task failed with exception: {e}")

logging.info("Script completed.")
