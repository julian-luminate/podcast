#!/usr/bin/env python3
"""
Genre Data Collection Analysis

Extracts existing genre data from Amazon platform and identifies
cross-platform shows that can inherit genres, then collects missing
genre data for YouTube and iHeart shows.
"""

import pandas as pd
from pathlib import Path
import re

def normalize_show_name(name):
    """Normalize show name for matching across platforms."""
    if pd.isna(name):
        return ""

    # Convert to lowercase and remove special characters
    normalized = str(name).lower().strip()
    normalized = re.sub(r'[^\w\s]', '', normalized)
    normalized = re.sub(r'\s+', ' ', normalized)
    return normalized

def load_data():
    """Load all platform data."""
    data_dir = Path("data")

    # Load Spotify
    spotify = pd.read_csv(data_dir / "spotify.csv", skiprows=7)
    spotify.columns = ["show_name", "spotify_plays", "category"]
    spotify = spotify.dropna()

    # Load YouTube
    youtube = pd.read_csv(data_dir / "youtube.csv")
    youtube = youtube.rename(columns={"playlist_name": "show_name"})
    # Filter for US shows only
    youtube = youtube[(youtube["FeatureCountry"] == "US") | (youtube["FeatureCountry"].isna())]

    # Load Amazon
    amazon = pd.read_csv(data_dir / "amazon.csv", skiprows=2)
    amazon = amazon.dropna(subset=["Show Title"])
    amazon = amazon.rename(columns={
        "Show Title": "show_name",
        "Category Name": "genre"
    })

    # Load iHeart
    iheart = pd.read_csv(data_dir / "iheart_platform_nominations.csv", skiprows=2)
    iheart.columns = ["rank", "show_name", "iheart_listeners", "iheart_streams", "iheart_completion", "iheart_followers"]
    iheart = iheart.dropna(subset=["show_name"])

    return spotify, youtube, amazon, iheart

def extract_amazon_genres():
    """Extract clean genre mapping from Amazon data."""
    _, _, amazon, _ = load_data()

    # Create genre mapping
    genre_map = {}
    for _, row in amazon.iterrows():
        normalized_name = normalize_show_name(row['show_name'])
        if normalized_name and not pd.isna(row['genre']):
            genre_map[normalized_name] = row['genre']

    print("Amazon Genre Distribution:")
    genre_counts = amazon['genre'].value_counts()
    for genre, count in genre_counts.items():
        print(f"  {genre}: {count} shows")

    print(f"\nTotal shows with genre data: {len(genre_map)}")
    return genre_map

def find_cross_platform_matches():
    """Find shows that appear on multiple platforms for genre inheritance."""
    spotify, youtube, amazon, iheart = load_data()

    # Normalize all show names
    spotify['normalized'] = spotify['show_name'].apply(normalize_show_name)
    youtube['normalized'] = youtube['show_name'].apply(normalize_show_name)
    amazon['normalized'] = amazon['show_name'].apply(normalize_show_name)
    iheart['normalized'] = iheart['show_name'].apply(normalize_show_name)

    # Get Amazon genre map
    amazon_genres = {}
    for _, row in amazon.iterrows():
        if not pd.isna(row['genre']):
            amazon_genres[row['normalized']] = row['genre']

    # Find YouTube shows that match Amazon shows
    youtube_matches = []
    for _, row in youtube.iterrows():
        if row['normalized'] in amazon_genres:
            youtube_matches.append({
                'show_name': row['show_name'],
                'normalized': row['normalized'],
                'genre': amazon_genres[row['normalized']],
                'source': 'Amazon match'
            })

    # Find iHeart shows that match Amazon shows
    iheart_matches = []
    for _, row in iheart.iterrows():
        if row['normalized'] in amazon_genres:
            iheart_matches.append({
                'show_name': row['show_name'],
                'normalized': row['normalized'],
                'genre': amazon_genres[row['normalized']],
                'source': 'Amazon match'
            })

    print(f"YouTube shows with Amazon genre matches: {len(youtube_matches)}")
    for match in youtube_matches:
        print(f"  {match['show_name']} -> {match['genre']}")

    print(f"\niHeart shows with Amazon genre matches: {len(iheart_matches)}")
    for match in iheart_matches:
        print(f"  {match['show_name']} -> {match['genre']}")

    return youtube_matches, iheart_matches

def collect_missing_genres():
    """Identify shows that need genre collection."""
    spotify, youtube, amazon, iheart = load_data()

    # Get existing matches
    youtube_matches, iheart_matches = find_cross_platform_matches()

    # Get matched show names
    youtube_matched = {m['normalized'] for m in youtube_matches}
    iheart_matched = {m['normalized'] for m in iheart_matches}

    # Find YouTube shows without genres
    youtube_missing = []
    for _, row in youtube.iterrows():
        normalized = normalize_show_name(row['show_name'])
        if normalized not in youtube_matched:
            youtube_missing.append({
                'show_name': row['show_name'],
                'normalized': normalized
            })

    # Find iHeart shows without genres
    iheart_missing = []
    for _, row in iheart.iterrows():
        normalized = normalize_show_name(row['show_name'])
        if normalized not in iheart_matched:
            iheart_missing.append({
                'show_name': row['show_name'],
                'normalized': normalized
            })

    print(f"\nYouTube shows needing genre collection: {len(youtube_missing)}")
    for show in youtube_missing[:10]:  # Show first 10
        print(f"  {show['show_name']}")
    if len(youtube_missing) > 10:
        print(f"  ... and {len(youtube_missing) - 10} more")

    print(f"\niHeart shows needing genre collection: {len(iheart_missing)}")
    for show in iheart_missing[:10]:  # Show first 10
        print(f"  {show['show_name']}")
    if len(iheart_missing) > 10:
        print(f"  ... and {len(iheart_missing) - 10} more")

    return youtube_missing, iheart_missing

if __name__ == "__main__":
    print("=== Genre Data Collection Analysis ===\n")

    # Extract Amazon genres
    amazon_genres = extract_amazon_genres()

    print("\n" + "="*50)

    # Find cross-platform matches
    youtube_matches, iheart_matches = find_cross_platform_matches()

    print("\n" + "="*50)

    # Find missing genres
    youtube_missing, iheart_missing = collect_missing_genres()

    print(f"\n=== Summary ===")
    print(f"Amazon shows with genres: {len(amazon_genres)}")
    print(f"YouTube cross-platform matches: {len(youtube_matches)}")
    print(f"iHeart cross-platform matches: {len(iheart_matches)}")
    print(f"YouTube shows needing research: {len(youtube_missing)}")
    print(f"iHeart shows needing research: {len(iheart_missing)}")