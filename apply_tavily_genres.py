#!/usr/bin/env python3
"""
Apply Tavily-researched genres to the ranking system
"""

import pandas as pd
from pathlib import Path

def normalize_show_name(name):
    """Normalize show name for matching."""
    if pd.isna(name):
        return ""
    return str(name).lower().strip().replace("'", "'").replace(""", '"').replace(""", '"')

def create_tavily_normalized_mapping():
    """Create normalized mapping from Tavily research."""

    # Load Tavily mapping
    tavily_df = pd.read_csv("tavily_genre_mapping.csv")

    # Create normalized mapping
    normalized_mapping = {}
    for _, row in tavily_df.iterrows():
        normalized_name = normalize_show_name(row['show_name'])
        normalized_mapping[normalized_name] = row['tavily_genre']

    # Save normalized mapping
    normalized_df = pd.DataFrame([
        {"normalized_name": name, "tavily_genre": genre}
        for name, genre in normalized_mapping.items()
    ])
    normalized_df.to_csv("tavily_normalized_genre_mapping.csv", index=False)

    print(f"Created normalized Tavily genre mapping with {len(normalized_mapping)} shows")
    return normalized_mapping

def test_ranking_with_tavily():
    """Test the ranking system with Tavily genres."""

    # First create the normalized mapping
    create_tavily_normalized_mapping()

    # Load and test a few shows from our data
    from podcast_ranking_system import load_and_clean_data, normalize_show_names

    spotify, youtube, amazon, iheart = load_and_clean_data()

    # Normalize names
    spotify = normalize_show_names(spotify)
    youtube = normalize_show_names(youtube)
    amazon = normalize_show_names(amazon)
    iheart = normalize_show_names(iheart)

    # Load Tavily mapping
    tavily_mapping_df = pd.read_csv("tavily_normalized_genre_mapping.csv")
    tavily_genre_map = dict(zip(tavily_mapping_df['normalized_name'], tavily_mapping_df['tavily_genre']))

    # Test mapping coverage
    all_shows = set()
    all_shows.update(spotify['normalized_name'])
    all_shows.update(youtube['normalized_name'])
    all_shows.update(amazon['normalized_name'])
    all_shows.update(iheart['normalized_name'])

    mapped_shows = 0
    unmapped_shows = []

    for show in all_shows:
        if show in tavily_genre_map:
            mapped_shows += 1
        else:
            unmapped_shows.append(show)

    print(f"\nMAPPING COVERAGE:")
    print(f"Total unique shows in data: {len(all_shows)}")
    print(f"Shows mapped with Tavily research: {mapped_shows}")
    print(f"Coverage: {mapped_shows/len(all_shows)*100:.1f}%")

    if unmapped_shows:
        print(f"\nUnmapped shows ({len(unmapped_shows)}):")
        for show in sorted(unmapped_shows)[:10]:
            print(f"  - {show}")
        if len(unmapped_shows) > 10:
            print(f"  ... and {len(unmapped_shows) - 10} more")

    return tavily_genre_map

if __name__ == "__main__":
    mapping = test_ranking_with_tavily()