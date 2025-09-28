#!/usr/bin/env python3
"""
Cross-Platform Podcast Ranking System

This script creates a unified ranking system across Spotify, YouTube, Amazon, and iHeart
platforms by normalizing engagement metrics and calculating composite scores.
"""

import pandas as pd
import numpy as np
from pathlib import Path


def load_and_clean_data():
    """Load all platform datasets and clean them."""
    data_dir = Path("data")

    # Load Spotify data
    spotify = pd.read_csv(data_dir / "spotify.csv", skiprows=7)
    spotify.columns = ["show_name", "spotify_plays", "category"]
    spotify = spotify.dropna()
    spotify["spotify_plays"] = spotify["spotify_plays"].str.replace(",", "").astype(float)

    # Load YouTube data
    youtube = pd.read_csv(data_dir / "youtube.csv")
    youtube = youtube.rename(columns={
        "playlist_name": "show_name",
        "watchtime_hrs": "youtube_watchtime_hrs",
        "views": "youtube_views",
        "num_2025_videos": "youtube_videos"
    })

    # Filter for US podcasts only (assume missing countries are US)
    youtube = youtube[(youtube["FeatureCountry"] == "US") | (youtube["FeatureCountry"].isna())]

    # Load Amazon data
    amazon = pd.read_csv(data_dir / "amazon.csv", skiprows=2)
    amazon = amazon.dropna(subset=["Show Title"])
    amazon = amazon.rename(columns={
        "Show Title": "show_name",
        "Total Plays": "amazon_plays",
        "Customers": "amazon_customers",
        "Average Completion Rate": "amazon_completion_rate"
    })

    # Load iHeart data
    iheart = pd.read_csv(data_dir / "iheart_platform_nominations.csv", skiprows=2)
    iheart.columns = ["rank", "show_name", "iheart_listeners", "iheart_streams", "iheart_completion", "iheart_followers"]
    iheart = iheart.dropna(subset=["show_name"])

    # Clean numeric columns
    for col in ["iheart_listeners", "iheart_streams", "iheart_followers"]:
        iheart[col] = iheart[col].str.replace(",", "").str.replace(" ", "").astype(float)

    iheart["iheart_completion"] = iheart["iheart_completion"].str.replace("%", "").astype(float) / 100

    return spotify, youtube, amazon, iheart


def normalize_show_names(df, name_col="show_name"):
    """Standardize show names for cross-platform matching."""
    df = df.copy()
    df[name_col] = df[name_col].str.strip().str.lower()
    df[name_col] = df[name_col].str.replace(r"[^\w\s]", "", regex=True)
    df[name_col] = df[name_col].str.replace(r"\s+", " ", regex=True)
    return df


def calculate_platform_scores(spotify, youtube, amazon, iheart):
    """Calculate scores using three-component weighted system: consumption + platform reach + platform count."""

    # Store original data for total consumption calculation
    all_data = []

    # Collect all consumption data with platform weights for total consumption score
    platform_weights = {
        "youtube": 1.0,      # YouTube watch hours weighted as equivalent to plays
        "spotify": 1.0,      # Spotify plays
        "amazon": 1.0,       # Amazon plays
        "iheart": 1.0        # iHeart streams
    }

    # Add consumption data to each dataframe
    for _, row in spotify.iterrows():
        all_data.append({
            'show_name': row['show_name'],
            'platform': 'spotify',
            'consumption': row['spotify_plays']
        })

    for _, row in youtube.iterrows():
        all_data.append({
            'show_name': row['show_name'],
            'platform': 'youtube',
            'consumption': row['youtube_watchtime_hrs']
        })

    for _, row in amazon.iterrows():
        all_data.append({
            'show_name': row['show_name'],
            'platform': 'amazon',
            'consumption': row['amazon_plays']
        })

    for _, row in iheart.iterrows():
        all_data.append({
            'show_name': row['show_name'],
            'platform': 'iheart',
            'consumption': row['iheart_streams']
        })

    # Calculate platform reach scores (0-100 within each platform)
    spotify["platform_reach"] = (spotify["spotify_plays"] / spotify["spotify_plays"].max()) * 100
    youtube["platform_reach"] = (youtube["youtube_watchtime_hrs"] / youtube["youtube_watchtime_hrs"].max()) * 100
    amazon["platform_reach"] = (amazon["amazon_plays"] / amazon["amazon_plays"].max()) * 100
    iheart["platform_reach"] = (iheart["iheart_streams"] / iheart["iheart_streams"].max()) * 100

    # Store platform reach as the platform score for now (will be combined in create_unified_ranking)
    spotify["spotify_score"] = spotify["platform_reach"]
    youtube["youtube_score"] = youtube["platform_reach"]
    amazon["amazon_score"] = amazon["platform_reach"]
    iheart["iheart_score"] = iheart["platform_reach"]

    return spotify, youtube, amazon, iheart


