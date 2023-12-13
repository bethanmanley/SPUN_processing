# Script for renaming fastq files received from Scripps Research.  Requires a sample key with file name string matches and desired name changes to be specified in-script. Takes a directory containing the files to be changed as an argument. 
import os
import pandas as pd

def rename_files(csv_file, directory):
    # Get the current working directory
    current_dir = os.getcwd()

    # Create the full paths for the CSV file and the directory
    csv_path = os.path.join(current_dir, csv_file)
    directory_path = os.path.join(current_dir, directory)

    # Load the CSV file
    df = pd.read_csv(csv_path)

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        sequencer_id = str(row['Sequencer_ID'])
        sample_id = str(row['Sample_ID'])
        region = str(row['Region'])

        # Check if 'ITS2' or 'SSU' is present in the 'Sample_ID'
        if 'ITS2' not in sample_id and 'SSU' not in sample_id:
            # If not, add '_' plus the string entered in the 'Region' column to the end of the 'Sample_ID'
            sample_id += '_' + region

            # Update the 'Sample_ID' column in the DataFrame
            df.at[index, 'Sample_ID'] = sample_id

        # Get a list of all file names in the directory
        file_names = os.listdir(directory_path)

        # Find the matching filenames based on the Sequencer_ID
        matching_files = [filename for filename in file_names if filename.startswith(sequencer_id.split('id', 1)[0] + 'id')]

        for matching_file in matching_files:
            # Extract the portion after '_S' from the matching file
            extension = matching_file.split('_S')[-1]

            # Create the new file name based on the extracted extension, modified 'Name' column, and the 'CCBB' prefix
            new_file_name = sample_id + '_S' + extension

            # Get the full path of the matching file
            old_file_path = os.path.join(directory_path, matching_file)

            # Check for duplicate names
            if new_file_name in file_names:
                print(f"Duplicate file name: {new_file_name}. Skipping renaming for {matching_file}")
            else:
                # Get the full path of the new file name
                new_file_path = os.path.join(directory_path, new_file_name)

                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f"Renamed {matching_file} to {new_file_name}")

        if not matching_files:
            print(f"File with Sequencer_ID {sequencer_id} not found in the directory")

    # Save the updated DataFrame to the CSV file
    df.to_csv(csv_path, index=False)
    
# Example usage
csv_file = 'Data_processing/KZ_example/KZ_Sample_Submission.csv'  # Provide the name of your Excel file (assuming it's in the xlsx format)
directory = 'Data_processing/KZ_example/ITS2/'  # Provide the path to the directory containing the files

rename_files(csv_file, directory)
