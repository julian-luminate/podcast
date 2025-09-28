#!/usr/bin/env python3
"""
Extract all unique show names from all platforms for genre research
"""

import pandas as pd
from pathlib import Path

def extract_unique_shows():
    """Extract unique show names from all platforms."""
    data_dir = Path("data")

    # Load and extract show names from each platform
    show_names = set()

    # Spotify
    try:
        spotify = pd.read_csv(data_dir / "spotify.csv", skiprows=7)
        spotify.columns = ["show_name", "spotify_plays", "category"]
        spotify = spotify.dropna()
        show_names.update(spotify["show_name"].str.lower().str.strip())
        print(f"Found {len(spotify)} shows from Spotify")
    except Exception as e:
        print(f"Error loading Spotify: {e}")

    # YouTube
    try:
        youtube = pd.read_csv(data_dir / "youtube.csv")
        youtube = youtube.rename(columns={"playlist_name": "show_name"})
        # Filter for US only
        youtube = youtube[(youtube["FeatureCountry"] == "US") | (youtube["FeatureCountry"].isna())]
        youtube_shows = youtube["show_name"].dropna().str.lower().str.strip()
        show_names.update(youtube_shows)
        print(f"Found {len(youtube_shows)} shows from YouTube")
    except Exception as e:
        print(f"Error loading YouTube: {e}")

    # Amazon
    try:
        amazon = pd.read_csv(data_dir / "amazon.csv", skiprows=2)
        amazon = amazon.dropna(subset=["Show Title"])
        amazon_shows = amazon["Show Title"].str.lower().str.strip()
        show_names.update(amazon_shows)
        print(f"Found {len(amazon_shows)} shows from Amazon")
    except Exception as e:
        print(f"Error loading Amazon: {e}")

    # iHeart
    try:
        iheart = pd.read_csv(data_dir / "iheart_platform_nominations.csv", skiprows=2)
        iheart.columns = ["rank", "show_name", "iheart_listeners", "iheart_streams", "iheart_completion", "iheart_followers"]
        iheart = iheart.dropna(subset=["show_name"])
        iheart_shows = iheart["show_name"].str.lower().str.strip()
        show_names.update(iheart_shows)
        print(f"Found {len(iheart_shows)} shows from iHeart")
    except Exception as e:
        print(f"Error loading iHeart: {e}")

    # Convert to sorted list
    unique_shows = sorted(list(show_names))

    print(f"\nTotal unique shows across all platforms: {len(unique_shows)}")

    # Save to file for reference
    shows_df = pd.DataFrame({"show_name": unique_shows})
    shows_df.to_csv("all_unique_shows.csv", index=False)

    return unique_shows

if __name__ == "__main__":
    shows = extract_unique_shows()
    print("\nFirst 10 shows:")
    for i, show in enumerate(shows[:10]):
        print(f"{i+1:2d}. {show}")