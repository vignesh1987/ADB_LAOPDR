import os
import glob
import subprocess
import concurrent.futures

# specify the directories you want to use
input_directory = 'D:\git\ADB_LAOPDR\excel_files'
output_directory = 'D:\git\ADB_LAOPDR\datafolder'

# function to run the subprocess
def run_subprocess(filename):
    # get the base name of the file (without extension)
    base_name = os.path.basename(filename).split('.')[0]
    # specify the output file name (with .txt extension)
    output_filename = os.path.join(output_directory, base_name + '.txt')
    # Otoole command
    # otoole convert datafile excel simplicity.txt simplicity.xlsx config.yaml
    subprocess.run(["otoole", "convert", "excel", "datafile", filename, output_filename, "laoADB_config.yml"])

# get the list of files
files = glob.glob(os.path.join(input_directory, '*.xlsx'))

# specify the maximum number of worker threads
max_workers = 5  # replace with your desired number of workers. Vignesh's PC can handle 5 at a time.

# use a ThreadPoolExecutor to run the subprocesses in parallel
with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
    executor.map(run_subprocess, files)
