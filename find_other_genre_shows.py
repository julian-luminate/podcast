#!/usr/bin/env python3
"""
Find shows with 'Other' genre classification for Tavily research
"""

import pandas as pd

def find_other_genre_shows():
    """Find shows currently classified as 'Other' genre."""

    # Load union genre mapping
    union_df = pd.read_csv("union_genre_mapping.csv")

    # Filter for "Other" genre shows
    other_shows = union_df[union_df["final_genre"] == "Other"]

    print("SHOWS WITH 'OTHER' GENRE CLASSIFICATION")
    print("=" * 50)
    print(f"Total shows with 'Other' genre: {len(other_shows)}")
    print()

    if len(other_shows) > 0:
        print("Shows needing genre research:")
        for i, (_, row) in enumerate(other_shows.iterrows(), 1):
            print(f"{i:2d}. {row['normalized_name']}")
            if row['platform_genre']:
                print(f"    Platform genre: {row['platform_genre']}")
            if row['research_genre']:
                print(f"    Research genre: {row['research_genre']}")
            if row['tavily_genre']:
                print(f"    Tavily genre: {row['tavily_genre']}")
            print(f"    Sources: {row['source_summary']}")
            print()

        # Return list for research
        return other_shows['normalized_name'].tolist()
    else:
        print("No shows found with 'Other' genre classification.")
        return []

if __name__ == "__main__":
    other_shows = find_other_genre_shows()