#!/usr/bin/env python3
"""
Run AbNatiV on multiple nanobody FASTA files
"""

import os
import subprocess
import glob
import pandas as pd
import json
from datetime import datetime


def find_input_files():
    """Find all the fasta files we need to process"""
    input_folder = "/mnt/c/WSL/abnativ_batches"
    output_folder = "/mnt/c/WSL/abnativ_output"

    # Make sure output folder exists
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    print("")
    print("Please make sure the fasta batches are located in the directory:")
    print(input_folder)
    print("which (originally) would have been 'C:/WSL/abnativ_batches' from your windows operation system")
    print("")

    # Find all fasta files
    fasta_files = []
    for pattern in ["*.fasta", "*.fa", "*.fas"]:
        files = glob.glob(os.path.join(input_folder, pattern))
        fasta_files.extend(files)

    print("Found", len(fasta_files), "FASTA files to process")
    return fasta_files, input_folder, output_folder


def run_abnativ_batch(fasta_file, output_dir):
    """Run AbNatiV on one batch file"""
    # Get just the filename without extension
    batch_name = os.path.basename(fasta_file).split('.')[0]
    batch_results_folder = os.path.join(output_dir, batch_name + "_results")

    # Create folder for this batch
    os.makedirs(batch_results_folder, exist_ok=True)

    # This is the command that worked in testing
    command = [
        "python",
        "./abnativ/abnativ_script.py",
        "score",
        "-i", fasta_file,
        "-odir", batch_results_folder,
        "-oid", batch_name,
        "-isVHH",
        "-nat", "VHH",
        "-align"
    ]

    print("Processing batch:", batch_name)

    # Actually run the command
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd="/home/thor",
            timeout=7200  # 2 hours should be enough for 250 sequences
        )

        if result.returncode == 0:
            print("success:", batch_name)
            return True
        else:
            print("error:", batch_name)
            print("Error message:", result.stderr)
            return False

    except subprocess.TimeoutExpired:
        print("timeout error:", batch_name, "- took too long")
        return False
    except Exception as e:
        print("error:", batch_name, "-", str(e))
        return False


def combine_all_results(output_dir):
    """Put all the results together into one big file"""
    all_data = []
    failed_batches = []

    # Look for result folders
    result_folders = glob.glob(os.path.join(output_dir, "*_results"))

    for folder in result_folders:
        batch_name = os.path.basename(folder).replace("_results", "")

        # Try to find CSV files in this folder
        csv_files = glob.glob(os.path.join(folder, "*.csv"))

        if csv_files:
            try:
                # Read the first CSV file we find
                df = pd.read_csv(csv_files[0])
                df['batch_name'] = batch_name  # Add batch info
                all_data.append(df)
            except:
                print("Could not read results for", batch_name)
                failed_batches.append(batch_name)
        else:
            failed_batches.append(batch_name)

    # Combine everything
    if all_data:
        combined_results = pd.concat(all_data, ignore_index=True)

        # Save combined file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        combined_filename = os.path.join(output_dir, f"all_abnativ_results_{timestamp}.csv")
        combined_results.to_csv(combined_filename, index=False)

        # Also save as a summary
        summary_info = {
            'total_batches_attempted': len(result_folders),
            'successful_batches': len(all_data),
            'failed_batches': failed_batches,
            'total_sequences_processed': len(combined_results),
            'processing_date': timestamp
        }

        summary_filename = os.path.join(output_dir, f"processing_summary_{timestamp}.json")
        with open(summary_filename, 'w') as f:
            json.dump(summary_info, f, indent=2)

        print("Combined results saved to:", combined_filename)
        return combined_filename

    return None


def main():
    """Main function"""
    print("Starting AbNatiV batch processing...")
    print("Current time:", datetime.now())

    # Step 1: Find all the files
    fasta_files, input_dir, output_dir = find_input_files()

    # Check if we actually found files
    if not fasta_files:
        print("ERROR: No FASTA files found in", input_dir)
        print("Make sure files are in C:\\WSL\\abnativ_batches")
        return

    # Step 2: Process each file
    successful_count = 0
    failed_count = 0

    # # DEBUG: Only process first 2 files for testing
    # fasta_files = fasta_files[:2]

    for i, fasta_file in enumerate(fasta_files):
        print(f"\n--- Batch {i + 1} of {len(fasta_files)} ---")

        success = run_abnativ_batch(fasta_file, output_dir)

        if success:
            successful_count += 1
        else:
            failed_count += 1

        # # TEMP: Print progress every 5 batches
        # if (i + 1) % 5 == 0:
        #     print(f"Progress: {i+1}/{len(fasta_files)} batches completed")

    # Step 3: Show final results
    print("\n" + "=" * 50)
    print("Batch processing and prediction finished")
    print("Total batches processed:", len(fasta_files))
    print("Successful:", successful_count)
    print("Failed:", failed_count)

    # Step 4: Combine results if we got any
    if successful_count > 0:
        print("\nCombining all results...")
        combined_file = combine_all_results(output_dir)

        if combined_file:
            print("All results combined successfully!")

    print(f"\nAll files saved to: {output_dir}")


# Run the script
if __name__ == "__main__":
    main()