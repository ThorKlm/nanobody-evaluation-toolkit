#!/usr/bin/env python3
"""
NanoMelt Results Analysis
Script for analyzing thermostability predictions from NanoMelt CSV files
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os

# where the NanoMelt results are stored
DATA_DIR = "./nanomelt_results/"

# colors for plots (copied from DeepLoc script)
colors = {
    'blue': '#2E86AB',
    'orange': '#FF8C00',
    'gray': '#708090',
    'darkgray': '#2F2F2F'
}


def load_files():  # renamed from load_nanomelt_files to be shorter
    """load all CSV files from nanomelt results directory"""
    pattern = os.path.join(DATA_DIR, "*.csv")
    files = glob.glob(pattern)

    if not files:
        print(f"No CSV files found in {DATA_DIR}")
        return None

    print(f"Loading {len(files)} NanoMelt result files...")

    all_data = []
    for i, file in enumerate(sorted(files)):
        try:
            df = pd.read_csv(file)
            df['file_number'] = i + 1  # probably don't need this but keeping it
            all_data.append(df)
            print(f"  - {os.path.basename(file)}: {len(df)} sequences")
        except Exception as e:
            print(f"Error loading {file}: {e}")

    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        print(f"Total: {len(combined)} sequences loaded")
        return combined
    return None


def analyze_data(df):  # simplified name
    """analyze melting temperature distribution"""
    tm_values = df['NanoMelt Tm (C)'].dropna()

    stats = {
        'count': len(tm_values),
        'mean': tm_values.mean(),
        'median': tm_values.median(),
        'std': tm_values.std(),
        'min': tm_values.min(),
        'max': tm_values.max(),
        'q25': tm_values.quantile(0.25),
        'q75': tm_values.quantile(0.75)
    }

    print(f"\nMelting Temperature Analysis:")
    print(f"  Total sequences: {stats['count']}")
    print(f"  Mean Tm: {stats['mean']:.1f}°C")
    print(f"  Median Tm: {stats['median']:.1f}°C")
    print(f"  Range: {stats['min']:.1f} - {stats['max']:.1f}°C")

    return stats, tm_values


def make_plot(tm_values, stats):
    """create histogram of melting temperatures"""
    fig, ax = plt.subplots(figsize=(10, 6))  # made it wider
    fig.patch.set_facecolor('white')

    # histogram
    n, bins, patches = ax.hist(tm_values, bins=25, color=colors['blue'],
                               alpha=0.7, edgecolor='black', linewidth=0.5)

    # add mean and median lines
    ax.axvline(stats['mean'], color=colors['orange'], linewidth=2,
               linestyle='--', label=f'Mean: {stats["mean"]:.1f}°C')
    ax.axvline(stats['median'], color='gold', linewidth=2,
               linestyle='-', label=f'Median: {stats["median"]:.1f}°C')

    ax.set_xlabel('Melting Temperature (°C)', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_title('NanoMelt Melting Temperature Distribution\n' + f'n={stats["count"]}',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    return fig


# def categorize_stability(tm_values):
#     """categorize sequences by thermal stability"""
#     # rough stability categories based on typical protein Tm values
#     low_stable = (tm_values < 60).sum()
#     moderate_stable = ((tm_values >= 60) & (tm_values < 70)).sum()
#     high_stable = (tm_values >= 70).sum()
#
#     categories = {
#         'Low (<60°C)': low_stable,
#         'Moderate (60-70°C)': moderate_stable,
#         'High (≥70°C)': high_stable
#     }
#
#     return categories

# def make_stability_plot(categories):
#     """pie chart of stability categories"""
#     # commented out - only want the main distribution plot
#     pass

def print_summary(stats):
    """print summary to console"""
    print("\n" + "=" * 40)  # made shorter
    print("ANALYSIS SUMMARY")
    print("=" * 40)
    print(f"Total sequences: {stats['count']}")
    print(f"Average Tm: {stats['mean']:.1f} ± {stats['std']:.1f}°C")
    print(f"Range: {stats['min']:.1f} - {stats['max']:.1f}°C")


if __name__ == "__main__":
    print("Starting analysis...")

    # load data
    df = load_files()
    if df is None:
        print("No data found. Exiting.")
        exit()

    # analyze
    stats, tm_values = analyze_data(df)
    print_summary(stats)

    # categories = categorize_stability(tm_values)  # don't need this anymore

    # make plot
    print("\nCreating plot...")

    fig = make_plot(tm_values, stats)
    plt.savefig("nanomelt_temperature_distribution.png", dpi=300, bbox_inches='tight')

    print("Saved plot: nanomelt_temperature_distribution.png")

    plt.show()
    print("Visualization finished.")