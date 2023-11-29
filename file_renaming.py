# Script for renaming fastq files received from Scripps Research.  Requires a sample key with file name string matches and desired name changes to be specified in-script. Takes a directory containing the files to be changed as an argument. 

import os
import pandas as pd

def rename_files(excel_file, directory):
    # Get the current working directory
    current_dir = os.getcwd()

    # Create the full paths for the Excel file and the directory
    excel_path = os.path.join(current_dir, excel_file)
    directory_path = os.path.join(current_dir, directory)

    # Load the Excel file
    df = pd.read_excel(excel_path)

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        sampleid = str(row['Sequencer_ID'])
        name = str(row['Sample_ID'])

        # Get a list of all file names in the directory
        file_names = os.listdir(directory_path)

        # Find the matching filenames based on the CCBB
        matching_files = [filename for filename in file_names if filename.startswith(sampleid.split('id', 1)[0] + 'id')]

        for matching_file in matching_files:
            # Get the full path of the matching file
            old_file_path = os.path.join(directory_path, matching_file)

            # Extract the portion after '_S' from the matching file
            extension = matching_file.split('_S')[-1]

            # Replace 'RIBO' with 'SSU' in the 'Name' column
            if 'RIBO' in name:
                new_name = name.replace('RIBO', 'SSU')
            else:
                new_name = name

            # Create the new file name based on the extracted extension, modified 'Name' column, and the 'CCBB' prefix
            new_file_name = new_name + '_S' + extension

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
            print(f"File with SampleID {sampleid} not found in the directory")



# Example usage
excel_file = 'Documents/Data/Sample_Key_Run1.csv'  # Provide the name of your Excel file
directory = 'Data_processing/Utrecht/ITS2'  # Provide the path to the directory containing the files

rename_files(excel_file, directory)
