#!/usr/bin/env python3
"""
Updated comprehensive podcast ranking system with new data
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path

def normalize_show_name(name):
    """Normalize show name for matching across platforms."""
    if pd.isna(name):
        return ""

    # Convert to string and lowercase
    normalized = str(name).strip().lower()

    # Remove common podcast suffixes and qualifiers
    patterns_to_remove = [
        r'\bpodcast\b',
        r'\bshow\b',
        r'\bthe podcast\b',
        r'\bthe show\b',
        r'\bwith\s+[^,]+$',  # "with [host name]" at end
        r'\bw/\s+[^,]+$',    # "w/ [host name]" at end
    ]

    for pattern in patterns_to_remove:
        normalized = re.sub(pattern, '', normalized)

    # Remove all non-word/space characters
    normalized = re.sub(r"[^\w\s]", "", normalized)

    # Collapse multiple spaces to single space
    normalized = re.sub(r"\s+", " ", normalized)

    return normalized.strip()

def load_platform_data():
    """Load and normalize data from all platforms."""

    print("LOADING UPDATED PLATFORM DATA")
    print("=" * 40)

    data_dir = Path("data")

    # 1. Load Spotify data
    print("1. Loading Spotify data...")
    try:
        spotify = pd.read_csv(data_dir / "spotify.csv", skiprows=7)
        spotify.columns = ["rank", "show_name", "plays"]
        spotify["plays"] = spotify["plays"].str.replace(",", "").astype(float)
        spotify = spotify.dropna()
        spotify["normalized_name"] = spotify["show_name"].apply(normalize_show_name)
        print(f"   ✓ Loaded {len(spotify)} Spotify shows")
    except Exception as e:
        print(f"   ✗ Error loading Spotify: {e}")
        spotify = pd.DataFrame()

    # 2. Load YouTube data
    print("2. Loading YouTube data...")
    try:
        youtube = pd.read_csv(data_dir / "youtube.csv")
        youtube = youtube.dropna(subset=["playlist_name"])
        youtube["normalized_name"] = youtube["playlist_name"].apply(normalize_show_name)
        print(f"   ✓ Loaded {len(youtube)} YouTube shows")
    except Exception as e:
        print(f"   ✗ Error loading YouTube: {e}")
        youtube = pd.DataFrame()

    # 3. Load Amazon data
    print("3. Loading Amazon data...")
    try:
        amazon = pd.read_csv(data_dir / "amazon.csv")
        amazon = amazon.dropna(subset=["Show Title"])
        amazon["normalized_name"] = amazon["Show Title"].apply(normalize_show_name)
        print(f"   ✓ Loaded {len(amazon)} Amazon shows")
    except Exception as e:
        print(f"   ✗ Error loading Amazon: {e}")
        amazon = pd.DataFrame()

    # 4. Load Apple data
    print("4. Loading Apple data...")
    try:
        apple = pd.read_csv(data_dir / "apple.csv")
        apple = apple.dropna(subset=["Podcast"])
        apple["normalized_name"] = apple["Podcast"].apply(normalize_show_name)
        print(f"   ✓ Loaded {len(apple)} Apple shows")
    except Exception as e:
        print(f"   ✗ Error loading Apple: {e}")
        apple = pd.DataFrame()

    return spotify, youtube, amazon, apple

def load_mappings():
    """Load country and genre mappings."""

    print("\n5. Loading country and genre mappings...")

    # Load country mapping
    try:
        country_mapping = pd.read_csv("comprehensive_country_mapping_updated.csv")
        country_map = dict(zip(country_mapping["normalized_name"], country_mapping["country"]))
        print(f"   ✓ Loaded country mapping: {len(country_map)} shows")
    except FileNotFoundError:
        print("   ⚠ No country mapping found")
        country_map = {}

    # Load genre mapping
    try:
        genre_mapping = pd.read_csv("comprehensive_genre_mapping_updated.csv")

        # Standardize genre names to match our 8 categories
        genre_standardization = {
            "True Crime": "True Crime",
            "Comedy": "Comedy",
            "News": "News & Politics",
            "Society & Culture": "Society & Culture",
            "Education": "Education",
            "History": "Education",  # Merge History into Education
            "Interview & Talk": "Interview & Talk",
            "Kids & Family": "Education",  # Merge Kids into Education
            "Leisure": "Entertainment",  # Merge Leisure into Entertainment
            "Fiction": "Entertainment",  # Merge Fiction into Entertainment
            "Sports": "Sports",
            "Business": "Business",
            "Religion & Spirituality": "Society & Culture",  # Merge into Society & Culture
            "TV & Film": "Entertainment",  # Merge into Entertainment
            "Arts": "Entertainment"  # Merge into Entertainment
        }

        genre_mapping["standardized_genre"] = genre_mapping["genre"].map(genre_standardization).fillna("Other")
        genre_map = dict(zip(genre_mapping["normalized_name"], genre_mapping["standardized_genre"]))
        print(f"   ✓ Loaded genre mapping: {len(genre_map)} shows")
    except FileNotFoundError:
        print("   ⚠ No genre mapping found")
        genre_map = {}

    return country_map, genre_map

def create_unified_ranking():
    """Create unified cross-platform ranking with updated 4-component scoring."""

    print("\nCREATING UNIFIED CROSS-PLATFORM RANKING")
    print("=" * 50)

    # Load data
    spotify, youtube, amazon, apple = load_platform_data()
    country_map, genre_map = load_mappings()

    # Get all unique shows
    all_shows = set()
    if not spotify.empty:
        all_shows.update(spotify["normalized_name"].tolist())
    if not youtube.empty:
        all_shows.update(youtube["normalized_name"].tolist())
    if not amazon.empty:
        all_shows.update(amazon["normalized_name"].tolist())
    if not apple.empty:
        all_shows.update(apple["normalized_name"].tolist())

    print(f"Total unique shows: {len(all_shows)}")

    # Create master DataFrame
    ranking_df = pd.DataFrame({"show_name": list(all_shows)})

    # Merge platform data
    if not spotify.empty:
        spotify_metrics = spotify[["normalized_name", "plays"]].rename(columns={"plays": "spotify_plays"})
        ranking_df = ranking_df.merge(spotify_metrics, left_on="show_name", right_on="normalized_name", how="left")
        ranking_df = ranking_df.drop("normalized_name", axis=1)
    else:
        ranking_df["spotify_plays"] = 0

    if not youtube.empty:
        youtube_metrics = youtube[["normalized_name", "views"]].rename(columns={"views": "youtube_views"})
        ranking_df = ranking_df.merge(youtube_metrics, left_on="show_name", right_on="normalized_name", how="left")
        ranking_df = ranking_df.drop("normalized_name", axis=1)
    else:
        ranking_df["youtube_views"] = 0

    if not amazon.empty:
        amazon_metrics = amazon[["normalized_name", "Total Plays"]].rename(columns={"Total Plays": "amazon_plays"})
        ranking_df = ranking_df.merge(amazon_metrics, left_on="show_name", right_on="normalized_name", how="left")
        ranking_df = ranking_df.drop("normalized_name", axis=1)
    else:
        ranking_df["amazon_plays"] = 0

    if not apple.empty:
        apple_metrics = apple[["normalized_name", "Plays (>30s)"]].rename(columns={"Plays (>30s)": "apple_plays"})
        ranking_df = ranking_df.merge(apple_metrics, left_on="show_name", right_on="normalized_name", how="left")
        ranking_df = ranking_df.drop("normalized_name", axis=1)
    else:
        ranking_df["apple_plays"] = 0

    # Fill missing values with 0
    metric_columns = ["spotify_plays", "youtube_views", "amazon_plays", "apple_plays"]
    for col in metric_columns:
        if col in ranking_df.columns:
            ranking_df[col] = ranking_df[col].fillna(0)
        else:
            ranking_df[col] = 0

    # Add country and genre information
    ranking_df["country"] = ranking_df["show_name"].map(country_map).fillna("Unknown")
    ranking_df["genre"] = ranking_df["show_name"].map(genre_map).fillna("Other")

    # Calculate platform presence
    ranking_df["platforms_present"] = (
        (ranking_df["spotify_plays"] > 0).astype(int) +
        (ranking_df["youtube_views"] > 0).astype(int) +
        (ranking_df["amazon_plays"] > 0).astype(int) +
        (ranking_df["apple_plays"] > 0).astype(int)
    )

    # Filter to shows with at least some data
    ranking_df = ranking_df[ranking_df["platforms_present"] > 0].copy()
    print(f"Shows with data: {len(ranking_df)}")

    # Calculate total consumption (normalized across platforms)
    ranking_df["total_consumption"] = (
        ranking_df["spotify_plays"] +
        ranking_df["youtube_views"] +
        ranking_df["amazon_plays"] +
        ranking_df["apple_plays"]
    )

    # 1. Total Consumption Score (50% weight)
    max_consumption = ranking_df["total_consumption"].max()
    ranking_df["consumption_score"] = (ranking_df["total_consumption"] / max_consumption * 100)

    # 2. Platform Reach Score (20% weight) - Best single platform performance
    platform_scores = []
    for _, row in ranking_df.iterrows():
        scores = []
        if row["spotify_plays"] > 0:
            scores.append(row["spotify_plays"] / ranking_df["spotify_plays"].max() * 100)
        if row["youtube_views"] > 0:
            scores.append(row["youtube_views"] / ranking_df["youtube_views"].max() * 100)
        if row["amazon_plays"] > 0:
            scores.append(row["amazon_plays"] / ranking_df["amazon_plays"].max() * 100)
        if row["apple_plays"] > 0:
            scores.append(row["apple_plays"] / ranking_df["apple_plays"].max() * 100)

        platform_scores.append(max(scores) if scores else 0)

    ranking_df["platform_reach_score"] = platform_scores

    # 3. Platform Count Score (20% weight)
    max_platforms = ranking_df["platforms_present"].max()
    ranking_df["platform_count_score"] = (ranking_df["platforms_present"] / max_platforms * 100)

    # 4. Within-Genre Popularity Score (10% weight) - Consumption-based
    genre_scores = []
    for _, row in ranking_df.iterrows():
        genre = row["genre"]
        genre_shows = ranking_df[ranking_df["genre"] == genre]

        if len(genre_shows) > 1:
            # Consumption-based percentile within genre
            genre_rank = (genre_shows["total_consumption"] <= row["total_consumption"]).mean() * 100
        else:
            # Single show in genre gets full score
            genre_rank = 100.0

        genre_scores.append(genre_rank)

    ranking_df["genre_rank_score"] = genre_scores

    # Final Composite Score: Weighted sum of four components
    ranking_df["composite_score"] = (
        ranking_df["consumption_score"] * 0.5 +      # 50% total consumption
        ranking_df["platform_reach_score"] * 0.2 +   # 20% platform reach
        ranking_df["platform_count_score"] * 0.2 +   # 20% platform count
        ranking_df["genre_rank_score"] * 0.1         # 10% within-genre popularity
    )

    # Final ranking
    ranking_df = ranking_df.sort_values("composite_score", ascending=False)
    ranking_df["rank"] = range(1, len(ranking_df) + 1)

    print(f"Final rankings: {len(ranking_df)} shows")

    # Display rankings summary
    print(f"\nTOP 10 GLOBAL PODCAST RANKINGS:")
    print("=" * 60)

    top_10 = ranking_df.head(10)
    for _, row in top_10.iterrows():
        platforms = []
        metrics = []

        if row["spotify_plays"] > 0:
            platforms.append("Spotify")
            metrics.append(f"Spotify: {row['spotify_plays']:,.0f} plays")
        if row["youtube_views"] > 0:
            platforms.append("YouTube")
            metrics.append(f"YouTube: {row['youtube_views']:,.0f} views")
        if row["amazon_plays"] > 0:
            platforms.append("Amazon")
            metrics.append(f"Amazon: {row['amazon_plays']:,.0f} plays")
        if row["apple_plays"] > 0:
            platforms.append("Apple")
            metrics.append(f"Apple: {row['apple_plays']:,.0f} plays")

        print(f"{row['rank']:2d}. {row['show_name'].title()}")
        print(f"    Score: {row['composite_score']:.1f} | Genre: {row['genre']} | Country: {row['country']}")
        print(f"    Platforms: {len(platforms)} ({', '.join(platforms)})")
        print(f"    Total Consumption: {row['total_consumption']:,.0f}")
        print(f"    Metrics: {' | '.join(metrics)}")
        print()

    return ranking_df

def save_final_ranking(ranking_df):
    """Save final ranking to CSV."""

    print("SAVING FINAL RANKING")
    print("=" * 25)

    # Prepare output columns
    output_columns = [
        "rank", "show_name", "composite_score", "genre", "country",
        "consumption_score", "platform_reach_score", "platform_count_score", "genre_rank_score",
        "total_consumption", "platforms_present",
        "spotify_plays", "youtube_views", "amazon_plays", "apple_plays"
    ]

    # Save to CSV
    final_ranking = ranking_df[output_columns]
    final_ranking.to_csv("updated_podcast_cross_platform_rankings.csv", index=False)

    print(f"✓ Saved final ranking: updated_podcast_cross_platform_rankings.csv")
    print(f"  Total shows ranked: {len(final_ranking)}")

    # Show summary statistics
    country_dist = ranking_df["country"].value_counts()
    genre_dist = ranking_df["genre"].value_counts()
    platform_dist = ranking_df["platforms_present"].value_counts()

    print(f"\nSUMMARY STATISTICS:")
    print(f"  Countries represented: {len(country_dist)}")
    print(f"  Top countries: {', '.join(country_dist.head(5).index.tolist())}")
    print(f"  Genres represented: {len(genre_dist)}")
    print(f"  Top genres: {', '.join(genre_dist.head(3).index.tolist())}")
    print(f"  Multi-platform shows: {sum(platform_dist[platform_dist.index > 1])}")

    return final_ranking

if __name__ == "__main__":
    # Create unified ranking
    ranking_df = create_unified_ranking()

    # Save final results
    final_ranking = save_final_ranking(ranking_df)

    print(f"\n🎯 UPDATED PODCAST RANKING SYSTEM COMPLETE!")
    print(f"   Ready for analysis with {len(final_ranking)} globally ranked podcasts")