#!/usr/bin/env python3
"""
Nanobody DeepLoc Results Analysis
Script for analyzing subcellular localization predictions from batch CSV files
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

# where my DeepLoc results are stored
DATA_DIR = "./deep_loc_evaluation_results/"

# thresholds from the DeepLoc website
thresholds = {
    'Cytoplasm': 0.4761,
    'Nucleus': 0.5014,
    'Extracellular': 0.6173,
    'Cell membrane': 0.5646,
    'Mitochondrion': 0.6220,
    'Plastid': 0.6395,
    'Endoplasmic reticulum': 0.6090,
    'Lysosome/Vacuole': 0.5848,
    'Golgi apparatus': 0.6494,
    'Peroxisome': 0.7364,
    'Peripheral': 0.60,
    'Transmembrane': 0.51,
    'Lipid anchor': 0.82,
    'Soluble': 0.50
}

# colors for the plots
colors = {
    'blue': '#2E86AB',
    'gold': '#FFAA00',
    'gray': '#708090',
    'darkgray': '#2F2F2F'
}


def load_files():
    """load all batch CSV files"""
    pattern = os.path.join(DATA_DIR, "batch_*_deeploc_2_1.csv")
    files = glob.glob(pattern)

    if not files:
        print(f"No files found in {DATA_DIR}")
        return None

    print(f"Loading {len(files)} batch files...")

    all_data = []
    for i, file in enumerate(sorted(files)):
        try:
            df = pd.read_csv(file)
            df['batch'] = i + 1
            all_data.append(df)
            print(f"  - {os.path.basename(file)}: {len(df)} sequences")
        except Exception as e:
            print(f"Error loading {file}: {e}")

    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        print(f"Total: {len(combined)} sequences loaded")
        return combined
    return None


def analyze_data(df):
    """count sequences above thresholds"""
    total = len(df)
    results = {'total': total, 'localizations': {}}

    print(f"\nAnalyzing {total} sequences...")

    for location, threshold in thresholds.items():
        if location in df.columns:
            above_thresh = (df[location] >= threshold).sum()
            percent = (above_thresh / total) * 100
            results['localizations'][location] = {
                'count': above_thresh,
                'percent': percent,
                'threshold': threshold
            }
            print(f"  {location}: {above_thresh} sequences ({percent:.1f}%)")

    return results


def save_interesting_sequences(df):
    """save non-extracellular sequences for further analysis"""
    extracellular_thresh = thresholds['Extracellular']
    non_extracellular = df[df['Extracellular'] < extracellular_thresh]

    print(f"\nFound {len(non_extracellular)} sequences below extracellular threshold")

    if len(non_extracellular) > 0:
        non_extracellular.to_csv("non_extracellular_sequences.csv", index=False)
        print("Saved to: non_extracellular_sequences.csv")

    # also save sequences predicted for other locations
    other_predictions = []
    for loc, thresh in thresholds.items():
        if loc != 'Extracellular' and loc in df.columns:
            predicted = df[df[loc] >= thresh]
            if len(predicted) > 0:
                predicted = predicted.copy()
                predicted['predicted_location'] = loc
                other_predictions.append(predicted)

    if other_predictions:
        alt_predictions = pd.concat(other_predictions, ignore_index=True)
        alt_predictions.to_csv("alternative_predictions.csv", index=False)
        print(f"Saved {len(alt_predictions)} alternative predictions")


def make_bar_plot(results):
    """simple bar plot for publication"""
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.patch.set_facecolor('white')

    locations = list(results['localizations'].keys())
    counts = [results['localizations'][loc]['count'] for loc in locations]
    percentages = [results['localizations'][loc]['percent'] for loc in locations]

    bars = ax.bar(range(len(locations)), counts, color=colors['blue'],
                  alpha=0.7, edgecolor='black', linewidth=0.8)

    # add percentage labels
    for bar, pct in zip(bars, percentages):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height + max(counts) * 0.01,
                f'{pct:.1f}%', ha='center', va='bottom', fontsize=9)

    ax.set_title(f'Subcellular Localization Predictions (n={results["total"]})',
                 fontsize=14, fontweight='bold')
    ax.set_ylabel('Number of Sequences', fontsize=12)
    ax.set_xlabel('Predicted Localization', fontsize=12)
    ax.set_xticks(range(len(locations)))
    ax.set_xticklabels([loc.replace(' ', '\n') for loc in locations],
                       rotation=45, ha='right', fontsize=9)

    # clean up the plot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    return fig


def make_histogram_plot(df):
    """histograms showing distribution of scores with thresholds"""
    # all the localization types
    all_locs = ['Cytoplasm', 'Nucleus', 'Extracellular', 'Cell membrane',
                'Mitochondrion', 'Plastid', 'Endoplasmic reticulum', 'Lysosome/Vacuole',
                'Golgi apparatus', 'Peroxisome', 'Peripheral', 'Transmembrane',
                'Lipid anchor', 'Soluble']

    # only use ones that exist in the data
    available = [loc for loc in all_locs if loc in df.columns]
    n_plots = len(available)

    fig, axes = plt.subplots(1, n_plots, figsize=(1.5 * n_plots, 6),
                             sharey=True, sharex=True)
    fig.patch.set_facecolor('white')

    if n_plots == 1:
        axes = [axes]

    plt.subplots_adjust(wspace=0.02, bottom=0.2, top=0.88)

    for i, location in enumerate(available):
        ax = axes[i]
        values = df[location].values
        thresh = thresholds[location]

        # create histogram with colored bars based on threshold
        n, bins, patches = ax.hist(values, bins=30, range=(0, 1),
                                   edgecolor='black', linewidth=0.5)

        # color bars: blue below threshold, orange above
        for j, (patch, bin_center) in enumerate(zip(patches, (bins[:-1] + bins[1:]) / 2)):
            if bin_center >= thresh:
                patch.set_facecolor('#FF8C00')  # orange for above threshold
                patch.set_alpha(0.7)
            else:
                patch.set_facecolor(colors['blue'])  # blue for below threshold
                patch.set_alpha(0.7)

        # add legend labels to last plot
        if i == n_plots - 1:
            # create dummy patches for legend
            from matplotlib.patches import Patch
            legend_elements = [
                Patch(facecolor=colors['blue'], alpha=0.7, label='Below threshold'),
                Patch(facecolor='#FF8C00', alpha=0.7, label='Above threshold'),
                plt.Line2D([0], [0], color=colors['gold'], linewidth=2, alpha=0.5,
                           label='Class specific\nthreshold')
            ]
            ax.legend(handles=legend_elements, loc='upper right', fontsize=12, framealpha=0.9)

        # threshold line
        ax.axvline(thresh, color=colors['gold'], linewidth=2, alpha=0.5)

        # reference line at zero (except first plot)
        if i > 0:
            ax.axvline(0, color='black', linewidth=2, alpha=0.25)

        # formatting
        ax.set_xlim(0, 1)
        ax.set_xticks([0.0, 0.25, 0.5])
        ax.set_xticklabels(['0.0', '0.25', '0.5'], fontsize=12)

        if i == 0:
            ax.set_ylabel('Count', fontsize=14, fontweight='bold')
        else:
            ax.tick_params(axis='y', left=False)

        # class label
        class_name = location.replace('Endoplasmic reticulum', 'Endoplasmic\nreticulum')
        ax.text(0.5, -0.15, class_name, transform=ax.transAxes,
                ha='center', va='top', fontsize=12, fontweight='bold', rotation=-15)

        # clean up
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        if i > 0:
            ax.spines['left'].set_visible(False)
        ax.grid(True, alpha=0.3, axis='y')

    # labels
    fig.text(0.5, 0.115, 'Prediction Score', ha='center', fontsize=14, fontweight='bold')
    plt.suptitle('Distribution of Predicted Scores', fontsize=18, fontweight='bold', y=0.95)

    return fig


def print_results(results):
    """print summary to console"""
    print("\n" + "=" * 40)
    print("RESULTS SUMMARY")
    print("=" * 40)
    print(f"Total sequences: {results['total']}")
    print("\nLocalizations above threshold:")

    for loc, data in results['localizations'].items():
        print(f"  {loc:20} {data['count']:4d} ({data['percent']:5.1f}%)")


if __name__ == "__main__":
    print("Starting analysis...")

    # load data
    df = load_files()
    if df is None:
        print("No data found. Exiting.")
        exit()

    # analyze
    results = analyze_data(df)
    print_results(results)

    # save interesting sequences
    save_interesting_sequences(df)

    # make plots
    print("\nCreating plots...")

    fig1 = make_bar_plot(results)
    plt.savefig("localization_summary.png", dpi=300, bbox_inches='tight')

    fig2 = make_histogram_plot(df)
    plt.savefig("score_distributions.png", dpi=300, bbox_inches='tight')

    print("Saved plots:")
    print("  - localization_summary.png")
    print("  - score_distributions.png")

    plt.show()
    print("Visualizations Completed.")