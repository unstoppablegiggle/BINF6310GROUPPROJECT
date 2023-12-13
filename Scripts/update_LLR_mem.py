import pandas as pd

# File paths
large_file_path = 'uniprot_llr.csv'
small_file_path = 'benchmark_with_tiled_scores.csv'
final_output_path = 'final_updated_file.csv'
chunk_size = 100000  # Adjust based on your system's memory

# load tiled scores into dataframe
small_df = pd.read_csv(small_file_path)

# Initialize new column
small_df['esm_score'] = pd.NA


def update_llr(chunk, small_df):
    """
    This function adds a new esm LLR score to the dataframe
    if there is a match for Uniprot Isoform id AND aa_change
    @param
    @param
    @Returns NONE

    """
    # Merge with the current chunk
    merged = pd.merge(small_df, chunk, how='left',
                      left_on=['uniprot_isoform_id', 'aa_change'],
                      right_on=['seq_id', 'mut_name'])

    # Ensure esm_score column is present in merged DataFrame
    if 'esm_score' not in merged:
        merged['esm_score'] = pd.NA

    # Update the esm_score column only where there's a match
    small_df['esm_score'].update(merged['esm_score'])

# Process the large file in chunks
for chunk in pd.read_csv(large_file_path, chunksize=chunk_size):
    update_llr(chunk, small_df)

# Write the updated DataFrame to a new CSV file
small_df.to_csv(final_output_path, index=False)

