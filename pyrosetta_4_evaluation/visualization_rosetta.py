import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# load data
df_stats = pd.read_csv('rosetta_multiseed_statistics.csv')

# sort names
nanobodies = sorted(df_stats['nanobody'].unique(), key=str.lower)
antigens = sorted(df_stats['antigen'].unique(), key=str.lower)

# create matrices
mean_matrix = df_stats.pivot(index='nanobody', columns='antigen', values='binding_energy_mean')
mean_matrix = mean_matrix.reindex(index=nanobodies, columns=antigens)

std_matrix = df_stats.pivot(index='nanobody', columns='antigen', values='binding_energy_std')
std_matrix = std_matrix.reindex(index=nanobodies, columns=antigens)

count_matrix = df_stats.pivot(index='nanobody', columns='antigen', values='binding_energy_count')
count_matrix = count_matrix.reindex(index=nanobodies, columns=antigens)

# plot
plt.figure(figsize=(16, 14))

# annotations with mean +/- std
annot_labels = mean_matrix.round(3).astype(str) + '\n+/-' + std_matrix.round(3).astype(str)

# add count if < 10
for i in range(len(nanobodies)):
    for j in range(len(antigens)):
        if not pd.isna(count_matrix.iloc[i, j]) and count_matrix.iloc[i, j] < 10:
            current_label = annot_labels.iloc[i, j]
            seed_count = int(count_matrix.iloc[i, j])
            annot_labels.iloc[i, j] = f"{current_label}\n(n={seed_count})"

ax = sns.heatmap(
    mean_matrix,
    annot=annot_labels,
    fmt='',
    cmap='viridis',
    square=True,
    linewidths=0.5,
    cbar_kws={'label': 'PyRosetta-4 IgFold Binding Energy (REU)'},
    annot_kws={'size': 14}
)

# colorbar
cbar = ax.collections[0].colorbar
cbar.set_label('PyRosetta-4 IgFold Binding Energy (REU)', size=20)

# highlight diagonal
for i in range(min(len(nanobodies), len(antigens))):
    ax.add_patch(plt.Rectangle((i, i), 1, 1, fill=False, edgecolor='red', lw=5))

plt.title('Nanobody-Antigen Binding Matrix (PyRosetta-4 IgFold, N=10 seeds)', fontsize=22, pad=20)
plt.xlabel('Antigens', fontsize=22)
plt.ylabel('Nanobodies', fontsize=22)
plt.xticks(rotation=45, ha='right', fontsize=18)
plt.yticks(rotation=0, fontsize=18)
plt.tight_layout()

plt.savefig("binding_matrix_pyrosetta4_igfold.png", dpi=300, bbox_inches='tight')
plt.show()