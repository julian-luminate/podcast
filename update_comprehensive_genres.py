#!/usr/bin/env python3
"""
Update Comprehensive Genre Dataset

Merges internet research data with existing cross-platform genre data
to create a complete genre classification for all shows.
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

def merge_genre_sources():
    """Merge all genre data sources into comprehensive mapping."""

    # Load existing genre mapping (from Amazon cross-platform matches)
    existing_genres = pd.read_csv("podcast_genres.csv")

    # Load internet research data
    internet_genres = pd.read_csv("internet_research_genres.csv")

    # Create comprehensive mapping
    all_genres = []

    # Add existing genres
    for _, row in existing_genres.iterrows():
        all_genres.append({
            'show_name': row['show_name'],
            'normalized_name': normalize_show_name(row['show_name']),
            'genre': row['genre'],
            'source': row['source']
        })

    # Add internet research genres
    for _, row in internet_genres.iterrows():
        all_genres.append({
            'show_name': row['show_name'],
            'normalized_name': normalize_show_name(row['show_name']),
            'genre': row['genre'],
            'source': 'Internet Research'
        })

    # Create DataFrame and remove duplicates (prioritize existing data)
    genres_df = pd.DataFrame(all_genres)
    genres_df = genres_df.drop_duplicates(subset=['normalized_name'], keep='first')

    return genres_df

def apply_comprehensive_genres():
    """Apply the comprehensive genre mapping to all platform datasets."""

    # Get comprehensive genre mapping
    comprehensive_genres = merge_genre_sources()
    genre_map = dict(zip(comprehensive_genres['normalized_name'], comprehensive_genres['genre']))

    # Load platform data
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

    # Load and process Amazon
    amazon = pd.read_csv(data_dir / "amazon.csv", skiprows=2)
    amazon = amazon.dropna(subset=["Show Title"])
    amazon = amazon.rename(columns={
        "Show Title": "show_name",
        "Category Name": "original_genre"
    })
    amazon['normalized'] = amazon['show_name'].apply(normalize_show_name)
    # Prioritize Amazon's original genres, supplement with our mapping
    amazon['genre'] = amazon['original_genre'].fillna(amazon['normalized'].map(genre_map))

    # Load and process iHeart
    iheart = pd.read_csv(data_dir / "iheart_platform_nominations.csv", skiprows=2)
    iheart.columns = ["rank", "show_name", "iheart_listeners", "iheart_streams", "iheart_completion", "iheart_followers"]
    iheart = iheart.dropna(subset=["show_name"])
    iheart['normalized'] = iheart['show_name'].apply(normalize_show_name)
    iheart['genre'] = iheart['normalized'].map(genre_map)

    return spotify, youtube, amazon, iheart, comprehensive_genres

def analyze_comprehensive_coverage():
    """Analyze the comprehensive genre coverage."""

    spotify, youtube, amazon, iheart, genres = apply_comprehensive_genres()

    print("=== Comprehensive Genre Coverage Analysis ===\n")

    # Coverage by platform
    platforms = [
        ("Spotify", spotify),
        ("YouTube", youtube),
        ("Amazon", amazon),
        ("iHeart", iheart)
    ]

    total_coverage = {}

    for platform_name, df in platforms:
        coverage = df['genre'].notna().sum() / len(df)
        total_coverage[platform_name] = {
            'coverage': coverage,
            'shows_with_genre': df['genre'].notna().sum(),
            'total_shows': len(df)
        }

        print(f"{platform_name}: {coverage:.1%} coverage ({df['genre'].notna().sum()}/{len(df)} shows)")

        # Top genres
        top_genres = df['genre'].value_counts().head(5)
        print("Top genres:")
        for genre, count in top_genres.items():
            print(f"  {genre}: {count}")
        print()

    # Overall genre distribution
    all_shows_with_genres = []
    for _, df in platforms:
        shows_with_genres = df[df['genre'].notna()]
        all_shows_with_genres.extend(shows_with_genres['genre'].tolist())

    overall_genre_dist = pd.Series(all_shows_with_genres).value_counts()

    print("=== Overall Genre Distribution ===")
    for genre, count in overall_genre_dist.head(10).items():
        print(f"{genre}: {count} shows")

    return total_coverage

def export_comprehensive_datasets():
    """Export the comprehensive genre-enhanced datasets."""

    spotify, youtube, amazon, iheart, genres = apply_comprehensive_genres()

    # Create output directory
    output_dir = Path("data_comprehensive_genres")
    output_dir.mkdir(exist_ok=True)

    # Export enhanced datasets
    spotify_export = spotify[['show_name', 'spotify_plays', 'category', 'genre']].copy()
    spotify_export.to_csv(output_dir / "spotify_comprehensive_genres.csv", index=False)

    youtube_export = youtube[['show_name', 'watchtime_hrs', 'views', 'num_2025_videos', 'FeatureCountry', 'genre']].copy()
    youtube_export.to_csv(output_dir / "youtube_comprehensive_genres.csv", index=False)

    amazon_export = amazon[['show_name', 'genre', 'Publisher', 'Customers', 'Total Plays', 'Average Completion Rate', 'Total Follows']].copy()
    amazon_export = amazon_export.head(50)  # Limit to actual shows
    amazon_export.to_csv(output_dir / "amazon_comprehensive_genres.csv", index=False)

    iheart_export = iheart[['show_name', 'iheart_listeners', 'iheart_streams', 'iheart_completion', 'iheart_followers', 'genre']].copy()
    iheart_export.to_csv(output_dir / "iheart_comprehensive_genres.csv", index=False)

    # Export master comprehensive genre mapping
    genres_export = genres[['show_name', 'genre', 'source']].copy()
    genres_export.to_csv(output_dir / "comprehensive_genre_mapping.csv", index=False)

    print(f"Comprehensive datasets exported to {output_dir}/")
    print(f"Total unique shows with genres: {len(genres)}")

    return output_dir

if __name__ == "__main__":
    print("Creating comprehensive genre dataset with internet research...")
    print("="*60)

    # Analyze coverage
    coverage = analyze_comprehensive_coverage()

    print("\n" + "="*60)

    # Export datasets
    output_dir = export_comprehensive_datasets()

    print(f"\nComprehensive genre classification complete!")
    print(f"Files available in: {output_dir}")