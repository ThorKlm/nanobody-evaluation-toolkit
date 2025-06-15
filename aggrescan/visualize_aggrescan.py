#!/usr/bin/env python3
"""
Visualize AGGRESCAN results from text files
"""

import os
import glob
import matplotlib.pyplot as plt
import numpy as np
import re

colors = {
    'blue': '#2E86AB',
    'orange': '#FF8C00',
    'red': '#DC143C'
}


def load_aggrescan_files():
    """Load all AGGRESCAN result text files"""
    pattern = "batch_*_aggrescan_results.txt"
    files = glob.glob(pattern)

    if not files:
        print("No AGGRESCAN result files found")
        return None

    print(f"Loading {len(files)} AGGRESCAN result files...")

    all_na4vss = []

    for file in sorted(files):
        try:
            with open(file, 'r') as f:
                content = f.read()

            # Find "Sorted by Na4vSS" section
            sorted_pattern = r'Sorted by Na4vSS\s+(.*?)(?:\n\n|\Z)'
            sorted_match = re.search(sorted_pattern, content, re.DOTALL)

            if sorted_match:
                sorted_section = sorted_match.group(1)
                # Extract Na4vSS values
                value_pattern = r'[\w_]+\s+([-\d.]+)'
                values = re.findall(value_pattern, sorted_section)

                for val in values:
                    try:
                        all_na4vss.append(float(val))
                    except:
                        pass

            print(f"  - {file}: {len(values) if 'values' in locals() else 0} sequences")

        except Exception as e:
            print(f"Error loading {file}: {e}")

    if all_na4vss:
        print(f"Total: {len(all_na4vss)} sequences loaded")
        return np.array(all_na4vss)
    return None


def analyze_scores(na4vss_values):
    """Analyze Na4vSS score distribution"""
    stats = {
        'count': len(na4vss_values),
        'mean': na4vss_values.mean(),
        'median': np.median(na4vss_values),
        'std': na4vss_values.std(),
        'min': na4vss_values.min(),
        'max': na4vss_values.max()
    }

    print(f"\nNa4vSS Analysis:")
    print(f"  Total sequences: {stats['count']}")
    print(f"  Mean: {stats['mean']:.2f}")
    print(f"  Median: {stats['median']:.2f}")
    print(f"  Range: {stats['min']:.2f} - {stats['max']:.2f}")

    return stats


def make_histogram_plot(na4vss_values, stats):
    """Create histogram of Na4vSS values"""
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor('white')

    # Histogram with threshold coloring
    threshold = 0.0  # Na4vSS threshold (negative = good)

    n, bins, patches = ax.hist(na4vss_values, bins=30, edgecolor='black', linewidth=0.5)

    # Color bars based on thresholds
    for patch, bin_center in zip(patches, (bins[:-1] + bins[1:]) / 2):
        if bin_center < 0:
            patch.set_facecolor(colors['blue'])  # Good: light blue
            patch.set_alpha(0.7)
        elif bin_center < 5:
            patch.set_facecolor('#1D007F')  # Poor: dark blue
            patch.set_alpha(0.7)
        else:
            patch.set_facecolor('#0A0040')  # Very poor: very dark blue
            patch.set_alpha(0.7)

    # Add statistics lines
    ax.axvline(stats['mean'], color=colors['orange'], linewidth=2,
               linestyle='--', label=f'Mean: {stats["mean"]:.1f}')
    ax.axvline(stats['median'], color='gold', linewidth=2,
               linestyle='-', label=f'Median: {stats["median"]:.1f}')
    ax.axvline(threshold, color='black', linewidth=2, alpha=0.7,
               linestyle=':', label='Threshold (0.0)')

    ax.set_xlabel('Na4vSS Score', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    ax.set_title(f'AGGRESCAN Na4vSS Distribution (N samples ={stats["count"]})',
                 fontsize=14, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, axis='y')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    return fig


def print_summary(stats, na4vss_values):
    """Print summary statistics"""
    print("\n" + "=" * 40)
    print("AGGRESCAN ANALYSIS SUMMARY")
    print("=" * 40)
    print(f"Total sequences: {stats['count']}")
    print(f"Mean Na4vSS: {stats['mean']:.2f} ± {stats['std']:.2f}")
    print(f"Range: {stats['min']:.2f} - {stats['max']:.2f}")

    # Quality categories
    good = (na4vss_values < 0).sum()
    poor = (na4vss_values >= 0).sum()

    print(f"\nAggregation Risk Categories:")
    print(f"  Low risk (Na4vSS < 0): {good} ({good / len(na4vss_values) * 100:.1f}%)")
    print(f"  High risk (Na4vSS ≥ 0): {poor} ({poor / len(na4vss_values) * 100:.1f}%)")


def main():
    """Main function"""
    print("Starting AGGRESCAN visualization...")

    # Load data
    na4vss_values = load_aggrescan_files()
    if na4vss_values is None:
        return

    # Analyze
    stats = analyze_scores(na4vss_values)
    print_summary(stats, na4vss_values)

    # Visualize
    print("\nCreating plot...")
    fig = make_histogram_plot(na4vss_values, stats)
    plt.savefig("aggrescan_na4vss_distribution.png", dpi=300, bbox_inches='tight')
    print("Saved plot: aggrescan_na4vss_distribution.png")
    plt.show()


if __name__ == "__main__":
    main()