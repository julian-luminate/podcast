#!/usr/bin/env python3
"""
Apply Genre Mapping to All Platforms

Applies the collected genre data to YouTube and iHeart datasets,
and creates comprehensive genre mapping across all platforms.
"""

import pandas as pd
from pathlib import Path
import re

def normalize_show_name(name):
    """Normalize show name for matching."""
    if pd.isna(name):
        return ""
    normalized = str(name).lower().strip()
    normalized = re.sub(r'[^\w\s]', '', normalized)
    normalized = re.sub(r'\s+', ' ', normalized)
    return normalized

def load_genre_mapping():
    """Load the genre mapping CSV."""
    genres_df = pd.read_csv("podcast_genres.csv")

    # Create normalized mapping
    genre_map = {}
    for _, row in genres_df.iterrows():
        normalized = normalize_show_name(row['show_name'])
        genre_map[normalized] = row['genre']

    return genre_map

def apply_genres_to_platforms():
    """Apply genre mapping to all platform datasets."""

    # Load genre mapping
    genre_map = load_genre_mapping()
    data_dir = Path("data")

    # Load and process Spotify
    spotify = pd.read_csv(data_dir / "spotify.csv", skiprows=7)
    spotify.columns = ["show_name", "spotify_plays", "category"]
    spotify = spotify.dropna()
    spotify['normalized'] = spotify['show_name'].apply(normalize_show_name)
    spotify['genre'] = spotify['normalized'].map(genre_map)

    # Load and process YouTube
    youtube = pd.read_csv(data_dir / "youtube.csv")
    youtube = youtube.rename(columns={"playlist_name": "show_name"})
    youtube = youtube[(youtube["FeatureCountry"] == "US") | (youtube["FeatureCountry"].isna())]
    youtube['normalized'] = youtube['show_name'].apply(normalize_show_name)
    youtube['genre'] = youtube['normalized'].map(genre_map)

    # Load and process Amazon (already has genres, but normalize them)
    amazon = pd.read_csv(data_dir / "amazon.csv", skiprows=2)
    amazon = amazon.dropna(subset=["Show Title"])
    amazon = amazon.rename(columns={
        "Show Title": "show_name",
        "Category Name": "genre"
    })
    amazon['normalized'] = amazon['show_name'].apply(normalize_show_name)
    # Use existing Amazon genres, supplemented by our mapping
    amazon['genre'] = amazon['genre'].fillna(amazon['normalized'].map(genre_map))

    # Load and process iHeart
    iheart = pd.read_csv(data_dir / "iheart_platform_nominations.csv", skiprows=2)
    iheart.columns = ["rank", "show_name", "iheart_listeners", "iheart_streams", "iheart_completion", "iheart_followers"]
    iheart = iheart.dropna(subset=["show_name"])
    iheart['normalized'] = iheart['show_name'].apply(normalize_show_name)
    iheart['genre'] = iheart['normalized'].map(genre_map)

    return spotify, youtube, amazon, iheart

