#!/usr/bin/env python3
"""
Add the Japanese show with correct Comedy genre to union mapping
"""

import pandas as pd
import re

def normalize_show_name(name):
    """Normalize show name for matching - consistent with ranking system."""
    if pd.isna(name):
        return ""

    # Apply same normalization as ranking system
    normalized = str(name).strip().lower()
    # Remove all non-word/space characters
    normalized = re.sub(r"[^\w\s]", "", normalized)
    # Collapse multiple spaces to single space
    normalized = re.sub(r"\s+", " ", normalized)

    return normalized.strip()

def add_japanese_show():
    """Add the Japanese show to union mapping with correct Comedy genre."""

    # Load existing union mapping
    union_df = pd.read_csv("union_genre_mapping.csv")

    # Define the Japanese show
    japanese_show = "安住紳一郎の日曜天国"
    normalized_name = normalize_show_name(japanese_show)

    print("ADDING JAPANESE SHOW TO GENRE MAPPING")
    print("=" * 45)
    print(f"Original name: {japanese_show}")
    print(f"Normalized name: {normalized_name}")

    # Check if it already exists
    existing_mask = union_df['normalized_name'] == normalized_name

    if existing_mask.any():
        print("Show already exists in mapping, updating genre...")
        # Update existing entry
        union_df.loc[existing_mask, 'final_genre'] = 'Comedy'
        union_df.loc[existing_mask, 'tavily_genre'] = 'Comedy'

        # Update source summary
        current_sources = union_df.loc[existing_mask, 'source_summary'].iloc[0]
        if 'Tavily research' not in str(current_sources):
            new_sources = str(current_sources) + ' + Tavily research' if str(current_sources) else 'Tavily research'
            union_df.loc[existing_mask, 'source_summary'] = new_sources
    else:
        print("Adding new entry for Japanese show...")
        # Create new entry
        new_entry = {
            "normalized_name": normalized_name,
            "final_genre": "Comedy",
            "platform_genre": "Leisure",
            "research_genre": "",
            "tavily_genre": "Comedy",
            "source_summary": "Amazon platform + Tavily research"
        }

        # Add to dataframe
        new_df = pd.DataFrame([new_entry])
        union_df = pd.concat([union_df, new_df], ignore_index=True)

    # Sort by normalized name for consistency
    union_df = union_df.sort_values("normalized_name")

    # Save updated mapping
    union_df.to_csv("union_genre_mapping.csv", index=False)

    print("✓ Updated genre from 'Leisure/Other' to 'Comedy'")
    print("Research evidence: TBS radio comedy talk show format")
    print(f"Total shows in mapping: {len(union_df)}")

if __name__ == "__main__":
    add_japanese_show()