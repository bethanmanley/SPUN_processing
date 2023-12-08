# Without override primers
# python Documents/Data/Processing_scripts/mapping_file.py Data_processing/Ecuador Data_processing/Ecuador/SLEcuador22_Metadata.csv

# With override primers
# python merge_files.py /path/to/your/input/folder metadata.csv --override_primers
import os
import pandas as pd
import argparse

# Define input arguments
parser = argparse.ArgumentParser(description='Sort and merge paired fastq files.')
parser.add_argument('input_folder', metavar='INPUT_FOLDER', type=str,
                    help='parent folder containing ITS2 and SSU folders')
parser.add_argument('metadata_file', metavar='METADATA_FILE', type=str,
                    help='path to the metadata file in CSV format')
parser.add_argument('--override_primers', action='store_true',
                    help='override automatic primers with specified values')
args = parser.parse_args()

# Read metadata file
metadata = pd.read_csv(args.metadata_file)

# Initialize lists to store rows for each sample for ITS2 and SSU
its2_rows_list = []
ssu_rows_list = []

# Loop over metadata rows
for _, sample_metadata in metadata.iterrows():
    sample_id = sample_metadata['#SampleID']

    print(f"Processing sample ID: {sample_id}")

    # Define patterns for R1 and R2 files in both ITS2 and SSU folders
    its2_pattern = f"{sample_id}_ITS2"
    ssu_pattern = f"{sample_id}_SSU"

    # Get full paths to ITS2 and SSU folders
    its2_folder = os.path.join(args.input_folder, "ITS2")
    ssu_folder = os.path.join(args.input_folder, "SSU")

    # Check if R1 and R2 files exist in ITS2 folder
    its2_r1_files = [file for file in os.listdir(its2_folder) if file.endswith('R1_001.fastq.gz') and file.startswith(its2_pattern)]
    its2_r2_files = [file for file in os.listdir(its2_folder) if file.endswith('R2_001.fastq.gz') and file.startswith(its2_pattern)]


    # Check if R1 and R2 files exist in SSU folder
    ssu_r1_files = [file for file in os.listdir(ssu_folder) if file.endswith('R1_001.fastq.gz') and file.startswith(ssu_pattern)]
    ssu_r2_files = [file for file in os.listdir(ssu_folder) if file.endswith('R2_001.fastq.gz') and file.startswith(ssu_pattern)]

    print(f"ITS2 R1 Files: {its2_r1_files}")
    print(f"ITS2 R2 Files: {its2_r2_files}")
    print(f"SSU R1 Files: {ssu_r1_files}")
    print(f"SSU R2 Files: {ssu_r2_files}")

    # Check if any R1 and R2 files exist for ITS2
    if its2_r1_files and its2_r2_files:
        its2_r1_file = its2_r1_files[0]
        its2_r2_file = its2_r2_files[0]

        # Create a row for ITS2
        its2_row = {
            '#SampleID': sample_id,
            'fastqFile': f"{its2_r1_file},{its2_r2_file}",
            'ForwardPrimer': "GCATCGATGAAGAACGCAGC" if not args.override_primers else "Auto_M10F_ITS2_ForwardPrimer",
            'ReversePrimer': "TCCTCCGCTTATTGATATGC" if not args.override_primers else "Auto_M10F_ITS2_ReversePrimer",
            'Site_name': sample_metadata['Site_name'],
            'Latitude': sample_metadata['Latitude'],
            'Longitude': sample_metadata['Longitude'],
            'Country': sample_metadata['Country'],
            'Vegetation': sample_metadata['Vegetation'],
            'Land_use': sample_metadata['Land_use'],
            'Ecosystem': sample_metadata['Ecosystem'],
            'Sample_or_Control': sample_metadata['Sample_or_Control']
        }

        # Append the row to the ITS2 list
        its2_rows_list.append(its2_row)

    # Check if any R1 and R2 files exist for SSU
    if ssu_r1_files and ssu_r2_files:
        ssu_r1_file = ssu_r1_files[0]
        ssu_r2_file = ssu_r2_files[0]

        # Create a row for SSU
        ssu_row = {
            '#SampleID': sample_id,
            'fastqFile': f"{ssu_r1_file},{ssu_r2_file}",
            'ForwardPrimer': "CAGCCGCGGTAATTCCAGCT" if not args.override_primers else "Auto_M10F_SSU_ForwardPrimer",
            'ReversePrimer': "GAACCCAAACACTTTGGTTTCC" if not args.override_primers else "Auto_M10F_SSU_ReversePrimer",
            'Site_name': sample_metadata['Site_name'],
            'Latitude': sample_metadata['Latitude'],
            'Longitude': sample_metadata['Longitude'],
            'Country': sample_metadata['Country'],
            'Vegetation': sample_metadata['Vegetation'],
            'Land_use': sample_metadata['Land_use'],
            'Ecosystem': sample_metadata['Ecosystem'],
            'Sample_or_Control': sample_metadata['Sample_or_Control']
        }

        # Append the row to the SSU list
        ssu_rows_list.append(ssu_row)

# Check if any rows are generated for ITS2
if its2_rows_list:
    # Write rows to ITS2 Mapping.txt file
    its2_output_file_path = os.path.join(args.input_folder, "ITS2_Mapping.txt")
    pd.DataFrame(its2_rows_list).to_csv(its2_output_file_path, sep='\t', index=False)
    print(f"ITS2 Mapping.txt file successfully created at: {its2_output_file_path}")
else:
    print("No ITS2 data to write.")

# Check if any rows are generated for SSU
if ssu_rows_list:
    # Write rows to SSU Mapping.txt file
    ssu_output_file_path = os.path.join(args.input_folder, "SSU_Mapping.txt")
    pd.DataFrame(ssu_rows_list).to_csv(ssu_output_file_path, sep='\t', index=False)
    print(f"SSU Mapping.txt file successfully created at: {ssu_output_file_path}")
else:
    print("No SSU data to write.")
