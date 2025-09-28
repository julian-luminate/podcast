#!/usr/bin/env python3
"""
Refined Genre Classification System

Creates a cleaner, more standardized genre taxonomy by reducing
43 variations down to ~8 core industry-standard categories.
"""

import pandas as pd
from pathlib import Path

def define_refined_genres():
    """Define the refined genre classification system with fewer, cleaner categories."""

    # Refined taxonomy - fewer, industry-standard categories
    refined_genres = {
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
            'Interview & Military'
        ],
        'Sports': [
            'Sports',
            'Sports & Commentary',
            'Sports & Entertainment',
            'Sports & Interview',
            'Sports & Lifestyle'
        ],
        'Business': [
            'Business & Finance',
            'Business & Interview',
            'Business & Politics'
        ],
        'Entertainment': [
            'Pop Culture & Entertainment',
            'Entertainment & Lifestyle',
            'Anime & Pop Culture',
            'Relationships & Pop Culture',
            'Hip-Hop & Culture',
            'Country Music & Radio',
            'Radio & Entertainment',
            'Relationships & Lifestyle'
        ],
        'Education': [
            'Educational',
            'Education & Law',
            'Science & Psychology',
            'Science & Technology',
            'Self-Help & Wellness',
            'Religion & Spirituality',
            'Mystery & Conspiracy',
            'Miscellaneous'
        ]
    }

    return refined_genres

def create_refined_mapping():
    """Create mapping from current genres to refined categories."""

    refined_system = define_refined_genres()

    # Create reverse mapping: current genre -> refined genre
    genre_mapping = {}

    for refined_genre, current_genres in refined_system.items():
        for current_genre in current_genres:
            genre_mapping[current_genre] = refined_genre

    return genre_mapping, refined_system

def apply_refined_classification():
    """Apply refined genre classification to all shows."""

    # Load current comprehensive genre data
    genres_df = pd.read_csv('data_comprehensive_genres/comprehensive_genre_mapping.csv')

    # Get refined mapping
    genre_mapping, refined_system = create_refined_mapping()

    # Apply refined classification
    genres_df['refined_genre'] = genres_df['genre'].map(genre_mapping)

    # Handle any unmapped genres
    unmapped = genres_df[genres_df['refined_genre'].isna()]
    if len(unmapped) > 0:
        print("Unmapped genres found:")
        for genre in unmapped['genre'].unique():
            print(f"  - {genre}")

        # Map unmapped to 'Education' (catch-all for misc content)
        genres_df['refined_genre'] = genres_df['refined_genre'].fillna('Education')

    return genres_df, genre_mapping, refined_system

def analyze_refined_distribution():
    """Analyze the distribution of refined genres."""

    refined_genres_df, _, refined_system = apply_refined_classification()

    print("=== Refined Genre Classification Analysis ===\n")

    # Show the refined taxonomy
    print("Refined Genre Taxonomy (8 Core Categories):")
    print("-" * 45)
    for refined_genre, original_genres in refined_system.items():
        count = len(refined_genres_df[refined_genres_df['refined_genre'] == refined_genre])
        print(f"{refined_genre} ({count} shows):")
        for orig in original_genres[:3]:  # Show first 3 examples
            print(f"  • {orig}")
        if len(original_genres) > 3:
            print(f"  • ... and {len(original_genres) - 3} more")
        print()

    # Distribution analysis
    refined_dist = refined_genres_df['refined_genre'].value_counts()

    print("=== Refined Genre Distribution ===")
    total_shows = len(refined_genres_df)

    for genre, count in refined_dist.items():
        percentage = (count / total_shows) * 100
        print(f"{genre:<18}: {count:2d} shows ({percentage:4.1f}%)")

    print(f"\nTotal shows: {total_shows}")
    print(f"Refined categories: {len(refined_dist)}")
    print(f"Major reduction: {len(refined_genres_df['genre'].unique())} → {len(refined_dist)} categories")

    # Show balance
    largest_percent = (refined_dist.iloc[0] / total_shows) * 100
    smallest_percent = (refined_dist.iloc[-1] / total_shows) * 100
    print(f"Category balance: {largest_percent:.1f}% (largest) to {smallest_percent:.1f}% (smallest)")

    return refined_dist

