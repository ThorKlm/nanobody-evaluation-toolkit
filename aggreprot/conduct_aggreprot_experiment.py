#!/usr/bin/env python3
"""
AggreProt batch processing script
Run aggregation prediction on multiple FASTA files
"""

import os
import subprocess
import glob
import pandas as pd
import json
from datetime import datetime


def find_input_files():
    """Find all fasta files to process"""
    input_folder = "./aggrescan_input"
    output_folder = "./aggreprot_results"

    # Create directories if they don't exist
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print(f"Looking for FASTA files in: {input_folder}")

    # Find all fasta files
    fasta_files = []
    for pattern in ["*.fasta", "*.fa", "*.fas"]:
        files = glob.glob(os.path.join(input_folder, pattern))
        fasta_files.extend(files)

    print(f"Found {len(fasta_files)} FASTA files to process")
    return fasta_files, input_folder, output_folder


def run_aggreprot_batch(fasta_file, output_dir):
    """Run AggreProt on one batch file"""
    batch_name = os.path.basename(fasta_file).split('.')[0]
    batch_results_folder = os.path.join(output_dir, batch_name + "_results")

    os.makedirs(batch_results_folder, exist_ok=True)

    command = [
        "aggreprot-predictor",
        "predict-sequential-batch",
        "--out-dir", os.path.abspath(batch_results_folder),
        os.path.abspath(fasta_file)
    ]

    print(f"Processing batch: {batch_name}")

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd="./aggreprot-predictor",  # Run from repo directory
            timeout=3600  # 1 hour timeout
        )

        if result.returncode == 0:
            print(f"Success: {batch_name}")
            return True, batch_results_folder
        else:
            print(f"Error: {batch_name}")
            print(f"Error message: {result.stderr}")
            return False, None

    except subprocess.TimeoutExpired:
        print(f"Timeout error: {batch_name}")
        return False, None
    except Exception as e:
        print(f"Error: {batch_name} - {str(e)}")
        return False, None


def parse_aggreprot_output(result_folder, batch_name):
    """Parse AggreProt output files and convert to CSV"""
    # Look for output files (AggreProt typically creates .txt or .csv files)
    output_files = glob.glob(os.path.join(result_folder, "*"))

    if not output_files:
        return None

    # Try to find the main results file
    results_data = []

    # AggreProt usually outputs per-residue scores
    for file_path in output_files:
        if file_path.endswith('.txt') or file_path.endswith('.csv'):
            try:
                # Try reading as CSV first
                if file_path.endswith('.csv'):
                    df = pd.read_csv(file_path)
                else:
                    # Try tab-separated for .txt files
                    df = pd.read_csv(file_path, sep='\t')

                # Add batch info
                df['batch_name'] = batch_name
                results_data.append(df)

            except Exception as e:
                # If CSV reading fails, try parsing as text
                try:
                    with open(file_path, 'r') as f:
                        lines = f.readlines()

                    # Basic parsing for AggreProt output format
                    parsed_data = []
                    for line in lines:
                        if line.strip() and not line.startswith('#'):
                            parts = line.strip().split()
                            if len(parts) >= 2:
                                parsed_data.append({
                                    'sequence_id': parts[0] if len(parts) > 2 else 'unknown',
                                    'position': parts[0] if len(parts) <= 2 else parts[1],
                                    'aggregation_score': float(parts[-1]),
                                    'batch_name': batch_name
                                })

                    if parsed_data:
                        df = pd.DataFrame(parsed_data)
                        results_data.append(df)

                except:
                    continue

    if results_data:
        combined_df = pd.concat(results_data, ignore_index=True)
        return combined_df

    return None


def combine_all_results(output_dir, successful_results):
    """Combine all results into single CSV"""
    all_data = []
    failed_batches = []

    for batch_name, result_folder in successful_results:
        df = parse_aggreprot_output(result_folder, batch_name)
        if df is not None:
            all_data.append(df)
        else:
            failed_batches.append(batch_name)

    if all_data:
        combined_results = pd.concat(all_data, ignore_index=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        combined_filename = os.path.join(output_dir, f"all_aggreprot_results_{timestamp}.csv")
        combined_results.to_csv(combined_filename, index=False)

        # Summary info
        summary_info = {
            'total_batches_processed': len(successful_results),
            'successful_parsing': len(all_data),
            'failed_parsing': failed_batches,
            'total_predictions': len(combined_results),
            'processing_date': timestamp
        }

        summary_filename = os.path.join(output_dir, f"processing_summary_{timestamp}.json")
        with open(summary_filename, 'w') as f:
            json.dump(summary_info, f, indent=2)

        print(f"Combined results saved to: {combined_filename}")
        return combined_filename

    return None


def main():
    """Main processing function"""
    print("Starting AggreProt batch processing...")
    print(f"Current time: {datetime.now()}")

    # Find input files
    fasta_files, input_dir, output_dir = find_input_files()

    if not fasta_files:
        print(f"ERROR: No FASTA files found in {input_dir}")
        print("Please place FASTA files in the ./aggrescan_input directory")
        return

    # Process each file
    successful_count = 0
    failed_count = 0
    successful_results = []

    # # DEBUG: Only process first 2 files
    # fasta_files = fasta_files[:2]

    for i, fasta_file in enumerate(fasta_files):
        print(f"\n--- Batch {i + 1} of {len(fasta_files)} ---")

        success, result_folder = run_aggreprot_batch(fasta_file, output_dir)

        if success:
            successful_count += 1
            batch_name = os.path.basename(fasta_file).split('.')[0]
            successful_results.append((batch_name, result_folder))
        else:
            failed_count += 1

    # Final summary
    print("\n" + "=" * 50)
    print("AggreProt batch processing completed")
    print(f"Total batches: {len(fasta_files)}")
    print(f"Successful: {successful_count}")
    print(f"Failed: {failed_count}")

    # Combine results
    if successful_count > 0:
        print("\nCombining results...")
        combined_file = combine_all_results(output_dir, successful_results)

        if combined_file:
            print("All results combined successfully!")

    print(f"\nResults saved to: {output_dir}")


import os
if __name__ == "__main__":
    main()