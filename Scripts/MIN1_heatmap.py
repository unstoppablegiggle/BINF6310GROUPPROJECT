import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from Bio import pairwise2

# Define your amino acid order for indexing
AAorder = ['K', 'R', 'H', 'E', 'D', 'N', 'Q', 'T', 'S', 'C', 'G', 'A', 'V', 'L', 'I', 'M', 'P', 'Y', 'F', 'W']

def make_Ramp( ramp_colors ):
    from colour import Color
    from matplotlib.colors import LinearSegmentedColormap

    color_ramp = LinearSegmentedColormap.from_list( 'diff_cmap', [ Color( c1 ).rgb for c1 in ramp_colors ] )
    return color_ramp
# diff_cmap = make_Ramp( ['navy','royalblue','#8ce4fa','#faf18c','#fabc8c','#fa5534','red' ] ) ## yellow in center
diff_cmap = make_Ramp( ['navy','royalblue','#acebfa','white','#faf18c','#fa5534','red' ] )
# Load the data from the CSV file
def load_data(uniprot_id, filename='C:/Users/tophe/PycharmProjects/BINF6310/esm-variants/output/men1_llr_scores.csv'):
    data = pd.read_csv(filename)
    filtered_data = data[data['seq_id'].str.contains(uniprot_id)]

    # Process the data to get it into the required format (20xL DataFrame)
    llr_df = pd.DataFrame(index=AAorder, columns=sorted(
        set(filtered_data['mut_name'].apply(lambda x: int(''.join(filter(str.isdigit, x)))))))

    for _, row in filtered_data.iterrows():
        mut_name = row['mut_name']
        wt_aa, position, mutated_aa = mut_name[0], int(''.join(filter(str.isdigit, mut_name))), mut_name[-1]
        llr_df.at[mutated_aa, position] = row['esm_score']

    return llr_df.fillna(0)


# Function to calculate score differences
def calculate_score_difference(df1, df2):
    return df1.subtract(df2, fill_value=0)


# Function to plot the heatmaps
def plot_heatmaps(df1, df2, score_diff, title1, title2, diff_title):
    fig, axes = plt.subplots(3, 1, figsize=(20, 20), gridspec_kw={'height_ratios': [1, 1, 1]})

    sns.heatmap(df1, ax=axes[0], cmap='viridis_r', cbar_kws={'label': 'ESMb LLR score'})
    axes[0].set_title(title1)

    sns.heatmap(df2, ax=axes[1], cmap='viridis_r', cbar_kws={'label': 'ESMb LLR score'})
    axes[1].set_title(title2)

    sns.heatmap(score_diff, ax=axes[2], cmap=diff_cmap, center=0, cbar_kws={'label': 'Score difference'})
    axes[2].set_title(diff_title)

    for ax in axes:
        ax.set_xlabel('Residue position')

    plt.tight_layout()
    plt.show()


# Use the functions to load data, calculate differences, and plot
llr_data_1 = load_data('O00255-1')
llr_data_2 = load_data('O00255-2')
score_diff = calculate_score_difference(llr_data_1, llr_data_2)

plot_heatmaps(llr_data_1, llr_data_2, score_diff, 'Primary isoform (O00255-1)', 'Isoform-2 (O00255-2)',
              'Score difference')
print(llr_data_1.head)
