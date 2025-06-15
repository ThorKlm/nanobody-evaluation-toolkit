# Concise python script to collect the information from the server output
# from the Google Colab notebook (e.g. in cases the full experiment could not be conducted in one run)
# This script allows to copy and paste the server output in a combined text file to convert it here
# into a plot-compatible csv format

import re
import pandas as pd
import numpy as np


# parse logs
def parse_logs(txt):
    results = []
    combo = None

    for i, line in enumerate(lines := txt.split('\n')):
        if m := re.match(r"Processing (\w+) vs structures/(\w+)", line):
            combo = {'nanobody': m.group(1), 'antigen': m.group(2)}
        elif combo and (m := re.match(r"\s*Seed (\d+)", line)):
            if i + 1 < len(lines):
                if m2 := re.match(r"\s*✓ BE: (-?\d+\.\d+)", lines[i + 1]):
                    results.append({**combo, 'seed': int(m.group(1)),
                                    'binding_energy': float(m2.group(1)), 'success': True})
    return pd.DataFrame(results)


# keep first n successful samples per combo
def filter_seeds(df, n=10):
    return df.groupby(['nanobody', 'antigen']).head(n)


# stats
def make_stats(df):
    stats = df.groupby(['nanobody', 'antigen'])['binding_energy'].agg(['mean', 'std', 'min', 'max', 'count']).round(3)
    stats.columns = [f'binding_energy_{x}' for x in stats.columns]
    # add dummy columns for compatibility
    for col in ['interface_area_mean', 'interface_area_std', 'interface_residues_mean',
                'interface_residues_std', 'complex_score_mean', 'complex_score_std']:
        stats[col] = 0
    return stats.reset_index()


# main call
with open('rosetta_notebook_outputs.txt', 'r', encoding='utf-8') as f:
    df = parse_logs(f.read())

df_filtered = filter_seeds(df[df['success']])
df_filtered.to_csv('rosetta_multiseed_raw_results.csv', index=False)
make_stats(df_filtered).to_csv('rosetta_multiseed_statistics.csv', index=False)

print(f"Completed: {len(df_filtered)} entries saved.")