def analyze_genre_coverage():
    """Analyze genre coverage across platforms."""
    spotify, youtube, amazon, iheart = apply_genres_to_platforms()

    print("=== Genre Coverage Analysis ===\n")

    # Spotify genre coverage
    spotify_coverage = spotify['genre'].notna().sum() / len(spotify)
    print(f"Spotify: {spotify_coverage:.1%} coverage ({spotify['genre'].notna().sum()}/{len(spotify)} shows)")
    spotify_genres = spotify['genre'].value_counts().head(10)
    print("Top genres:")
    for genre, count in spotify_genres.items():
        print(f"  {genre}: {count}")

    print()

    # YouTube genre coverage
    youtube_coverage = youtube['genre'].notna().sum() / len(youtube)
    print(f"YouTube: {youtube_coverage:.1%} coverage ({youtube['genre'].notna().sum()}/{len(youtube)} shows)")
    youtube_genres = youtube['genre'].value_counts().head(10)
    print("Top genres:")
    for genre, count in youtube_genres.items():
        print(f"  {genre}: {count}")

    print()

    # Amazon genre coverage
    amazon_coverage = amazon['genre'].notna().sum() / len(amazon)
    print(f"Amazon: {amazon_coverage:.1%} coverage ({amazon['genre'].notna().sum()}/{len(amazon)} shows)")
    amazon_genres = amazon['genre'].value_counts().head(10)
    print("Top genres:")
    for genre, count in amazon_genres.items():
        print(f"  {genre}: {count}")

    print()

    # iHeart genre coverage
    iheart_coverage = iheart['genre'].notna().sum() / len(iheart)
    print(f"iHeart: {iheart_coverage:.1%} coverage ({iheart['genre'].notna().sum()}/{len(iheart)} shows)")
    iheart_genres = iheart['genre'].value_counts().head(10)
    print("Top genres:")
    for genre, count in iheart_genres.items():
        print(f"  {genre}: {count}")

def export_genre_enhanced_data():
    """Export datasets with genre information."""
    spotify, youtube, amazon, iheart = apply_genres_to_platforms()

    # Create output directory
    output_dir = Path("data_with_genres")
    output_dir.mkdir(exist_ok=True)

    # Export enhanced datasets
    spotify_export = spotify[['show_name', 'spotify_plays', 'category', 'genre']].copy()
    spotify_export.to_csv(output_dir / "spotify_with_genres.csv", index=False)

    youtube_export = youtube[['show_name', 'watchtime_hrs', 'views', 'num_2025_videos', 'FeatureCountry', 'genre']].copy()
    youtube_export.to_csv(output_dir / "youtube_with_genres.csv", index=False)

    amazon_export = amazon[['show_name', 'genre', 'Publisher', 'Customers', 'Total Plays', 'Average Completion Rate', 'Total Follows']].copy()
    amazon_export = amazon_export.head(50)  # Limit to actual shows, not padding
    amazon_export.to_csv(output_dir / "amazon_with_genres.csv", index=False)

    iheart_export = iheart[['show_name', 'iheart_listeners', 'iheart_streams', 'iheart_completion', 'iheart_followers', 'genre']].copy()
    iheart_export.to_csv(output_dir / "iheart_with_genres.csv", index=False)

    print(f"\nGenre-enhanced datasets exported to {output_dir}/")

    # Create master genre mapping
    all_shows = []

    for _, row in spotify.iterrows():
        if pd.notna(row['genre']):
            all_shows.append({
                'show_name': row['show_name'],
                'normalized_name': row['normalized'],
                'genre': row['genre'],
                'platforms': 'Spotify'
            })

    for _, row in youtube.iterrows():
        if pd.notna(row['genre']):
            all_shows.append({
                'show_name': row['show_name'],
                'normalized_name': row['normalized'],
                'genre': row['genre'],
                'platforms': 'YouTube'
            })

    for _, row in amazon.iterrows():
        if pd.notna(row['genre']):
            all_shows.append({
                'show_name': row['show_name'],
                'normalized_name': row['normalized'],
                'genre': row['genre'],
                'platforms': 'Amazon'
            })

    for _, row in iheart.iterrows():
        if pd.notna(row['genre']):
            all_shows.append({
                'show_name': row['show_name'],
                'normalized_name': row['normalized'],
                'genre': row['genre'],
                'platforms': 'iHeart'
            })

    master_df = pd.DataFrame(all_shows)
    master_df.to_csv(output_dir / "master_genre_mapping.csv", index=False)

    return spotify_export, youtube_export, amazon_export, iheart_export

if __name__ == "__main__":
    print("Applying genre mapping to all platforms...")

    # Analyze coverage
    analyze_genre_coverage()

    print("\n" + "="*60)

    # Export enhanced data
    export_genre_enhanced_data()

    print("\nGenre mapping complete!")