#!/usr/bin/env python3
"""
Copy full FASTA batches to clipboard for AGGRESCAN
"""

import os
import glob
import pyperclip


def find_next_batch():
    """Find next batch to process"""
    batch_index = 1
    while os.path.exists(f"batch_{batch_index}_aggrescan_results.txt"):
        batch_index += 1
    return batch_index


def find_fasta_files():
    """Find all FASTA files"""
    input_dir = "./aggrescan_input"
    if not os.path.exists(input_dir):
        return []

    files = []
    for pattern in ["*.fasta", "*.fa", "*.fas"]:
        files.extend(glob.glob(os.path.join(input_dir, pattern)))

    return sorted(files)


def format_fasta_for_aggrescan(filepath):
    """Read and format FASTA, filter invalid sequences"""
    formatted_content = []
    valid_aa = set('ACDEFGHIKLMNPQRSTVWY')
    current_header = None
    current_sequence = ""

    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_header and current_sequence:
                    if all(aa in valid_aa for aa in current_sequence):
                        formatted_content.append(current_header)
                        formatted_content.append(current_sequence)

                current_header = '> ' + line[1:]
                current_sequence = ""
            else:
                current_sequence += line

        if current_header and current_sequence:
            if all(aa in valid_aa for aa in current_sequence):
                formatted_content.append(current_header)
                formatted_content.append(current_sequence)

    return '\n'.join(formatted_content)


def main():
    """Main function"""
    batch_index = find_next_batch()
    fasta_files = find_fasta_files()

    if batch_index > len(fasta_files):
        print("All batches completed")
        return

    selected_file = fasta_files[batch_index - 1]
    formatted_content = format_fasta_for_aggrescan(selected_file)

    if not formatted_content:
        print("No valid sequences found")
        return

    pyperclip.copy(formatted_content)

    seq_count = len(formatted_content.split('\n')) // 2
    filename = os.path.basename(selected_file)

    print(f"Batch {batch_index}: {filename}")
    print(f"Copied {seq_count} sequences to clipboard")
    print(f"Save website results as: batch_{batch_index}_aggrescan_results.txt")


if __name__ == "__main__":
    main()