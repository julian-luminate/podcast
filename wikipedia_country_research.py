#!/usr/bin/env python3
"""
Wikipedia research for podcast country origins
"""

import pandas as pd
import re
from pathlib import Path

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

def get_shows_needing_research():
    """Get list of shows needing country research."""

    # Load explicit country mapping
    explicit_mapping = {}
    try:
        explicit_df = pd.read_csv("explicit_country_mapping.csv")
        explicit_mapping = dict(zip(explicit_df['normalized_name'], explicit_df['country']))
        print(f"Loaded explicit country mapping: {len(explicit_mapping)} shows")
    except FileNotFoundError:
        print("No explicit country mapping found")
        return []

    # Get all shows from non-YouTube platforms
    all_shows = set()
    data_dir = Path("data")

    # Spotify shows
    try:
        spotify = pd.read_csv(data_dir / "spotify.csv", skiprows=7)
        spotify.columns = ["show_name", "spotify_plays", "category"]
        spotify = spotify.dropna()

        spotify_shows = [normalize_show_name(show) for show in spotify["show_name"]]
        all_shows.update(spotify_shows)
        print(f"Spotify shows: {len(spotify_shows)}")
    except Exception as e:
        print(f"Error loading Spotify: {e}")

    # Amazon shows
    try:
        amazon = pd.read_csv(data_dir / "amazon.csv", skiprows=2)
        amazon = amazon.dropna(subset=["Show Title"])

        amazon_shows = [normalize_show_name(show) for show in amazon["Show Title"]]
        all_shows.update(amazon_shows)
        print(f"Amazon shows: {len(amazon_shows)}")
    except Exception as e:
        print(f"Error loading Amazon: {e}")

    # iHeart shows
    try:
        iheart = pd.read_csv(data_dir / "iheart_platform_nominations.csv", skiprows=2)
        iheart.columns = ["rank", "show_name", "iheart_listeners", "iheart_streams", "iheart_completion", "iheart_followers"]
        iheart = iheart.dropna(subset=["show_name"])

        iheart_shows = [normalize_show_name(show) for show in iheart["show_name"]]
        all_shows.update(iheart_shows)
        print(f"iHeart shows: {len(iheart_shows)}")
    except Exception as e:
        print(f"Error loading iHeart: {e}")

    print(f"Total unique shows from non-YouTube platforms: {len(all_shows)}")

    # Find shows without explicit country data
    missing_country = []
    for show in all_shows:
        if show not in explicit_mapping:
            missing_country.append(show)

    print(f"Shows needing Wikipedia research: {len(missing_country)}")
    return sorted(missing_country)

def research_show_countries():
    """Research country origins for shows missing explicit data."""

    missing_shows = get_shows_needing_research()

    if not missing_shows:
        print("No shows need country research")
        return {}

    print(f"\nResearching {len(missing_shows)} shows...")
    print("=" * 60)

    # Research results will be collected here
    research_results = {}

    # Process shows in batches for Wikipedia research
    batch_size = 5
    for i in range(0, len(missing_shows), batch_size):
        batch = missing_shows[i:i+batch_size]
        print(f"\nBatch {i//batch_size + 1}: Researching {len(batch)} shows")

        for show in batch:
            print(f"Researching: {show}")
            # This will be filled with actual Wikipedia research
            research_results[show] = {
                "country": "RESEARCH_NEEDED",
                "source": "Wikipedia research pending",
                "confidence": "pending"
            }

    return research_results

if __name__ == "__main__":
    # Get shows needing research
    missing_shows = get_shows_needing_research()

    print(f"\nShows requiring Wikipedia research:")
    print("=" * 50)
    for i, show in enumerate(missing_shows[:20], 1):
        print(f"{i:2d}. {show}")

    if len(missing_shows) > 20:
        print(f"... and {len(missing_shows) - 20} more shows")

    print(f"\nNext step: Use Wikipedia search to research country origins for these {len(missing_shows)} shows")