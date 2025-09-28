#!/usr/bin/env python3
"""
Unified Genre Classification System

Creates a standardized genre taxonomy and maps all shows to unified categories.
Reduces 43+ diverse genre labels to ~12 core categories for consistent analysis.
"""

import pandas as pd
from pathlib import Path

def define_unified_genres():
    """Define the unified genre classification system."""

    # Core unified genres (industry standard categories)
    unified_genres = {
        'True Crime': [
            'True Crime',
            'True Crime & Beauty',
            'True Crime & Comedy'
        ],
        'News & Politics': [
            'News & Politics',
            'News',
            'News & Commentary',
            'News & Law'
        ],
        'Comedy': [
            'Comedy',
            'Comedy & Entertainment',
            'Comedy & Interview',
            'Comedy & Lifestyle',
            'Comedy & Live Show',
            'Comedy & News',
            'Comedy & Pop Culture',
            'Comedy & Sports',
            'Comedy & Commentary',
            'Gaming & Comedy'
        ],
        'Interview & Talk': [
            'Interview & Talk',
            'Interview & Military',
            'Business & Interview'
        ],
        'Sports': [
            'Sports',
            'Sports & Commentary',
            'Sports & Entertainment',
            'Sports & Interview',
            'Sports & Lifestyle'
        ],
        'Business & Finance': [
            'Business & Finance',
            'Business & Politics'
        ],
        'Pop Culture & Entertainment': [
            'Pop Culture & Entertainment',
            'Entertainment & Lifestyle',
            'Anime & Pop Culture',
            'Relationships & Pop Culture',
            'Hip-Hop & Culture',
            'Country Music & Radio',
            'Radio & Entertainment'
        ],
        'Health & Wellness': [
            'Self-Help & Wellness',
            'Relationships & Lifestyle'
        ],
        'Education & Learning': [
            'Educational',
            'Education & Law',
            'Science & Psychology',
            'Science & Technology'
        ],
        'Religion & Spirituality': [
            'Religion & Spirituality'
        ],
        'Mystery & Paranormal': [
            'Mystery & Conspiracy'
        ],
        'Other': [
            'Miscellaneous'
        ]
    }

    return unified_genres

def create_genre_mapping():
    """Create mapping from current genres to unified categories."""

    unified_system = define_unified_genres()

    # Create reverse mapping: current genre -> unified genre
    genre_mapping = {}

    for unified_genre, current_genres in unified_system.items():
        for current_genre in current_genres:
            genre_mapping[current_genre] = unified_genre

    return genre_mapping, unified_system

def apply_unified_classification():
    """Apply unified genre classification to all shows."""

    # Load current comprehensive genre data
    genres_df = pd.read_csv('data_comprehensive_genres/comprehensive_genre_mapping.csv')

    # Get genre mapping
    genre_mapping, unified_system = create_genre_mapping()

    # Apply unified classification
    genres_df['unified_genre'] = genres_df['genre'].map(genre_mapping)

    # Handle any unmapped genres
    unmapped = genres_df[genres_df['unified_genre'].isna()]
    if len(unmapped) > 0:
        print("Unmapped genres found:")
        for genre in unmapped['genre'].unique():
            print(f"  - {genre}")

        # Map unmapped to 'Other' for now
        genres_df['unified_genre'] = genres_df['unified_genre'].fillna('Other')

    return genres_df, genre_mapping, unified_system

def analyze_unified_distribution():
    """Analyze the distribution of unified genres."""

    unified_genres_df, _, unified_system = apply_unified_classification()

    print("=== Unified Genre Classification Analysis ===\n")

    # Show the unified taxonomy
    print("Unified Genre Taxonomy:")
    print("-" * 30)
    for unified_genre, original_genres in unified_system.items():
        print(f"{unified_genre}:")
        for orig in original_genres:
            print(f"  • {orig}")
        print()

    # Distribution analysis
    unified_dist = unified_genres_df['unified_genre'].value_counts()

    print("=== Unified Genre Distribution ===")
    total_shows = len(unified_genres_df)

    for genre, count in unified_dist.items():
        percentage = (count / total_shows) * 100
        print(f"{genre}: {count} shows ({percentage:.1f}%)")

    print(f"\nTotal shows: {total_shows}")
    print(f"Unified categories: {len(unified_dist)}")
    print(f"Reduction from {len(unified_genres_df['genre'].unique())} to {len(unified_dist)} categories")

    return unified_dist

