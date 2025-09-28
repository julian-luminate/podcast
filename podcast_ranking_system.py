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
            'consumption': row['youtube_views']
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
    youtube["platform_reach"] = (youtube["youtube_views"] / youtube["youtube_views"].max()) * 100
    amazon["platform_reach"] = (amazon["amazon_plays"] / amazon["amazon_plays"].max()) * 100
    iheart["platform_reach"] = (iheart["iheart_streams"] / iheart["iheart_streams"].max()) * 100

    # Store platform reach as the platform score for now (will be combined in create_unified_ranking)
    spotify["spotify_score"] = spotify["platform_reach"]
    youtube["youtube_score"] = youtube["platform_reach"]
    amazon["amazon_score"] = amazon["platform_reach"]
    iheart["iheart_score"] = iheart["platform_reach"]

    return spotify, youtube, amazon, iheart


def create_unified_ranking(spotify, youtube, amazon, iheart):
    """Create unified ranking using four-component weighted system."""

    # Load union genre mapping (platform + research + Tavily)
    try:
        union_mapping_df = pd.read_csv("union_genre_mapping.csv")
        genre_map = dict(zip(union_mapping_df['normalized_name'], union_mapping_df['final_genre']))
        print(f"Using union genre mapping ({len(genre_map)} shows mapped)")
    except FileNotFoundError:
        # Fallback to Tavily-researched genres
        try:
            tavily_mapping_df = pd.read_csv("tavily_normalized_genre_mapping.csv")
            genre_map = dict(zip(tavily_mapping_df['normalized_name'], tavily_mapping_df['tavily_genre']))
            print(f"Using Tavily-researched genres ({len(genre_map)} shows mapped)")
        except FileNotFoundError:
            # Fallback to refined genres
            genre_mapping_df = pd.read_csv("data_refined_genres/normalized_genre_mapping.csv")
            genre_map = dict(zip(genre_mapping_df['normalized_name'], genre_mapping_df['refined_genre']))
            print(f"Using refined genres ({len(genre_map)} shows mapped)")

    # Load comprehensive country mapping (explicit + Wikipedia research)
    try:
        country_mapping_df = pd.read_csv("comprehensive_country_mapping.csv")
        country_map = dict(zip(country_mapping_df['normalized_name'], country_mapping_df['country']))
        print(f"Using comprehensive country mapping ({len(country_map)} shows mapped)")
    except FileNotFoundError:
        # Fallback to basic country mapping
        try:
            country_mapping_df = pd.read_csv("country_mapping.csv")
            country_map = dict(zip(country_mapping_df['normalized_name'], country_mapping_df['country']))
            print(f"Using basic country mapping ({len(country_map)} shows mapped)")
        except FileNotFoundError:
            print("No country mapping found, shows will display without country information")
            country_map = {}

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
    ranking_df = ranking_df.merge(youtube[["show_name", "youtube_score", "youtube_views"]], on="show_name", how="left")
    ranking_df = ranking_df.merge(amazon[["show_name", "amazon_score", "amazon_plays", "amazon_customers"]], on="show_name", how="left")
    ranking_df = ranking_df.merge(iheart[["show_name", "iheart_score", "iheart_streams", "iheart_listeners"]], on="show_name", how="left")

    # Add genre information
    ranking_df["genre"] = ranking_df["show_name"].map(genre_map)

    # Add country information
    ranking_df["country"] = ranking_df["show_name"].map(country_map)

    # Fill missing numerical values with 0, preserve genre strings
    numeric_cols = ["spotify_score", "spotify_plays", "youtube_score", "youtube_views",
                   "amazon_score", "amazon_plays", "amazon_customers",
                   "iheart_score", "iheart_streams", "iheart_listeners"]

    for col in numeric_cols:
        if col in ranking_df.columns:
            ranking_df[col] = ranking_df[col].fillna(0)

    # Fill missing genre with 'Other'
    ranking_df["genre"] = ranking_df["genre"].fillna("Other")

    # Fill missing country with 'Unknown'
    ranking_df["country"] = ranking_df["country"].fillna("Unknown")

    # Component 1: Total Consumption Score (50% weight)
    # Sum all raw consumption metrics across platforms with normalization
    ranking_df["total_consumption"] = (
        ranking_df["spotify_plays"] +
        ranking_df["youtube_views"] +
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

    # Component 3: Platform Count Score (10% weight)
    # Normalize platform count to 0-100 scale
    max_platforms = ranking_df["platforms_count"].max()
    ranking_df["platform_count_score"] = (ranking_df["platforms_count"] / max_platforms) * 100

    # Component 4: Within-Genre Popularity Score (20% weight)
    # Score shows within their genre based on consumption (normalized 0-100)
    ranking_df["genre_rank_score"] = 0.0

    for genre in ranking_df["genre"].unique():
        if pd.notna(genre) and genre != "":
            genre_mask = ranking_df["genre"] == genre
            genre_shows = ranking_df[genre_mask]

            if len(genre_shows) > 1:
                # Score within genre based on consumption (highest consumption = 100)
                max_genre_consumption = genre_shows["total_consumption"].max()

                if max_genre_consumption > 0:
                    # Normalize consumption within genre to 0-100 scale
                    genre_score = (genre_shows["total_consumption"] / max_genre_consumption) * 100
                    ranking_df.loc[genre_mask, "genre_rank_score"] = genre_score
                else:
                    # All shows have zero consumption in genre
                    ranking_df.loc[genre_mask, "genre_rank_score"] = 0.0
            else:
                # Single show in genre gets full score
                ranking_df.loc[genre_mask, "genre_rank_score"] = 100.0

    # Final Composite Score: Weighted sum of four components
    ranking_df["composite_score"] = (
        ranking_df["consumption_score"] * 0.5 +      # 50% total consumption
        ranking_df["platform_reach_score"] * 0.2 +   # 20% platform reach
        ranking_df["platform_count_score"] * 0.2 +   # 20% platform count
        ranking_df["genre_rank_score"] * 0.1         # 10% within-genre popularity
    )

    # Include shows from all countries (no filtering)
    print(f"Total shows across all countries: {len(ranking_df)} shows")

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
    output_cols = ["rank", "show_name", "composite_score", "genre", "country",
                   "consumption_score", "platform_reach_score", "platform_count_score", "genre_rank_score",
                   "total_consumption", "platforms_count",
                   "spotify_score", "youtube_score", "amazon_score", "iheart_score",
                   "spotify_plays", "youtube_views", "amazon_plays", "iheart_streams"]

    ranking_df[output_cols].to_csv("podcast_cross_platform_rankings.csv", index=False)

    # Display full rankings with detailed metrics
    print("Global Cross-Platform Podcast Rankings:")
    print("=" * 80)
    all_rankings = ranking_df[output_cols]
    for _, row in all_rankings.iterrows():
        platforms = []
        metrics = []

        # Build platform list and metrics display
        if row["spotify_score"] > 0:
            platforms.append("Spotify")
            metrics.append(f"Spotify: {row['spotify_plays']:,.0f} plays")
        if row["youtube_score"] > 0:
            platforms.append("YouTube")
            metrics.append(f"YouTube: {row['youtube_views']:,.0f} views")
        if row["amazon_score"] > 0:
            platforms.append("Amazon")
            metrics.append(f"Amazon: {row['amazon_plays']:,.0f} plays")
        if row["iheart_score"] > 0:
            platforms.append("iHeart")
            metrics.append(f"iHeart: {row['iheart_streams']:,.0f} streams")

        print(f"{row['rank']:2d}. {row['show_name'].title()}")
        print(f"    Composite Score: {row['composite_score']:.1f} | Genre: {row['genre']} | Country: {row['country']}")
        print(f"    Components: Consumption:{row['consumption_score']:.1f} " +
              f"Platform Reach:{row['platform_reach_score']:.1f} " +
              f"Platform Count:{row['platform_count_score']:.1f} " +
              f"Genre Rank:{row['genre_rank_score']:.1f}")
        print(f"    Total Consumption: {row['total_consumption']:,.0f} | Platforms: {row['platforms_count']}")
        if metrics:
            print(f"    Raw Metrics: {' | '.join(metrics)}")
        print()


if __name__ == "__main__":
    main()