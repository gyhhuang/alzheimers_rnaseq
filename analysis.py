import pandas as pd
import os
import numpy as np
from tqdm import tqdm
from mygene import MyGeneInfo


mapping = {
    'SRR22924387': ['EC', 'Stage 3'],
    'SRR22924389': ['V2', 'Stage 3'],
    'SRR22924393': ['V2', 'Stage 1'],
    'SRR22924395': ['EC', 'Stage 1'],
    'SRR22924433': ['EC', 'Stage 4'],
    'SRR22924461': ['V2', 'Stage 4'],
    'SRR22924451': ['V2', 'Stage 1'],
    'SRR22924452': ['EC', 'Stage 1'],
    'SRR22924470': ['V2', 'Stage 3'],
    'SRR22924471': ['EC', 'Stage 3'],
    'SRR22924475': ['EC', 'Stage 4'],
    'SRR22924476': ['V2', 'Stage 4'],
    'SRR22924489': ['V2', 'Stage 2'],
    'SRR22924490': ['EC', 'Stage 2'],
    'SRR22924497': ['EC', 'Stage 2'],
    'SRR22924507': ['V2', 'Stage 2'],
}

# Initialize a list to hold DataFrames
data_frames = []

ec_df= []
v2_df = []

base_dir = 'expression'

# Iterate through the mapping
for key, (tissue, path_stage) in mapping.items():

    file_path = os.path.join(base_dir, key, 'abundance.tsv')
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, sep='\t', usecols=['target_id', 'est_counts', 'tpm'])
        
        df['tissue'] = tissue
        df['path_stage'] = path_stage

        if tissue == 'EC':
            ec_df.append(df)

        elif tissue == 'V2':
            v2_df.append(df)

    else:
        print(f"File not found: {file_path}")

# Combine all the DataFrames
ec_combined = pd.concat(ec_df, ignore_index=True)
v2_combined = pd.concat(v2_df, ignore_index=True)


# Pivot longer approach
def pivot_longer_by_stage(df):
    # Group by `target_id` and `path_stage`, then calculate mean for 'est_counts' and 'tpm'
    stage_means = df.groupby(['target_id', 'path_stage']).mean(numeric_only=True).reset_index()
    
    # Pivot to make 'path_stage' into columns for averages
    pivoted = stage_means.pivot(index='target_id', columns='path_stage', values=['est_counts', 'tpm'])
    
    # Flatten MultiIndex columns and rename for clarity
    pivoted.columns = ['_'.join(col).strip() for col in pivoted.columns.values]
    pivoted.reset_index(inplace=True)
    
    return pivoted

# Apply the function to EC and V2 combined DataFrames
ec_long = pivot_longer_by_stage(ec_combined)
v2_long = pivot_longer_by_stage(v2_combined)

genes = ec_long['target_id']

tpm_columns = ['tpm_Stage 1', 'tpm_Stage 2', 'tpm_Stage 3', 'tpm_Stage 4']

ec_tpm = ec_long[tpm_columns]
v2_tpm = v2_long[tpm_columns]

ec_tpm_log = np.log1p(ec_tpm)
v2_tpm_log = np.log1p(v2_tpm)

ec_with_labels = pd.concat([genes, ec_tpm_log], axis=1)
v2_with_labels = pd.concat([genes, v2_tpm_log], axis=1)

# Compute the slope of the trend for each row
v2_with_labels['slope'] = v2_with_labels[['tpm_Stage 1', 'tpm_Stage 2', 'tpm_Stage 3', 'tpm_Stage 4']].apply(
    lambda row: np.polyfit(range(1, 5), row, 1)[0], axis=1
)

ec_with_labels['slope'] = ec_with_labels[['tpm_Stage 1', 'tpm_Stage 2', 'tpm_Stage 3', 'tpm_Stage 4']].apply(
    lambda row: np.polyfit(range(1, 5), row, 1)[0], axis=1
)

# Sort by slope to identify strongest increasing or decreasing trends
increasing_trends = v2_with_labels.sort_values('slope', ascending=False).head(10)
decreasing_trends = v2_with_labels.sort_values('slope', ascending=True).head(10)

increasing_trends_ec = ec_with_labels.sort_values('slope', ascending=False).head(10)
decreasing_trends_ec = ec_with_labels.sort_values('slope', ascending=True).head(10)

def map_transcript_to_gene(transcript_ids):
    mg = MyGeneInfo()
    
    # Strip version suffix from transcript IDs
    stripped_ids = [transcript_id.split('.')[0] for transcript_id in transcript_ids]
    
    results = mg.querymany(stripped_ids, scopes='ensembl.transcript', fields='symbol', species='human')
    
    transcript_to_gene = {}
    for original_id, stripped_id in zip(transcript_ids, stripped_ids):
        match = next((item for item in results if item['query'] == stripped_id), None)
        if match and 'symbol' in match:
            transcript_to_gene[original_id] = match['symbol']
        else:
            transcript_to_gene[original_id] = 'Unknown'
    
    return transcript_to_gene

# Map for increasing trends
transcript_to_gene_increasing = map_transcript_to_gene(increasing_trends['target_id'].tolist())
increasing_trends['gene'] = increasing_trends['target_id'].map(transcript_to_gene_increasing)
transcript_to_gene_decreasing = map_transcript_to_gene(decreasing_trends['target_id'].tolist())
decreasing_trends['gene'] = decreasing_trends['target_id'].map(transcript_to_gene_decreasing)
transcript_to_gene_increasing_ec = map_transcript_to_gene(increasing_trends_ec['target_id'].tolist())
increasing_trends_ec['gene'] = increasing_trends_ec['target_id'].map(transcript_to_gene_increasing_ec)
transcript_to_gene_decreasing_ec = map_transcript_to_gene(decreasing_trends_ec['target_id'].tolist())
decreasing_trends_ec['gene'] = decreasing_trends_ec['target_id'].map(transcript_to_gene_decreasing_ec)

column_order = ['gene', 'slope', 'tpm_Stage 1', 'tpm_Stage 2', 'tpm_Stage 3', 'tpm_Stage 4']

increasing_trends = increasing_trends[column_order]
decreasing_trends = decreasing_trends[column_order]
increasing_trends_ec = increasing_trends_ec[column_order]
decreasing_trends_ec = decreasing_trends_ec[column_order]

print("Top 10 Increasing Trends V2:")
print(increasing_trends)

print("\nTop 10 Decreasing Trends V2:")
print(decreasing_trends)

print("\nTop 10 Increasing Trends EC:")
print(increasing_trends_ec)

print("\nTop 10 Decreasing Trends EC:")
print(decreasing_trends_ec)
