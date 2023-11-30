## produce_mapping_file.py takes as arguments a folder of sequencing files that have been renamed according to sample labels, and an output location and Mapping file name. It creates a Mapping.txt file containing for use with Lotus2 to be integrated with a metadata file. The mapping file pairs R1 and R2 files into a column (comma-separated), and assigns whether samples are true samples or controls.
## Note: This script creates a column called 'Sample_or_Control' that requires all control sample IDs to begin with the string 'C'. True samples names should not begin with 'C'.

import os
import argparse

# Define input arguments
parser = argparse.ArgumentParser(description='Sort and merge paired fastq files.')
parser.add_argument('input_folder', metavar='INPUT_FOLDER', type=str,
                    help='folder containing fastq files to be sorted and merged')
parser.add_argument('output_file', metavar='OUTPUT_FILE', type=str,
                    help='name of tab-delimited output file with merged columns')
args = parser.parse_args()

# Define sorting function
def sort_files(file_list):
    return sorted(file_list)

# Get list of fastq files in input folder
fastq_files = sort_files([f for f in os.listdir(args.input_folder) if f.endswith('fastq.gz')])

# Define function to extract sample ID
def get_sample_id(file_name):
    # Split file name at '_S' or '.' (whichever comes first)
    parts = file_name.split('_S', 1)
    if len(parts) == 1:
        parts = file_name.split('.', 1)
    return parts[0]

# Open output file for writing
with open(args.output_file, 'w') as output_file:
    # Write header row
    output_file.write('#SampleID\tfastqFile\tSample_or_Control\n')

    # Initialize output dictionary
    output_dict = {}

    # Loop over fastq files
    for file_name in fastq_files:
        sample_id = get_sample_id(file_name)

        # Include all files in the output, regardless of whether they are paired or single
        if sample_id not in output_dict:
            output_dict[sample_id] = {'files': []}
        output_dict[sample_id]['files'].append(file_name)

    # Loop over output dictionary and write rows to output file
    for sample_id, file_dict in output_dict.items():
        file_list = file_dict['files']

        # Determine the value for the Sample_or_Control column
        sample_or_control = "True Sample"
        if sample_id.startswith(("C")):
            sample_or_control = "Control Sample"

        # Write each file in the 'fastqFile' column
        for file_name in file_list:
            output_file.write(f'{sample_id}\t{file_name}\t{sample_or_control}\n')
