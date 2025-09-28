#!/usr/bin/env python3
"""
Verify that all normalization is consistent across the system
"""

import pandas as pd
import re
from pathlib import Path

def ranking_normalize_show_name(name):
    """Normalization function from ranking system."""
    if pd.isna(name):
        return ""
    normalized = str(name).strip().lower()
    normalized = re.sub(r"[^\w\s]", "", normalized)
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized.strip()

def load_and_normalize_data():
    """Load all platform data and normalize show names."""

    # Load platform data
    data_dir = Path("data")

    # Spotify
    spotify = pd.read_csv(data_dir / "spotify.csv", skiprows=7)
    spotify.columns = ["show_name", "spotify_plays", "category"]
    spotify = spotify.dropna()

    # YouTube (US filter)
    youtube = pd.read_csv(data_dir / "youtube.csv")
    youtube = youtube.rename(columns={"playlist_name": "show_name"})
    youtube = youtube[(youtube["FeatureCountry"] == "US") | (youtube["FeatureCountry"].isna())]

    # Amazon
    amazon = pd.read_csv(data_dir / "amazon.csv", skiprows=2)
    amazon = amazon.dropna(subset=["Show Title"])
    amazon = amazon.rename(columns={"Show Title": "show_name"})

    # iHeart
    iheart = pd.read_csv(data_dir / "iheart_platform_nominations.csv", skiprows=2)
    iheart.columns = ["rank", "show_name", "iheart_listeners", "iheart_streams", "iheart_completion", "iheart_followers"]
    iheart = iheart.dropna(subset=["show_name"])

    # Normalize all show names
    platform_shows = set()

    for show in spotify["show_name"]:
        platform_shows.add(ranking_normalize_show_name(show))

    for show in youtube["show_name"]:
        platform_shows.add(ranking_normalize_show_name(show))

    for show in amazon["show_name"]:
        platform_shows.add(ranking_normalize_show_name(show))

    for show in iheart["show_name"]:
        platform_shows.add(ranking_normalize_show_name(show))

    return platform_shows

def verify_genre_mapping_consistency():
    """Verify that genre mapping uses the same normalization."""

    print("NORMALIZATION CONSISTENCY VERIFICATION")
    print("=" * 50)

    # Get platform shows with ranking system normalization
    platform_shows = load_and_normalize_data()
    print(f"Platform shows (ranking normalization): {len(platform_shows)}")

    # Load union genre mapping
    try:
        union_df = pd.read_csv("union_genre_mapping.csv")
        genre_shows = set(union_df["normalized_name"])
        print(f"Genre mapping shows: {len(genre_shows)}")

        # Check coverage
        mapped_shows = platform_shows.intersection(genre_shows)
        unmapped_platform_shows = platform_shows - genre_shows
        extra_genre_shows = genre_shows - platform_shows

        print(f"\nCOVERAGE ANALYSIS:")
        print(f"Shows in both platform data and genre mapping: {len(mapped_shows)}")
        print(f"Platform shows missing from genre mapping: {len(unmapped_platform_shows)}")
        print(f"Genre mapping shows not in platform data: {len(extra_genre_shows)}")
        print(f"Coverage percentage: {len(mapped_shows)/len(platform_shows)*100:.1f}%")

        if unmapped_platform_shows:
            print(f"\nUNMAPPED PLATFORM SHOWS ({len(unmapped_platform_shows)}):")
            for i, show in enumerate(sorted(unmapped_platform_shows)[:10]):
                print(f"  {i+1:2d}. {show}")
            if len(unmapped_platform_shows) > 10:
                print(f"  ... and {len(unmapped_platform_shows) - 10} more")

        if extra_genre_shows:
            print(f"\nEXTRA GENRE SHOWS ({len(extra_genre_shows)}):")
            for i, show in enumerate(sorted(extra_genre_shows)[:10]):
                print(f"  {i+1:2d}. {show}")
            if len(extra_genre_shows) > 10:
                print(f"  ... and {len(extra_genre_shows) - 10} more")

        # Test some specific shows
        test_shows = [
            "The Joe Rogan Experience",
            "Crime Junkie",
            "48 Hours",
            "The Daily",
            "Good Mythical Morning with Rhett & Link"
        ]

        print(f"\nTEST SHOW NORMALIZATION:")
        for show in test_shows:
            normalized = ranking_normalize_show_name(show)
            in_genre_mapping = normalized in genre_shows
            print(f"  '{show}' -> '{normalized}' -> {'✓' if in_genre_mapping else '✗'}")

        return len(mapped_shows), len(platform_shows), len(genre_shows)

    except FileNotFoundError:
        print("ERROR: union_genre_mapping.csv not found")
        return 0, len(platform_shows), 0

if __name__ == "__main__":
    verify_genre_mapping_consistency()