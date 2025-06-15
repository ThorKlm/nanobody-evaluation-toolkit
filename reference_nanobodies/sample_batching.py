#!/usr/bin/env python3
"""
Minimal FASTA sequence batcher for nanobody evaluation toolkit.
Splits FASTA files into batches for web server submissions.
"""

import os
import argparse
import shutil
from pathlib import Path


def parse_fasta(fasta_file):
    """Parse FASTA file and return list of (header, sequence) tuples."""
    sequences = []
    with open(fasta_file, 'r') as f:
        header = None
        sequence = ""

        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if header is not None:
                    sequences.append((header, sequence))
                header = line[1:]  # Remove '>'
                sequence = ""
            else:
                sequence += line

        # Add last sequence
        if header is not None:
            sequences.append((header, sequence))

    return sequences


def create_batches(sequences, batch_size, output_dir, format_type='fasta'):
    """Create batch files in specified format."""

    # Clean and create output directory
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    total_batches = (len(sequences) + batch_size - 1) // batch_size

    for i in range(0, len(sequences), batch_size):
        batch_num = (i // batch_size) + 1
        batch_sequences = sequences[i:i + batch_size]

        if format_type == 'fasta':
            filename = f"batch_{batch_num}.fasta"
            write_fasta_batch(batch_sequences, os.path.join(output_dir, filename))
        else:  # txt format - sequences only
            filename = f"batch_{batch_num}.txt"
            write_txt_batch(batch_sequences, os.path.join(output_dir, filename))

        print(f"Created {filename} with {len(batch_sequences)} sequences")

    print(f"\nTotal: {total_batches} batches created in '{output_dir}/'")
    return total_batches


def write_fasta_batch(sequences, filename):
    """Write sequences in FASTA format."""
    with open(filename, 'w') as f:
        for header, sequence in sequences:
            f.write(f">{header}\n{sequence}\n")


def write_txt_batch(sequences, filename):
    """Write sequences only (one per line)."""
    with open(filename, 'w') as f:
        for _, sequence in sequences:
            f.write(f"{sequence}\n")


def main():
    parser = argparse.ArgumentParser(description='Batch FASTA sequences for web server submissions')
    parser.add_argument('input_fasta', help='Input FASTA file')
    parser.add_argument('-b', '--batch-size', type=int, default=25,
                        help='Number of sequences per batch (default: 25)')
    parser.add_argument('-o', '--output-dir', default='batches',
                        help='Output directory for batches (default: batches)')
    parser.add_argument('-f', '--format', choices=['fasta', 'txt'], default='fasta',
                        help='Output format: fasta or txt (sequences only)')

    args = parser.parse_args()

    # Validate input file
    if not os.path.exists(args.input_fasta):
        print(f"Error: Input file '{args.input_fasta}' not found")
        return

    # Parse sequences
    print(f"Parsing sequences from {args.input_fasta}...")
    sequences = parse_fasta(args.input_fasta)

    if not sequences:
        print("No sequences found in input file")
        return

    print(f"Found {len(sequences)} sequences")

    # Create batches
    print(f"Creating batches of {args.batch_size} sequences...")
    create_batches(sequences, args.batch_size, args.output_dir, args.format)


if __name__ == "__main__":
    main()