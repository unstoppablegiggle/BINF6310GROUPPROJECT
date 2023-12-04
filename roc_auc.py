import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_auc_score

benchmark_dataset = pd.read_csv('final_updated_file_two.csv')
benchmark_dataset['esm_score'] = -benchmark_dataset['esm_score']
benchmark_dataset = benchmark_dataset.dropna(subset=['esm_score'])
benchmark_dataset['clinvar_hq_label'] = benchmark_dataset['clinvar_label'].where(benchmark_dataset['Gold_Stars'] >= 1)
print(benchmark_dataset)


def set_ax_border_color(ax, color):
    """
    Set the border color of the given axis.

    Parameters:
    - ax: The axis to set the border color for.
    - color: The color to set for the border.
    """
    for spine in ax.spines.values():
        spine.set_edgecolor(color)


def get_benchmark_results(benchmark_name, dataset, benchmark_label, score):
    global_auc = roc_auc_score(dataset[benchmark_label], dataset[score])
    avg_gene_auc = np.mean([roc_auc_score(gene_variants[benchmark_label], gene_variants[score]) for \
                            _, gene_variants in dataset.groupby('uniprot_isoform_id') if
                            set(gene_variants[benchmark_label]) == \
                            {0.0, 1.0}])
    return benchmark_name, len(dataset), int(dataset[benchmark_label].sum()), \
        len(dataset['uniprot_isoform_id'].unique()), score, global_auc, avg_gene_auc


benchmark_results = []

for benchmark_label in ['clinvar_hq_label']:

    label_dataset = benchmark_dataset.dropna(subset=[benchmark_label, 'EVE_scores_ASM'])

    for score in ['EVE_scores_ASM', 'esm_score']:
        benchmark_results.append(get_benchmark_results('%s - all' % benchmark_label, label_dataset, benchmark_label,
                                                       score))
        benchmark_results.append(get_benchmark_results('%s - short sequences (<= 1022 aa)' % benchmark_label, \
                                                       label_dataset[label_dataset['seq_len'] <= 1022], benchmark_label,
                                                       score))
        benchmark_results.append(get_benchmark_results('%s - long sequences (> 1022 aa)' % benchmark_label, \
                                                       label_dataset[label_dataset['seq_len'] > 1022], benchmark_label,
                                                       score))

benchmark_results = pd.DataFrame(benchmark_results, columns=['benchmark', 'n_variants', 'n_positive_variants', \
                                                             'n_genes', 'score', 'global_auc', 'avg_gene_auc'])
print(benchmark_results)


BENCHMARKS = ['clinvar_hq_label - all']

fig, ax = plt.subplots(figsize=(15, 10))

bar_width = 0.3  # Adjust the width of the bars
bar_spacing = 0.2  # Adjust the spacing between bars

x = 2 * np.arange(len(BENCHMARKS))

# EVE_scores_ASM
y1 = benchmark_results[benchmark_results['score'] == 'EVE_scores_ASM'].set_index('benchmark') \
    .loc[BENCHMARKS, 'global_auc']
ax.bar(x - bar_spacing, y1, label='EVE', color='#17A589', width=bar_width)

# esm_score
y2 = benchmark_results[benchmark_results['score'] == 'esm_score'].set_index('benchmark') \
    .loc[BENCHMARKS, 'global_auc']
ax.bar(x + bar_spacing, y2, label='ESM1b', color='#9B59B6', width=bar_width)

ax.set_xticks(x)
ax.set_xticklabels(['ClinVar'], fontsize=45)

ax.set_ylim((0.8, 0.95))
ax.set_ylabel('ROC-AUC', fontsize=45)
ax.tick_params(axis='y', which='major', labelsize=30)

ax.legend(loc='lower right', fontsize=45)
set_ax_border_color(ax, '#aaaaaa')
plt.savefig('roc_auc')

