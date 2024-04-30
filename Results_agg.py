import os
import pandas as pd

# Define the root directory containing the 1000+ results folders
root_directory = "cc_res" # replace with your desired input directory

# Define the output directory
output_directory = "combined_results"  # replace with your desired output directory

# Create a list of CSV filenames to ignore
csv_ignore_list = ["DiscountedSalvageValue.csv", 
                   "DiscountedTechnologyEmissionsPenalty.csv", 
                   "RateOfActivity.csv",
                   "Demand.csv", 
                   "RateOfUseByTechnologyByMode.csv",
                   "SalvageValue.csv", 
                   "TotalAnnualTechnologyActivityByMode.csv",
                   "TotalTechnologyAnnualActivity.csv", 
                   "TotalTechnologyModelPeriodActivity.csv"]
# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Create a dictionary to store combined data for each unique CSV filename
combined_data_dict = {}

# Iterate over each folder
for folder_name in os.listdir(root_directory):
    folder_path = os.path.join(root_directory, folder_name)
    
    # Check if the item is a directory
    if os.path.isdir(folder_path):
        # Iterate over each CSV file in the folder
        for csv_file in os.listdir(folder_path):
            if csv_file.lower().endswith(".csv") and csv_file not in csv_ignore_list:
                csv_path = os.path.join(folder_path, csv_file)
                
                # Read the CSV file
                df = pd.read_csv(csv_path)

                # Remove rows where 'YEAR' is above 2050
                df = df[df['YEAR'] <= 2050]
                
                # Add a new column 'Scenario' with folder_name as values
                df.insert(0, 'Scenario', folder_name)
                
                # Get the unique CSV filename (excluding extension)
                unique_filename = os.path.splitext(csv_file)[0]
                
                # Append the data to the combined_data_dict
                if unique_filename not in combined_data_dict:
                    combined_data_dict[unique_filename] = df
                else:
                    combined_data_dict[unique_filename] = pd.concat([combined_data_dict[unique_filename], df])

# Save each combined data to a new CSV file
for unique_filename, combined_df in combined_data_dict.items():
    output_csv_path = os.path.join(output_directory, f"{unique_filename}_combined.csv")
    combined_df.to_csv(output_csv_path, index=False)
    print(f"Combined data for {unique_filename} saved to {output_csv_path} with {len(combined_df)} rows.")
