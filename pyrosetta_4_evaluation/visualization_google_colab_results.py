import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def load_rosetta_results(raw_file, stats_file):
    """Load Rosetta multi-seed results"""
    df_raw = pd.read_csv(raw_file)
    df_stats = pd.read_csv(stats_file)
    return df_raw, df_stats

def create_rosetta_binding_matrix_visualization(df_stats, score_column='binding_energy_mean',
                                               std_column='binding_energy_std',
                                               title_suffix='Rosetta Binding Energy Multi-Seed'):
    """Create Rosetta binding matrix visualization matching AlphaFold format"""

    if len(df_stats) == 0:
        print("No data to plot")
        return None

    # Sort names alphabetically
    nanobodies = sorted(df_stats['nanobody'].unique(), key=str.lower)
    antigens = sorted(df_stats['antigen'].unique(), key=str.lower)

    # Create pivot tables
    df_clean = df_stats.drop_duplicates(subset=['nanobody', 'antigen'], keep='first')

    mean_matrix = df_clean.pivot(index='nanobody', columns='antigen', values=score_column)
    mean_matrix = mean_matrix.reindex(index=nanobodies, columns=antigens)

    std_matrix = df_clean.pivot(index='nanobody', columns='antigen', values=std_column)
    std_matrix = std_matrix.reindex(index=nanobodies, columns=antigens)

    count_matrix = df_clean.pivot(index='nanobody', columns='antigen', values=score_column.replace('_mean', '_count'))
    count_matrix = count_matrix.reindex(index=nanobodies, columns=antigens)

    # Create plot
    plt.figure(figsize=(16, 14))

    # Use RdBu_r colormap (red=bad/positive, blue=good/negative for binding energy)
    cmap = 'RdBu_r'

    # Create annotation labels with mean ± std
    annot_labels = mean_matrix.round(1).astype(str) + '\n+/-' + std_matrix.round(1).astype(str)

    # Add seed count for low-count combinations
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
       cmap=cmap,
       center=0,  # Center colormap at 0
       square=True,
       linewidths=0.5,
       cbar_kws={'label': f'{title_suffix} (REU)'},
       annot_kws={'size': 14}
    )

    # Colorbar formatting
    cbar = ax.collections[0].colorbar
    cbar.set_label(f'{title_suffix} (REU)', size=20)

    # Highlight diagonal (expected binding pairs)
    for i in range(min(len(nanobodies), len(antigens))):
        ax.add_patch(plt.Rectangle((i, i), 1, 1, fill=False, edgecolor='red', lw=5))

    plt.title(f'Nanobody-Antigen Binding Matrix ({title_suffix})', fontsize=22, pad=20)
    plt.xlabel('Antigens', fontsize=22)
    plt.ylabel('Nanobodies', fontsize=22)
    plt.xticks(rotation=45, ha='right', fontsize=18)
    plt.yticks(rotation=0, fontsize=18)
    plt.tight_layout()

    # Save with descriptive filename
    plt.savefig("binding_matrix_rosetta_multiseed.png", dpi=300, bbox_inches='tight')
    plt.show()

    return mean_matrix, std_matrix

