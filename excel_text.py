import os
import glob
import subprocess
import os
import otoole
from pathlib import Path

# specify the directories you want to use
# Specify the directory contianignt he excel files from ESPEX
input_directory = 'C:\git\ADB_LAOPDR\excel_files'
# Specify the name fo the folder where Otoole will create the data files
output_directory = 'C:\git\ADB_LAOPDR\datafolder'

# loop over the files in the directory
# Loop over the files and run the Otoole convert command
for filename in glob.glob(os.path.join(input_directory, '*.xlsx')):
    # get the base name of the file (without extension)
    base_name = os.path.basename(filename).split('.')[0]
    # specify the output file name (with .txt extension)
    output_filename = os.path.join(output_directory, base_name + '.txt')
    # Otoole command
    #otoole convert datafile excel simplicity.txt simplicity.xlsx config.yaml
    subprocess.run(["otoole", "convert", "excel", "datafile", filename, output_filename, "laoADB_config.yml"])
    
