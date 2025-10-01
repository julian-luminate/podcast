#!/usr/bin/env python3
"""
Improve show name matching by creating a more robust normalization function
and identifying potential duplicate shows across platforms.
"""

import pandas as pd
import re
from collections import defaultdict


def improved_normalize(name):
    """
    Enhanced normalization that removes common podcast suffixes and prefixes
    to better match shows across platforms.
    """
    if pd.isna(name) or not name:
        return ''

    # Convert to lowercase and strip whitespace
    normalized = str(name).strip().lower()

    # Remove common suffixes (order matters - remove longer patterns first)
    suffixes_to_remove = [
        r'\s+the\s+podcast$',
        r'\s+podcast$',
        r'\s+the\s+show$',
        r'\s+show$',
        r'\s+with\s+stugotz$',
        r'\s+with\s+dax\s+shepard$',
        r'\s+with\s+karen\s+kilgariff\s+and\s+georgia\s+hardstark$',
        r'\s+with\s+matt\s+rogers\s+and\s+bowen\s+yang$',
        r'\s+with\s+rhett\s+link$',
        r'\s+w\s+theo\s+von$',
        r'\s+w/\s+theo\s+von$',
    ]

    for suffix in suffixes_to_remove:
        normalized = re.sub(suffix, '', normalized, flags=re.IGNORECASE)

    # Remove punctuation but keep spaces
    normalized = re.sub(r'[^\w\s]', '', normalized)

    # Normalize whitespace
    normalized = re.sub(r'\s+', ' ', normalized).strip()

    return normalized


def analyze_matches():
    """Analyze current matching and find potential improvements."""

    # Load all datasets
    print("Loading datasets...")

    spotify = pd.read_csv('data/spotify.csv', skiprows=7)
    spotify.columns = ['show_name', 'spotify_plays', 'category']
    spotify = spotify.dropna()

    youtube = pd.read_csv('data/youtube.csv')
    youtube = youtube.rename(columns={'playlist_name': 'show_name'})
    youtube = youtube[(youtube["FeatureCountry"] == "US") | (youtube["FeatureCountry"].isna())]

    amazon = pd.read_csv('data/amazon.csv', skiprows=2)
    amazon = amazon.rename(columns={'Show Title': 'show_name'})
    amazon = amazon.dropna(subset=['show_name'])

    apple = pd.read_csv('data/apple.csv')
    apple = apple.rename(columns={'Podcast': 'show_name'})
    apple = apple.dropna(subset=['show_name'])

    iheart = pd.read_csv('data/iheart_platform_nominations.csv', skiprows=2)
    iheart.columns = ['rank', 'show_name', 'iheart_listeners', 'iheart_streams', 'iheart_completion', 'iheart_followers']
    iheart = iheart.dropna(subset=['show_name'])

    # Apply old and new normalization
    def old_normalize(name):
        return str(name).strip().lower().replace(r'[^\w\s]', '').replace(r'\s+', ' ')

    # Create comparison dataframes
    all_shows = []

    for df, platform in [(spotify, 'Spotify'), (youtube, 'YouTube'),
                          (amazon, 'Amazon'), (apple, 'Apple'), (iheart, 'iHeart')]:
        temp = df[['show_name']].copy()
        temp['platform'] = platform
        temp['old_normalized'] = temp['show_name'].apply(lambda x: old_normalize(str(x)))
        temp['new_normalized'] = temp['show_name'].apply(improved_normalize)
        all_shows.append(temp)

    all_shows_df = pd.concat(all_shows, ignore_index=True)

    # Find shows that will now match with improved normalization
    print("\n=== IMPROVED MATCHING ANALYSIS ===\n")

    # Group by new normalized name and find cross-platform matches
    new_matches = all_shows_df.groupby('new_normalized').filter(
        lambda x: len(x['platform'].unique()) > 1
    )

    old_matches = all_shows_df.groupby('old_normalized').filter(
        lambda x: len(x['platform'].unique()) > 1
    )

    print(f"Old normalization: {len(old_matches['old_normalized'].unique())} shows matched across platforms")
    print(f"New normalization: {len(new_matches['new_normalized'].unique())} shows matched across platforms")
    print(f"Improvement: {len(new_matches['new_normalized'].unique()) - len(old_matches['old_normalized'].unique())} additional matches\n")

    # Show specific improvements
    newly_matched = set(new_matches['new_normalized'].unique()) - set(old_matches['old_normalized'].unique())

    if newly_matched:
        print(f"=== {len(newly_matched)} NEW CROSS-PLATFORM MATCHES ===\n")
        for norm_name in sorted(newly_matched):
            shows = all_shows_df[all_shows_df['new_normalized'] == norm_name]
            print(f"Normalized: '{norm_name}'")
            for _, row in shows.iterrows():
                print(f"  - {row['show_name']} [{row['platform']}]")
            print()

    return all_shows_df


def create_improved_mapping():
    """Create a mapping file for manual review of potential matches."""

    all_shows_df = analyze_matches()

    # Create a mapping file showing old vs new matches
    mapping = all_shows_df.groupby('new_normalized').agg({
        'show_name': lambda x: ' | '.join(sorted(set(x))),
        'platform': lambda x: ', '.join(sorted(set(x))),
        'old_normalized': 'first'
    }).reset_index()

    mapping.columns = ['new_normalized', 'all_variants', 'platforms', 'old_normalized']
    mapping['platform_count'] = mapping['platforms'].str.count(',') + 1
    mapping = mapping.sort_values('platform_count', ascending=False)

    mapping.to_csv('show_name_matching_analysis.csv', index=False)
    print(f"\nSaved matching analysis to show_name_matching_analysis.csv")
    print(f"Review this file to see all show name variants and how they match")


if __name__ == "__main__":
    create_improved_mapping()
