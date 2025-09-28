#!/usr/bin/env python3
"""
Check which Spotify and iHeart shows are missing genre mappings
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

def check_genre_coverage():
    """Check genre coverage for Spotify and iHeart shows."""

    print("CHECKING GENRE COVERAGE FOR SPOTIFY AND iHEART")
    print("=" * 55)

    # Load platform data
    data_dir = Path("data")

    # Load Spotify shows
    spotify = pd.read_csv(data_dir / "spotify.csv", skiprows=7)
    spotify.columns = ["show_name", "spotify_plays", "category"]
    spotify = spotify.dropna()

    spotify_shows = set()
    for show in spotify["show_name"]:
        spotify_shows.add(normalize_show_name(show))

    print(f"Spotify shows: {len(spotify_shows)}")

    # Load iHeart shows
    iheart = pd.read_csv(data_dir / "iheart_platform_nominations.csv", skiprows=2)
    iheart.columns = ["rank", "show_name", "iheart_listeners", "iheart_streams", "iheart_completion", "iheart_followers"]
    iheart = iheart.dropna(subset=["show_name"])

    iheart_shows = set()
    for show in iheart["show_name"]:
        iheart_shows.add(normalize_show_name(show))

    print(f"iHeart shows: {len(iheart_shows)}")

    # Load current genre mapping
    union_df = pd.read_csv("union_genre_mapping.csv")
    mapped_shows = set(union_df["normalized_name"])

    print(f"Shows with genre mapping: {len(mapped_shows)}")

    # Find missing shows
    missing_spotify = spotify_shows - mapped_shows
    missing_iheart = iheart_shows - mapped_shows

    print(f"\nMISSING GENRE MAPPINGS:")
    print(f"Spotify shows missing genre: {len(missing_spotify)}")
    if missing_spotify:
        print("Spotify missing shows:")
        for i, show in enumerate(sorted(missing_spotify)):
            print(f"  {i+1:2d}. {show}")

    print(f"\niHeart shows missing genre: {len(missing_iheart)}")
    if missing_iheart:
        print("iHeart missing shows:")
        for i, show in enumerate(sorted(missing_iheart)):
            print(f"  {i+1:2d}. {show}")

    # Get original show names for research
    spotify_name_map = {}
    for _, row in spotify.iterrows():
        normalized = normalize_show_name(row["show_name"])
        spotify_name_map[normalized] = row["show_name"]

    iheart_name_map = {}
    for _, row in iheart.iterrows():
        normalized = normalize_show_name(row["show_name"])
        iheart_name_map[normalized] = row["show_name"]

    # Return missing shows with original names for research
    missing_with_originals = {}

    for show in missing_spotify:
        missing_with_originals[show] = {
            "original": spotify_name_map.get(show, show),
            "platform": "Spotify"
        }

    for show in missing_iheart:
        missing_with_originals[show] = {
            "original": iheart_name_map.get(show, show),
            "platform": "iHeart"
        }

    return missing_with_originals

if __name__ == "__main__":
    missing = check_genre_coverage()