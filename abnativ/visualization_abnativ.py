#!/usr/bin/env python3
"""
AbNatiV Results Analysis
Script for analyzing naturalness scores from AbNatiV CSV files
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

# where my AbNatiV results are stored
DATA_DIR = "./abnativ_results/"

# colors for the plots (similar to DeepLoc style)
colors = {
    'blue': '#2E86AB',
    'gold': '#FFAA00',
    'gray': '#708090'
}


def load_files():
    """load all CSV files from abnativ results directory"""
    pattern = os.path.join(DATA_DIR, "*.csv")
    files = glob.glob(pattern)

    if not files:
        print(f"No CSV files found in {DATA_DIR}")
        return None

    print(f"Loading {len(files)} AbNatiV result files...")

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


def analyze_scores(df):
    """analyze naturalness score distributions"""
    score_columns = [
        'AbNatiV VHH Score',
        'AbNatiV CDR1-VHH Score',
        'AbNatiV CDR2-VHH Score',
        'AbNatiV CDR3-VHH Score',
        'AbNatiV FR-VHH Score'
    ]

    results = {'total': len(df)}
    print(f"\nAnalyzing {len(df)} sequences...")

    for col in score_columns:
        if col in df.columns:
            values = df[col].dropna()
            stats = {
                'count': len(values),
                'mean': values.mean(),
                'median': values.median(),
                'std': values.std(),
                'min': values.min(),
                'max': values.max()
            }
            results[col] = stats
            print(f"  {col}: mean={stats['mean']:.3f}, range={stats['min']:.3f}-{stats['max']:.3f}")

    return results


def make_histogram_plot(df):
    """create distribution plots similar to DeepLoc style"""
    # score types to plot
    score_types = [
        'AbNatiV VHH Score',
        'AbNatiV CDR1-VHH Score',
        'AbNatiV CDR2-VHH Score',
        'AbNatiV CDR3-VHH Score',
        'AbNatiV FR-VHH Score'
    ]

    # short names for labels
    short_names = ['Overall', 'CDR1', 'CDR2', 'CDR3', 'Framework']

    # filter to available columns
    available_scores = []
    available_names = []
    for score, name in zip(score_types, short_names):
        if score in df.columns:
            available_scores.append(score)
            available_names.append(name)

    n_plots = len(available_scores)
    if n_plots == 0:
        print("No score columns found!")
        return None

    # create plots with more spacing since fewer plots
    fig, axes = plt.subplots(1, n_plots, figsize=(2.2 * n_plots, 6),
                             sharey=False, sharex=True)  # no shared y-axis
    fig.patch.set_facecolor('white')

    if n_plots == 1:
        axes = [axes]

    plt.subplots_adjust(wspace=0.1, bottom=0.2, top=0.88)  # more spacing

    for i, (score_col, short_name) in enumerate(zip(available_scores, available_names)):
        ax = axes[i]
        values = df[score_col].dropna()

        # for Overall score, color based on threshold
        if i == 0 and short_name == 'Overall':
            threshold = 0.8  # changed threshold
            # create histogram with threshold coloring
            n, bins, patches = ax.hist(values, bins=25, range=(0, 1),
                                       edgecolor='black', linewidth=0.5)

            # color bars based on threshold
            for j, (patch, bin_center) in enumerate(zip(patches, (bins[:-1] + bins[1:]) / 2)):
                if bin_center >= threshold:
                    patch.set_facecolor(colors['blue'])  # gold for above threshold (accepted)
                    patch.set_alpha(0.7)
                    # pass  # keep default color
                else:
                    patch.set_facecolor('#1D007F')  # dark blue for below threshold (not accepted)
                    patch.set_alpha(0.7)

            # add threshold line
            ax.axvline(threshold, color=colors['gold'], linewidth=2, alpha=0.5)
        else:
            # other plots just blue histograms
            n, bins, patches = ax.hist(values, bins=25, range=(0, 1),
                                       color=colors['blue'], alpha=0.7,
                                       edgecolor='black', linewidth=0.5)

        # formatting
        ax.set_xlim(0, 1)
        ax.set_xticks([0, 0.5, 1])  # changed to 0, 0.5, 1
        ax.set_xticklabels(['0', '0.5', '1'], fontsize=12)

        # add y-axis to each plot with y-label for first plot
        ax.tick_params(axis='y', colors='black', labelsize=8)
        if i == 0:
            ax.set_ylabel('Count', fontsize=14, fontweight='bold')

        # class label (no rotation)
        ax.text(0.5, -0.15, short_name, transform=ax.transAxes,
                ha='center', va='top', fontsize=12, fontweight='bold')

        # clean up spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('black')
        ax.spines['left'].set_linewidth(1)
        ax.grid(True, alpha=0.3, axis='y')

    # add legend to last plot
    if n_plots > 0:
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#1D007F', alpha=0.7, label='Below threshold'),  # dark blue
            Patch(facecolor=colors['blue'], alpha=0.7, label='Above threshold'),  # gold
            plt.Line2D([0], [0], color=colors['gold'], linewidth=2, alpha=0.5,
                       label='Threshold (0.8)')  # removed (0.5) from label
        ]
        axes[-1].legend(handles=legend_elements, loc='upper left', fontsize=11, framealpha=0.9)

    # labels (same style as DeepLoc)
    fig.text(0.5, 0.115, 'Naturalness Score', ha='center', fontsize=14, fontweight='bold')
    plt.suptitle('Distribution of AbNatiV Naturalness Scores', fontsize=18, fontweight='bold', y=0.95)

    return fig


def print_summary(results):
    """print summary to console"""
    print("\n" + "=" * 40)
    print("ABNATIV ANALYSIS SUMMARY")
    print("=" * 40)
    print(f"Total sequences: {results['total']}")

    print("\nNaturalness scores (mean ± std):")
    for col in results:
        if col != 'total' and isinstance(results[col], dict):
            stats = results[col]
            short_name = col.replace('AbNatiV ', '').replace('-VHH Score', '')
            print(f"  {short_name:12}: {stats['mean']:.3f} ± {stats['std']:.3f}")


if __name__ == "__main__":
    print("Starting AbNatiV analysis...")

    # load data
    df = load_files()
    if df is None:
        print("No data found. Exiting.")
        exit()

    # analyze
    results = analyze_scores(df)
    print_summary(results)

    # make plot
    print("\nCreating plot...")

    fig = make_histogram_plot(df)
    if fig:
        plt.savefig("abnativ_naturalness_distributions.png", dpi=300, bbox_inches='tight')
        print("Saved plot: abnativ_naturalness_distributions.png")
        plt.show()

    print("Visualization generated.")