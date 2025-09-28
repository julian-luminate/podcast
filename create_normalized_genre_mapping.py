#!/usr/bin/env python3
"""
Create normalized genre mapping for the ranking system
"""

import pandas as pd
import re

def normalize_show_name(name):
    """Normalize show name for matching."""
    if pd.isna(name):
        return ""
    normalized = str(name).lower().strip()
    normalized = re.sub(r'[^\w\s]', '', normalized)
    normalized = re.sub(r'\s+', ' ', normalized)
    return normalized

# Load refined genre data
genre_df = pd.read_csv('data_refined_genres/refined_genre_master.csv')

# Create normalized mapping
normalized_mapping = {}
for _, row in genre_df.iterrows():
    original_name = row['show_name']
    normalized_name = normalize_show_name(original_name)
    genre = row['refined_genre']

    normalized_mapping[normalized_name] = {
        'original_name': original_name,
        'genre': genre
    }

# Create DataFrame for the normalized mapping
mapping_rows = []
for norm_name, data in normalized_mapping.items():
    mapping_rows.append({
        'normalized_name': norm_name,
        'original_name': data['original_name'],
        'refined_genre': data['genre']
    })

mapping_df = pd.DataFrame(mapping_rows)
mapping_df.to_csv('data_refined_genres/normalized_genre_mapping.csv', index=False)

print(f"Created normalized genre mapping with {len(mapping_df)} shows")
print("\nSample mappings:")
for _, row in mapping_df.head().iterrows():
    print(f"'{row['normalized_name']}' -> {row['refined_genre']}")