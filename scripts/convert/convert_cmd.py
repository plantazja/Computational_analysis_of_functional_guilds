import argparse
import os
import re
import pandas as pd
from tqdm import tqdm

def parse_args():
    parser = argparse.ArgumentParser(description='Convert curatedMetagenomics output')
    parser.add_argument('-i', '--input_file', type=str, required=True, help='The input file')
    parser.add_argument('-o', '--output_dir', type=str, required=True, help='The output directory')
    parser.add_argument('-d', '--data_type', type=str, required=True, choices=['functions', 'genera'], help='Provide type of data - functional or taxonomical')
    parser.add_argument('--chunksize', type=int, default=2000, help='Number of rows to process at a time')
    parser.add_argument('--full_matrix', action='store_true', help='If flag, UNMAPPED and UNINTEGRATED will be included in the output matrix')
    return parser.parse_args()

def process_name(index_name, data_type):
    if data_type == 'genera':
        genus_match = re.search(r'g__([^|;]+)', index_name)
        processed_name = genus_match.group(1) if genus_match else 'unclassified'

    elif data_type == 'functions':
        # Original row name format is pathway_code:pathway_name and pathway_code:pathway_name|taxonomy
        # Rows with taxonomy are removed
        if '|' in index_name:
            return
        if index_name.startswith('UNMAPPED') or index_name.startswith('UNINTEGRATED'):
            processed_name = index_name  # Keep the original name for UNMAPPED and UNINTEGRATED
        else:
            processed_name = index_name.split(': ')[0]
    return processed_name


def write_to_matrix(input_path, output_path, data_type, chunksize, full_matrix):
    # Read the input file in chunks
    reader = pd.read_csv(input_path, sep='\t', header=0, index_col=0, chunksize=chunksize)
    
    # Initialize an empty DataFrame for accumulation
    accumulated_df = None
    indexcol_name = 'Genus' if data_type == 'genera' else 'Function'
    
    for chunk in tqdm(reader, desc="Processing chunks"):
        # Filter out UNMAPPED and UNINTEGRATED if full_matrix is False
        if not full_matrix:
            chunk = chunk[~chunk.index.str.contains('UNMAPPED|UNINTEGRATED', na=False)]
        
        # Process each row
        processed_rows = []
        processed_indices = []
        
        for idx in chunk.index:
            processed_name = process_name(idx, data_type)
            if processed_name is None:
                continue
            processed_indices.append(processed_name)
            processed_rows.append(chunk.loc[idx].values)
        
        # Create DataFrame from processed rows
        if processed_rows:
            chunk_df = pd.DataFrame(
                processed_rows,
                index=processed_indices,
                columns=chunk.columns
            )
            
            # Group by index (genus/function) and sum
            chunk_df = chunk_df.groupby(level=0).sum()
            
            # Accumulate with previous chunks
            if accumulated_df is None:
                accumulated_df = chunk_df
            else:
                # Align indices before adding
                accumulated_df = accumulated_df.add(chunk_df, fill_value=0)
    
    # Write the final result
    if accumulated_df is not None:
        # Sort index for consistent output
        accumulated_df = accumulated_df.sort_index()
        accumulated_df.to_csv(output_path, sep='\t')
    else:
        # Handle empty result
        pd.DataFrame().to_csv(output_path, sep='\t')
        print(f"Warning: No data processed. Empty file created at {output_path}")

def main():
    args = parse_args()
    output_filename = os.path.basename(args.input_file)

    write_to_matrix(args.input_file,
                    os.path.join(args.output_dir,
                                 output_filename),
                    args.data_type,
                    args.chunksize,
                    args.full_matrix)

if __name__ == '__main__':
    main()