def analyze_rosetta_multiseed_results(df_raw, df_stats):
    """Analyze Rosetta multi-seed results matching AlphaFold format"""
    print("=== Rosetta Multi-Seed Results Analysis ===")
    print()

    if len(df_raw) == 0:
        print("ERROR: No data found")
        return

    # Basic statistics
    df_successful = df_raw[df_raw['success'] == True]
    n_seeds_max = 10  # Target seeds per combination
    n_combinations = len(df_stats)

    print(f"Total experiments: {len(df_raw)}")
    print(f"Successful experiments: {len(df_successful)}")
    print(f"Overall success rate: {len(df_successful)/len(df_raw)*100:.1f}%")
    print(f"Unique nanobody-antigen combinations: {n_combinations}")
    print(f"Number of nanobodies: {df_stats['nanobody'].nunique()}")
    print(f"Number of antigens: {df_stats['antigen'].nunique()}")
    print()

    # Show completeness
    complete_combinations = (df_stats['binding_energy_count'] == n_seeds_max).sum()
    print(f"Combinations with all {n_seeds_max} seeds: {complete_combinations}/{n_combinations}")

    # Seed count distribution
    seed_counts = df_stats['binding_energy_count'].value_counts().sort_index()
    print("Seed count distribution:")
    for count, freq in seed_counts.items():
        print(f"  {int(count)} seeds: {freq} combinations")
    print()

    # Quality metrics
    strong_binders = (df_stats['binding_energy_mean'] < -5).sum()
    moderate_binders = ((df_stats['binding_energy_mean'] >= -5) &
                       (df_stats['binding_energy_mean'] < -1)).sum()
    weak_binders = (df_stats['binding_energy_mean'] >= -1).sum()

    print("Binding strength distribution (based on mean energy):")
    print(f"  Strong binders (<-5 REU): {strong_binders}/{n_combinations}")
    print(f"  Moderate binders (-5 to -1 REU): {moderate_binders}/{n_combinations}")
    print(f"  Weak binders (>-1 REU): {weak_binders}/{n_combinations}")
    print()

    # Top binding pairs
    print("Top 5 binding pairs (most negative mean binding energy):")
    top_pairs = df_stats.nsmallest(5, 'binding_energy_mean')
    for _, row in top_pairs.iterrows():
        strength = "strong" if row['binding_energy_mean'] < -5 else "moderate" if row['binding_energy_mean'] < -1 else "weak"
        print(f"  {strength:8s} {row['nanobody']} + {row['antigen']}: "
              f"{row['binding_energy_mean']:.1f}+/-{row['binding_energy_std']:.1f} REU "
              f"(n={int(row['binding_energy_count'])})")
    print()

    # Check diagonal matches (expected pairs)
    diagonal_pairs = []
    for _, row in df_stats.iterrows():
        nb_clean = row['nanobody'].replace('nb', '').split('_')[0].upper()
        ag_clean = row['antigen'].upper()
        if nb_clean == ag_clean:
            diagonal_pairs.append(row)

    if diagonal_pairs:
        print("Expected binding pairs (diagonal matches):")
        for _, pair in pd.DataFrame(diagonal_pairs).iterrows():
            strength = "strong" if pair['binding_energy_mean'] < -5 else "moderate" if pair['binding_energy_mean'] < -1 else "weak"
            print(f"  {strength:8s} {pair['nanobody']} + {pair['antigen']}: "
                  f"{pair['binding_energy_mean']:.1f}+/-{pair['binding_energy_std']:.1f} REU "
                  f"(n={int(pair['binding_energy_count'])})")
        print()

    # Summary statistics
    print("Summary statistics (successful runs only):")
    print(f"  Binding Energy - Mean: {df_successful['binding_energy'].mean():.1f} "
          f"Std: {df_successful['binding_energy'].std():.1f} "
          f"Range: {df_successful['binding_energy'].min():.1f} to {df_successful['binding_energy'].max():.1f} REU")
    print(f"  Interface Area - Mean: {df_successful['interface_area'].mean():.1f} "
          f"Std: {df_successful['interface_area'].std():.1f} Ų")
    print(f"  Interface Residues - Mean: {df_successful['interface_residues'].mean():.1f} "
          f"Std: {df_successful['interface_residues'].std():.1f}")

# Main execution
if __name__ == "__main__":
    print("=== Loading Rosetta Multi-Seed Results ===")

    # Load data
    try:
        df_raw, df_stats = load_rosetta_results(
            "results/rosetta_multiseed_raw_results.csv",
            "results/rosetta_multiseed_statistics.csv"
        )

        print(f"Loaded {len(df_raw)} raw experiments")
        print(f"Loaded {len(df_stats)} combination statistics")
        print()

        # Create visualization
        print("Creating binding matrix visualization...")
        mean_matrix, std_matrix = create_rosetta_binding_matrix_visualization(
            df_stats, 'binding_energy_mean', 'binding_energy_std'
        )

        # Analyze results
        analyze_rosetta_multiseed_results(df_raw, df_stats)

        # Save additional outputs
        if mean_matrix is not None:
            mean_matrix.to_csv('results/rosetta_binding_matrix_mean.csv')
            std_matrix.to_csv('results/rosetta_binding_matrix_std.csv')

        print()
        print("=== Files Saved ===")
        print("binding_matrix_rosetta_multiseed.png - Visualization")
        print("results/rosetta_binding_matrix_mean.csv - Mean binding matrix")
        print("results/rosetta_binding_matrix_std.csv - Std deviation matrix")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Make sure to run the multi-seed experiment first!")

    print("Analysis complete!")