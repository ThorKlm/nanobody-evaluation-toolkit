import numpy as np
import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog


# https://biocomp.chem.uw.edu.pl/A3D2/

def compute_developmentability_score(residue_scores):
    """
    Compute a developmentability score for nanobodies using Aggrescan3D data.

    Args:
        residue_scores (list or np.array): List of A3D scores (floats)

    Returns:
        float: Developmentability score (higher = better)
    """
    scores = np.array(residue_scores)
    seq_len = len(scores)

    if seq_len == 0:
        return 0.0

    # Core Metrics
    avg_score = np.mean(scores)
    max_score = np.max(scores)

    # Count problematic residues
    positive_count = np.sum(scores > 0.0)
    high_risk_count = np.sum(scores > 0.5)
    very_high_risk_count = np.sum(scores > 1.0)

    # Fractions
    positive_fraction = positive_count / seq_len
    high_risk_fraction = high_risk_count / seq_len

    # Aggregation burden (sum of positive scores)
    positive_scores = scores[scores > 0.0]
    aggregation_burden = np.sum(positive_scores) if len(positive_scores) > 0 else 0.0

    # Scoring Components (0-1 scale, higher = better)

    # 1. Average score (more negative is better)
    avg_component = max(0.0, min(1.0, (-avg_score + 0.5) / 2.5))

    # 2. Maximum score (lower peaks are better)
    if max_score <= 0.0:
        max_component = 1.0
    elif max_score <= 0.5:
        max_component = 1.0 - (max_score / 0.5) * 0.3
    elif max_score <= 1.0:
        max_component = 0.7 - (max_score - 0.5) * 1.4
    else:
        max_component = max(0.0, 0.7 - 1.4 - (max_score - 1.0) * 2.0)

    # 3. Positive fraction (fewer positive residues is better)
    pos_fraction_component = max(0.0, 1.0 - positive_fraction * 2.0)

    # 4. High-risk fraction (fewer high-risk residues is better)
    high_risk_component = max(0.0, 1.0 - high_risk_fraction * 5.0)

    # 5. Aggregation burden (lower total positive scores is better)
    burden_component = max(0.0, 1.0 - aggregation_burden / 10.0)

    # === Weighted Final Score ===
    overall_score = (
            0.20 * avg_component +
            0.20 * max_component +
            0.20 * pos_fraction_component +
            0.20 * high_risk_component +
            0.20 * burden_component
    )

    # === Hard Rejection Criteria ===
    hard_reject = (
            very_high_risk_count > 2 or
            max_score > 2.0 or
            positive_fraction > 0.4 or
            aggregation_burden > 15.0
    )

    if hard_reject:
        overall_score = min(overall_score, 0.3)

    return round(overall_score, 4)


def process_csv_file(csv_path):
    """
    Process a single CSV file and return results.

    Args:
        csv_path (str): Path to CSV file

    Returns:
        dict: Results dictionary with protein IDs and scores
    """
    try:
        df = pd.read_csv(csv_path)
        print(f"Loaded CSV: {os.path.basename(csv_path)}")
        print(f"Total rows: {len(df)}")

        results = {}
        for (protein, chain), group in df.groupby(['protein', 'chain']):
            group_sorted = group.sort_values('residue')
            scores = group_sorted['score'].values

            protein_id = f"{protein}_{chain}" if chain else protein
            score = compute_developmentability_score(scores)
            results[protein_id] = score

            print(f"{protein_id}: {score} ({len(scores)} residues)")

        print(f"\nProcessed {len(results)} protein(s)")
        return results

    except Exception as e:
        print(f"ERROR processing {os.path.basename(csv_path)}: {str(e)}")
        return {}


def select_csv_file():
    """
    Open file dialog to select CSV file.

    Returns:
        str or None: Selected file path, or None if cancelled
    """
    try:
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        file_path = filedialog.askopenfilename(
            title="Select Aggrescan3D CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialdir=os.getcwd()
        )

        root.destroy()
        return file_path if file_path else None

    except Exception as e:
        print(f"File dialog error: {str(e)}")
        return None


# Main script
if __name__ == "__main__":
    print("AGGRESCAN3D DEVELOPMENTABILITY SCORER")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_csv = os.path.join(script_dir, "sample_A3D.csv")

    # Try default file first
    if os.path.exists(default_csv):
        print(f"Found default file: {os.path.basename(default_csv)}")
        process_csv_file(default_csv)
    else:
        print("Default 'sample_A3D.csv' not found.")

    # Always offer file selection option
    print("\nSelect different CSV file? (File dialog will open)")
    selected_file = select_csv_file()

    if selected_file:
        print(f"\nProcessing selected file: {os.path.basename(selected_file)}")
        process_csv_file(selected_file)
    else:
        print("No file selected or dialog cancelled.")

        if not os.path.exists(default_csv):
            print("\nNo CSV file to process.")
            print("Expected format: protein,chain,residue,residue_name,score")

    print("\nAnalysis Complete")