import pandas as pd
import requests
from Bio import PDB
from Bio.PDB import PDBParser
from Bio.PDB.Polypeptide import protein_letters_3to1
import time
import os
import warnings
from collections import defaultdict
from tqdm import tqdm

# Suppress all BioPython warnings
warnings.filterwarnings("ignore")
import Bio

Bio.PDB.Polypeptide.protein_letters_3to1 = Bio.PDB.Polypeptide.three_to_one


# Download PDB files from RCSB
def download_pdb_file(pdb_id, pdb_dir="pdb_files"):
    if not os.path.exists(pdb_dir):
        os.makedirs(pdb_dir)

    pdb_file = os.path.join(pdb_dir, f"{pdb_id}.pdb")
    if os.path.exists(pdb_file):
        return pdb_file

    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(pdb_file, 'w') as f:
                f.write(response.text)
            return pdb_file
        else:
            return None
    except Exception:
        return None


# Get amino acid sequence from PDB chain
def extract_sequence_from_pdb(pdb_file, chain_id):
    parser = PDBParser(QUIET=True)

    try:
        structure = parser.get_structure("structure", pdb_file)
        for model in structure:
            for chain in model:
                if chain.id == chain_id:
                    sequence = ""
                    for residue in chain:
                        if PDB.is_aa(residue):
                            sequence += protein_letters_3to1.get(residue.get_resname(), 'X')
                    return sequence
        return None
    except Exception:
        return None


def get_nanobody_sequences(tsv_file=r"sabdab_nano_summary_all.tsv", output_file="nanobody_sequences.csv"):
    # Load SABDAB data
    df = pd.read_csv(tsv_file, sep='\t')

    # Filter for nanobodies - they have heavy chain but no light chain
    nanobody_df = df[(df['Lchain'] == 'NA') | (df['Lchain'].isna())].copy()
    # nanobody_df = nanobody_df.head(20)  # debugging!

    sequences_data = []
    processed = set()

    # Progress bar for processing
    for idx, row in tqdm(nanobody_df.iterrows(), total=len(nanobody_df), desc="Processing nanobodies"):
        try:
            pdb_id = row['pdb'].lower()
            hchain = row['Hchain']

            if pd.isna(hchain) or hchain == 'NA':
                continue

            # Skip duplicates
            key = f"{pdb_id}_{hchain}"
            if key in processed:
                continue
            processed.add(key)

            # Get PDB file and extract sequence
            pdb_file = download_pdb_file(pdb_id)
            if not pdb_file:
                continue

            sequence = extract_sequence_from_pdb(pdb_file, hchain)
            if sequence:
                sequences_data.append({
                    'pdb_id': pdb_id,
                    'chain_id': hchain,
                    'sequence': sequence,
                    'length': len(sequence),
                    'organism': row.get('heavy_species', 'Unknown'),
                    'resolution': row.get('resolution', 'NA'),
                    'method': row.get('method', 'Unknown')
                })

            time.sleep(0.1)  # be nice to servers

        except Exception as e:
            # Skip problematic entries and continue
            continue

    # Process results and remove duplicate sequences
    results_df = pd.DataFrame(sequences_data)

    if len(results_df) > 0:
        # Group by sequence to find duplicates
        unique_seqs = defaultdict(list)
        for _, row in results_df.iterrows():
            unique_seqs[row['sequence']].append(row.to_dict())

        # Keep best resolution for each unique sequence
        final_data = []
        for i, (seq, entries) in enumerate(unique_seqs.items()):
            def get_resolution(x):
                try:
                    return float(x['resolution'])
                except (ValueError, TypeError):
                    return 999.0

            best = min(entries, key=get_resolution)
            best['sequence_index'] = i
            final_data.append(best)

        final_df = pd.DataFrame(final_data)
        final_df = final_df[
            ['pdb_id', 'sequence_index', 'sequence', 'chain_id', 'length', 'organism', 'resolution', 'method']]

        # Save results
        final_df.to_csv(output_file, index=False)
        print(f"Saved {len(final_df)} unique sequences to {output_file}")

        return final_df
    else:
        print("No sequences found")
        return pd.DataFrame()


# Main execution
if __name__ == "__main__":
    sequences_df = get_nanobody_sequences()

    # Also save as FASTA
    if len(sequences_df) > 0:
        with open("nanobody_sequences.fasta", "w") as f:
            for _, row in sequences_df.iterrows():
                f.write(f">{row['pdb_id']}_{row['chain_id']}_idx{row['sequence_index']}\n")
                f.write(f"{row['sequence']}\n")
        print("FASTA file stored.")