def export_refined_datasets():
    """Export all datasets with refined genre classification."""

    refined_genres_df, genre_mapping, refined_system = apply_refined_classification()

    # Create refined mapping for easy lookup
    refined_lookup = dict(zip(refined_genres_df['show_name'], refined_genres_df['refined_genre']))

    # Load and update platform datasets
    data_dir = Path("data_comprehensive_genres")
    output_dir = Path("data_refined_genres")
    output_dir.mkdir(exist_ok=True)

    # Update Spotify
    spotify = pd.read_csv(data_dir / "spotify_comprehensive_genres.csv")
    spotify['refined_genre'] = spotify['show_name'].map(refined_lookup)
    spotify.to_csv(output_dir / "spotify_refined_genres.csv", index=False)

    # Update YouTube
    youtube = pd.read_csv(data_dir / "youtube_comprehensive_genres.csv")
    youtube['refined_genre'] = youtube['show_name'].map(refined_lookup)
    youtube.to_csv(output_dir / "youtube_refined_genres.csv", index=False)

    # Update Amazon
    amazon = pd.read_csv(data_dir / "amazon_comprehensive_genres.csv")
    amazon['refined_genre'] = amazon['show_name'].map(refined_lookup)
    amazon.to_csv(output_dir / "amazon_refined_genres.csv", index=False)

    # Update iHeart
    iheart = pd.read_csv(data_dir / "iheart_comprehensive_genres.csv")
    iheart['refined_genre'] = iheart['show_name'].map(refined_lookup)
    iheart.to_csv(output_dir / "iheart_refined_genres.csv", index=False)

    # Export master refined mapping
    refined_master = refined_genres_df[['show_name', 'genre', 'refined_genre', 'source']].copy()
    refined_master.to_csv(output_dir / "refined_genre_master.csv", index=False)

    # Export refined taxonomy reference
    taxonomy_rows = []
    for refined_genre, original_genres in refined_system.items():
        for original in original_genres:
            taxonomy_rows.append({
                'original_genre': original,
                'refined_genre': refined_genre
            })

    taxonomy_df = pd.DataFrame(taxonomy_rows)
    taxonomy_df.to_csv(output_dir / "refined_taxonomy_mapping.csv", index=False)

    print(f"\nRefined datasets exported to: {output_dir}")
    print(f"Files created:")
    print(f"  - Platform datasets with refined genres")
    print(f"  - refined_genre_master.csv (all shows)")
    print(f"  - refined_taxonomy_mapping.csv (taxonomy reference)")

    return output_dir

def validate_refined_system():
    """Validate the refined classification system."""

    refined_genres_df, _, _ = apply_refined_classification()

    print("\n=== Validation Results ===")

    # Check coverage
    total_shows = len(refined_genres_df)
    shows_with_refined = refined_genres_df['refined_genre'].notna().sum()
    coverage = (shows_with_refined / total_shows) * 100

    print(f"Coverage: {coverage:.1f}% ({shows_with_refined}/{total_shows} shows)")

    # Genre balance analysis
    refined_dist = refined_genres_df['refined_genre'].value_counts()

    print("\nGenre Balance Analysis:")
    for i, (genre, count) in enumerate(refined_dist.items(), 1):
        percentage = (count / total_shows) * 100
        balance_status = "✓ Good" if 5 <= percentage <= 40 else "⚠ Check" if percentage < 5 else "⚠ High"
        print(f"  {i}. {genre:<18}: {percentage:4.1f}% ({count:2d} shows) {balance_status}")

    # Show distribution quality
    gini_coefficient = calculate_genre_balance(refined_dist.values)
    print(f"\nDistribution balance score: {(1-gini_coefficient)*100:.1f}% (higher = more balanced)")

def calculate_genre_balance(counts):
    """Calculate genre distribution balance (Gini coefficient)."""
    import numpy as np

    counts = np.array(sorted(counts))
    n = len(counts)
    cumsum = np.cumsum(counts)
    return (n + 1 - 2 * sum(cumsum) / cumsum[-1]) / n

if __name__ == "__main__":
    print("Creating Refined Genre Classification System")
    print("=" * 50)

    # Analyze current distribution and create refined system
    distribution = analyze_refined_distribution()

    print("\n" + "=" * 50)

    # Export refined datasets
    output_dir = export_refined_datasets()

    # Validate the system
    validate_refined_system()

    print(f"\nRefined genre classification complete!")
    print(f"Reduced complexity: 43 → 8 categories")
    print(f"Files available in: {output_dir}")