def create_unified_ranking(spotify, youtube, amazon, iheart):
    """Create unified ranking using three-component weighted system."""

    # Normalize show names for matching
    spotify = normalize_show_names(spotify)
    youtube = normalize_show_names(youtube)
    amazon = normalize_show_names(amazon)
    iheart = normalize_show_names(iheart)

    # Start with all unique shows
    all_shows = set()
    all_shows.update(spotify["show_name"].tolist())
    all_shows.update(youtube["show_name"].tolist())
    all_shows.update(amazon["show_name"].tolist())
    all_shows.update(iheart["show_name"].tolist())

    # Create master dataframe
    ranking_df = pd.DataFrame({"show_name": list(all_shows)})

    # Merge platform data
    ranking_df = ranking_df.merge(spotify[["show_name", "spotify_score", "spotify_plays"]], on="show_name", how="left")
    ranking_df = ranking_df.merge(youtube[["show_name", "youtube_score", "youtube_watchtime_hrs", "youtube_views"]], on="show_name", how="left")
    ranking_df = ranking_df.merge(amazon[["show_name", "amazon_score", "amazon_plays", "amazon_customers"]], on="show_name", how="left")
    ranking_df = ranking_df.merge(iheart[["show_name", "iheart_score", "iheart_streams", "iheart_listeners"]], on="show_name", how="left")

    # Fill missing values with 0
    ranking_df = ranking_df.fillna(0)

    # Component 1: Total Consumption Score (50% weight)
    # Sum all raw consumption metrics across platforms with normalization
    ranking_df["total_consumption"] = (
        ranking_df["spotify_plays"] +
        ranking_df["youtube_watchtime_hrs"] +
        ranking_df["amazon_plays"] +
        ranking_df["iheart_streams"]
    )
    max_consumption = ranking_df["total_consumption"].max()
    ranking_df["consumption_score"] = (ranking_df["total_consumption"] / max_consumption) * 100

    # Component 2: Platform Reach Score (30% weight)
    # Average of platform-specific reach scores (already calculated as spotify_score etc.)
    score_cols = ["spotify_score", "youtube_score", "amazon_score", "iheart_score"]
    ranking_df["platforms_count"] = (ranking_df[score_cols] > 0).sum(axis=1)

    # Calculate average platform reach for shows that appear on platforms
    ranking_df["platform_reach_score"] = ranking_df[score_cols].sum(axis=1) / ranking_df["platforms_count"].replace(0, 1)

    # Component 3: Platform Count Score (20% weight)
    # Normalize platform count to 0-100 scale
    max_platforms = ranking_df["platforms_count"].max()
    ranking_df["platform_count_score"] = (ranking_df["platforms_count"] / max_platforms) * 100

    # Final Composite Score: Weighted sum of three components
    ranking_df["composite_score"] = (
        ranking_df["consumption_score"] * 0.5 +      # 50% total consumption
        ranking_df["platform_reach_score"] * 0.3 +   # 30% platform reach
        ranking_df["platform_count_score"] * 0.2     # 20% platform count
    )

    # Final ranking
    ranking_df = ranking_df.sort_values("composite_score", ascending=False)
    ranking_df["rank"] = range(1, len(ranking_df) + 1)

    return ranking_df


def main():
    """Generate cross-platform podcast rankings."""
    # Load data
    spotify, youtube, amazon, iheart = load_and_clean_data()

    # Calculate platform scores
    spotify, youtube, amazon, iheart = calculate_platform_scores(spotify, youtube, amazon, iheart)

    # Create unified ranking
    ranking_df = create_unified_ranking(spotify, youtube, amazon, iheart)

    # Save results
    output_cols = ["rank", "show_name", "composite_score",
                   "consumption_score", "platform_reach_score", "platform_count_score",
                   "total_consumption", "platforms_count",
                   "spotify_score", "youtube_score", "amazon_score", "iheart_score",
                   "spotify_plays", "youtube_watchtime_hrs", "amazon_plays", "iheart_streams"]

    ranking_df[output_cols].to_csv("podcast_cross_platform_rankings.csv", index=False)

    # Display top 25 with detailed metrics
    print("Top 25 Cross-Platform Podcast Rankings:")
    print("=" * 80)
    top_25 = ranking_df[output_cols].head(25)
    for _, row in top_25.iterrows():
        platforms = []
        metrics = []

        # Build platform list and metrics display
        if row["spotify_score"] > 0:
            platforms.append("Spotify")
            metrics.append(f"Spotify: {row['spotify_plays']:,.0f} plays")
        if row["youtube_score"] > 0:
            platforms.append("YouTube")
            metrics.append(f"YouTube: {row['youtube_watchtime_hrs']:,.0f}hrs watch")
        if row["amazon_score"] > 0:
            platforms.append("Amazon")
            metrics.append(f"Amazon: {row['amazon_plays']:,.0f} plays")
        if row["iheart_score"] > 0:
            platforms.append("iHeart")
            metrics.append(f"iHeart: {row['iheart_streams']:,.0f} streams")

        print(f"{row['rank']:2d}. {row['show_name'].title()}")
        print(f"    Composite Score: {row['composite_score']:.1f}")
        print(f"    Components: Consumption:{row['consumption_score']:.1f} " +
              f"Platform Reach:{row['platform_reach_score']:.1f} " +
              f"Platform Count:{row['platform_count_score']:.1f}")
        print(f"    Total Consumption: {row['total_consumption']:,.0f} | Platforms: {row['platforms_count']}")
        if metrics:
            print(f"    Raw Metrics: {' | '.join(metrics)}")
        print()


if __name__ == "__main__":
    main()