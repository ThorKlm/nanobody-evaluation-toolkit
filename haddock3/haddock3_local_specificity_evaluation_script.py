"""
HADDOCK3 Matrix Screening Pipeline/ Specificity evaluation script
Automatically runs all nanobody-antigen combinations and generates results matrix
"""

import os
import glob
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import time
import concurrent.futures
from typing import List, Tuple, Dict


class HADDOCK3MatrixScreening:
    def __init__(self, structures_dir: str, output_dir: str = "haddock3_matrix_results"):
        """
        Initialize the matrix screening pipeline

        Args:
            structures_dir: Directory containing nanobody*.pdb and antigen*.pdb files
            output_dir: Directory to store all results
        """
        self.structures_dir = Path(structures_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Find all nanobody and antigen structures
        self.nanobodies = sorted(glob.glob(str(self.structures_dir / "nanobody*.pdb")))
        self.antigens = sorted(glob.glob(str(self.structures_dir / "antigen*.pdb")))

        print(f"Found {len(self.nanobodies)} nanobodies and {len(self.antigens)} antigens")
        print(f"Total combinations: {len(self.nanobodies) * len(self.antigens)}")

        # Initialize results storage
        self.results_matrix = None
        self.detailed_results = []

    def create_haddock_config(self, nanobody_path: str, antigen_path: str, run_name: str) -> str:
        """Create HADDOCK3 configuration file for a specific pair"""
        config_content = f"""run_dir = "{run_name}"

molecules = [
    "{nanobody_path}",
    "{antigen_path}"
]

[topoaa]

[rigidbody]
sampling = 100

[flexref]
sampling_factor = 3

[clustfcc]
min_population = 10

[caprieval]
"""
        config_path = self.output_dir / f"{run_name}.cfg"
        with open(config_path, 'w') as f:
            f.write(config_content)
        return str(config_path)

    def run_haddock_job(self, nanobody_path: str, antigen_path: str) -> Dict:
        """Run a single HADDOCK3 job and extract results"""
        # Generate run name
        nb_name = Path(nanobody_path).stem
        ag_name = Path(antigen_path).stem
        run_name = f"{nb_name}_vs_{ag_name}"

        print(f"Starting: {run_name}")
        start_time = time.time()

        try:
            # Create config file
            config_path = self.create_haddock_config(nanobody_path, antigen_path, run_name)

            # Run HADDOCK3
            cmd = ["haddock3", config_path]
            result = subprocess.run(cmd, cwd=self.output_dir, capture_output=True, text=True, timeout=6000)  # 1 hour t>
            if result.returncode == 0:
                # Extract results
                results = self.extract_results(run_name)
                results.update({
                    'nanobody': nb_name,
                    'antigen': ag_name,
                    'status': 'success',
                    'runtime': time.time() - start_time
                })
                print(f"Completed: {run_name} ({results['runtime']:.1f}s)")
            else:
                print(f"Failed: {run_name}")
                results = {
                    'nanobody': nb_name,
                    'antigen': ag_name,
                    'status': 'failed',
                    'runtime': time.time() - start_time,
                    'haddock_score': np.nan,
                    'cluster_size': 0,
                    'best_model': None
                }

        except subprocess.TimeoutExpired:
            print(f"Timeout: {run_name}")
            results = {
                'nanobody': nb_name,
                'antigen': ag_name,
                'status': 'timeout',
                'runtime': 3600,
                'haddock_score': np.nan,
                'cluster_size': 0,
                'best_model': None
            }

        return results

    def extract_results(self, run_name: str) -> Dict:
        """Extract key results from HADDOCK3 output"""
        run_dir = self.output_dir / run_name

        # Default values
        results = {
            'haddock_score': np.nan,
            'cluster_size': 0,
            'best_model': None,
            'i_rmsd': np.nan,
            'l_rmsd': np.nan,
            'fnat': np.nan
        }

        try:
            # Read capri_ss.tsv for scoring information
            capri_file = run_dir / "analysis" / "4_caprieval_analysis" / "capri_ss.tsv"
            if capri_file.exists():
                df = pd.read_csv(capri_file, sep='\t')
                if not df.empty:
                    # Get best model (first row)
                    best = df.iloc[0]
                    results['haddock_score'] = best.get('score', np.nan)
                    results['i_rmsd'] = best.get('i-RMSD', np.nan)
                    results['l_rmsd'] = best.get('l-RMSD', np.nan)
                    results['fnat'] = best.get('Fnat', np.nan)
                    results['best_model'] = best.get('model', 'cluster_1_model_1')

            # Read cluster information
            cluster_file = run_dir / "3_clustfcc" / "clustfcc.tsv"
            if cluster_file.exists():
                cluster_df = pd.read_csv(cluster_file, sep='\t')
                if not cluster_df.empty:
                    results['cluster_size'] = cluster_df.iloc[0].get('n', 0)

        return results

    def run_all_combinations(self, max_workers: int = 4):
        """Run all nanobody-antigen combinations"""
        print(f"Starting matrix screening with {max_workers} parallel workers...")

        # Generate all combinations
        combinations = [(nb, ag) for nb in self.nanobodies for ag in self.antigens]

        # Run jobs in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.run_haddock_job, nb, ag) for nb, ag in combinations]

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                self.detailed_results.append(result)

        print(f"Completed all {len(combinations)} combinations!")

    def create_results_matrix(self):
        """Create results matrix from detailed results"""
        if not self.detailed_results:
            print("No results available. Run combinations first.")
            return

        # Convert to DataFrame
        df = pd.DataFrame(self.detailed_results)

        # Create pivot table for HADDOCK scores
        self.results_matrix = df.pivot(index='nanobody', columns='antigen', values='haddock_score')

        # Save detailed results
        df.to_csv(self.output_dir / "detailed_results.csv", index=False)
        self.results_matrix.to_csv(self.output_dir / "haddock_score_matrix.csv")

        print(f"Results saved to {self.output_dir}")

    def plot_results_matrix(self, figsize: Tuple[int, int] = (12, 10)):
        """Plot the results matrix as a heatmap"""
        if self.results_matrix is None:
            print("No results matrix available. Create matrix first.")
            return

        plt.figure(figsize=figsize)

        # Create heatmap (lower scores = better binding, so reverse colormap)
        sns.heatmap(self.results_matrix,
                    annot=True,
                    fmt='.1f',
                    cmap='RdYlBu',  # Red=high(bad), Blue=low(good)
                    center=self.results_matrix.median().median(),
                    cbar_kws={'label': 'HADDOCK Score (lower = better)'})

        plt.title('Nanobody-Antigen Binding Matrix\n(HADDOCK3 Scores)', fontsize=16)
        plt.xlabel('Antigens', fontsize=12)
        plt.ylabel('Nanobodies', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()

        # Save plot
        plt.savefig(self.output_dir / "binding_matrix_heatmap.png", dpi=300, bbox_inches='tight')
        plt.savefig(self.output_dir / "binding_matrix_heatmap.pdf", bbox_inches='tight')
        plt.show()

    def generate_summary_report(self):
        """Generate a summary report of the screening results"""
        if not self.detailed_results:
            return

        df = pd.DataFrame(self.detailed_results)

        report = []
        report.append("HADDOCK3 Matrix Screening Summary Report")
        report.append("=" * 50)
        report.append(f"Total combinations tested: {len(df)}")
        report.append(f"Successful runs: {len(df[df['status'] == 'success'])}")
        report.append(f"Failed runs: {len(df[df['status'] == 'failed'])}")
        report.append(f"Timeout runs: {len(df[df['status'] == 'timeout'])}")
        report.append(f"Average runtime: {df['runtime'].mean():.1f} seconds")
        report.append("")

        # Best binding pairs
        successful = df[df['status'] == 'success'].copy()
        if not successful.empty:
            best_pairs = successful.nsmallest(5, 'haddock_score')
            report.append("Top 5 Binding Pairs (lowest HADDOCK scores):")
            for idx, row in best_pairs.iterrows():
                report.append(f"  {row['nanobody']} + {row['antigen']}: {row['haddock_score']:.1f}")
            report.append("")

        # Statistics
        if not successful.empty:
            report.append("Score Statistics:")
            report.append(f"  Best score: {successful['haddock_score'].min():.1f}")
            report.append(f"  Worst score: {successful['haddock_score'].max():.1f}")
            report.append(f"  Mean score: {successful['haddock_score'].mean():.1f}")
            report.append(f"  Std deviation: {successful['haddock_score'].std():.1f}")

        # Save report
        with open(self.output_dir / "summary_report.txt", 'w') as f:
            f.write('\n'.join(report))

        print('\n'.join(report))


def main():
    """Example usage"""
    # Initialize the screening pipeline
    screener = HADDOCK3MatrixScreening(
        structures_dir="/mnt/c/WSL/haddock3",  # Directory with nanobody*.pdb and antigen*.pdb
        output_dir="/mnt/c/WSL/haddock3_matrix_screening"
    )

    # Run all combinations (adjust max_workers based on your system)
    screener.run_all_combinations(max_workers=2)  # Conservative for stability

    # Create results matrix
    screener.create_results_matrix()

    # Plot results
    screener.plot_results_matrix()

    # Generate summary report
    screener.generate_summary_report()


if __name__ == "__main__":
    main()