def export_unified_datasets():
    """Export all datasets with unified genre classification."""

    unified_genres_df, genre_mapping, unified_system = apply_unified_classification()

    # Create unified mapping for easy lookup
    unified_lookup = dict(zip(unified_genres_df['show_name'], unified_genres_df['unified_genre']))

    # Load and update platform datasets
    data_dir = Path("data_comprehensive_genres")
    output_dir = Path("data_unified_genres")
    output_dir.mkdir(exist_ok=True)

    # Update Spotify
    spotify = pd.read_csv(data_dir / "spotify_comprehensive_genres.csv")
    spotify['unified_genre'] = spotify['show_name'].map(unified_lookup)
    spotify.to_csv(output_dir / "spotify_unified_genres.csv", index=False)

    # Update YouTube
    youtube = pd.read_csv(data_dir / "youtube_comprehensive_genres.csv")
    youtube['unified_genre'] = youtube['show_name'].map(unified_lookup)
    youtube.to_csv(output_dir / "youtube_unified_genres.csv", index=False)

    # Update Amazon
    amazon = pd.read_csv(data_dir / "amazon_comprehensive_genres.csv")
    amazon['unified_genre'] = amazon['show_name'].map(unified_lookup)
    amazon.to_csv(output_dir / "amazon_unified_genres.csv", index=False)

    # Update iHeart
    iheart = pd.read_csv(data_dir / "iheart_comprehensive_genres.csv")
    iheart['unified_genre'] = iheart['show_name'].map(unified_lookup)
    iheart.to_csv(output_dir / "iheart_unified_genres.csv", index=False)

    # Export master unified mapping
    unified_master = unified_genres_df[['show_name', 'genre', 'unified_genre', 'source']].copy()
    unified_master.to_csv(output_dir / "unified_genre_master.csv", index=False)

    # Export genre taxonomy reference
    taxonomy_rows = []
    for unified_genre, original_genres in unified_system.items():
        for original in original_genres:
            taxonomy_rows.append({
                'original_genre': original,
                'unified_genre': unified_genre
            })

    taxonomy_df = pd.DataFrame(taxonomy_rows)
    taxonomy_df.to_csv(output_dir / "genre_taxonomy_mapping.csv", index=False)

    print(f"\nUnified datasets exported to: {output_dir}")
    print(f"Files created:")
    print(f"  - Platform datasets with unified genres")
    print(f"  - unified_genre_master.csv (all shows)")
    print(f"  - genre_taxonomy_mapping.csv (taxonomy reference)")

    return output_dir

def validate_unified_system():
    """Validate the unified classification system."""

    unified_genres_df, _, _ = apply_unified_classification()

    print("\n=== Validation Results ===")

    # Check coverage
    total_shows = len(unified_genres_df)
    shows_with_unified = unified_genres_df['unified_genre'].notna().sum()
    coverage = (shows_with_unified / total_shows) * 100

    print(f"Coverage: {coverage:.1f}% ({shows_with_unified}/{total_shows} shows)")

    # Check for 'Other' category usage
    other_count = len(unified_genres_df[unified_genres_df['unified_genre'] == 'Other'])
    other_percentage = (other_count / total_shows) * 100

    print(f"'Other' category usage: {other_percentage:.1f}% ({other_count} shows)")

    if other_count > 0:
        print("Shows in 'Other' category:")
        other_shows = unified_genres_df[unified_genres_df['unified_genre'] == 'Other']
        for _, row in other_shows.iterrows():
            print(f"  - {row['show_name']} (was: {row['genre']})")

    # Genre balance check
    unified_dist = unified_genres_df['unified_genre'].value_counts()
    largest_genre = unified_dist.iloc[0]
    largest_percentage = (largest_genre / total_shows) * 100

    print(f"\nLargest genre: {unified_dist.index[0]} ({largest_percentage:.1f}%)")
    print(f"Genre balance: {len(unified_dist)} categories")

if __name__ == "__main__":
    print("Creating Unified Genre Classification System")
    print("=" * 50)

    # Analyze current distribution and create unified system
    distribution = analyze_unified_distribution()

    print("\n" + "=" * 50)

    # Export unified datasets
    output_dir = export_unified_datasets()

    # Validate the system
    validate_unified_system()

    print(f"\nUnified genre classification complete!")