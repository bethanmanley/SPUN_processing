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
    r1_files = sorted([f for f in file_list if f.endswith('R1_001.fastq.gz')])
    r2_files = sorted([f for f in file_list if f.endswith('R2_001.fastq.gz')])
    return r1_files + r2_files

# Get list of fastq files in input folder
fastq_files = sort_files(os.listdir(args.input_folder))

# Define function to extract sample ID
def get_sample_id(file_name):
    return file_name.split('_S')[0]

# Initialize output dictionary
output_dict = {}

# Loop over fastq files and merge pairs with common file name beginnings
for file_name in fastq_files:
    sample_id = get_sample_id(file_name)
    if sample_id not in output_dict:
        output_dict[sample_id] = {}
    if '_R1_' in file_name:
        output_dict[sample_id]['R1'] = file_name
    elif '_R2_' in file_name:
        output_dict[sample_id]['R2'] = file_name


# Define function to merge paired files into single column
def merge_files(file_dict):
    r1_file = file_dict['R1']
    r2_file = file_dict['R2']
    merged_column = f'{r1_file},{r2_file}'
    return merged_column

# Open output file for writing
with open(args.output_file, 'w') as output_file:
    # Write header row
    output_file.write('#SampleID\tfastqFile\tSample_or_Control\n')
    # Loop over output dictionary and write rows to output file
    for sample_id, file_dict in output_dict.items():
        merged_column = merge_files(file_dict)
        # Determine the value for the Sample_or_Control column
        sample_or_control = "True Sample"
        if sample_id.startswith(("C")):
            sample_or_control = "Control Sample"
        output_file.write(f'{sample_id}\t{merged_column}\t{sample_or_control}\n')
