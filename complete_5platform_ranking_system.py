#!/usr/bin/env python3
"""
Complete 5-platform podcast ranking system with updated data
Includes: Spotify, YouTube, Amazon, Apple, iHeart
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

def load_all_platform_data():
    """Load and normalize data from all 5 platforms."""

    print("LOADING COMPLETE 5-PLATFORM DATA")
    print("=" * 45)

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

    # 5. Load iHeart data (NEW!)
    print("5. Loading iHeart data...")
    try:
        iheart = pd.read_csv(data_dir / "iheart_platform_nominations.csv")
        iheart = iheart.dropna(subset=["Show title"])
        iheart["normalized_name"] = iheart["Show title"].apply(normalize_show_name)

        # Clean numeric columns
        iheart["TOTAL STREAMS - YTD"] = iheart["TOTAL STREAMS - YTD"].astype(float)
        iheart["UNIQUE LISTENERS - YTD"] = iheart["UNIQUE LISTENERS - YTD"].astype(float)

        print(f"   ✓ Loaded {len(iheart)} iHeart shows")
    except Exception as e:
        print(f"   ✗ Error loading iHeart: {e}")
        iheart = pd.DataFrame()

    return spotify, youtube, amazon, apple, iheart

def load_updated_mappings():
    """Load the most comprehensive country and genre mappings."""

    print("\n6. Loading comprehensive mappings...")

    # Load final mappings if they exist, otherwise use available ones
    try:
        country_mapping = pd.read_csv("comprehensive_country_mapping_complete.csv")
        country_map = dict(zip(country_mapping["normalized_name"], country_mapping["country"]))
        print(f"   ✓ Loaded final country mapping: {len(country_map)} shows")
    except FileNotFoundError:
        try:
            country_mapping = pd.read_csv("comprehensive_country_mapping_updated.csv")
            country_map = dict(zip(country_mapping["normalized_name"], country_mapping["country"]))
            print(f"   ✓ Loaded comprehensive country mapping: {len(country_map)} shows")
        except FileNotFoundError:
            print("   ⚠ No country mapping found")
            country_map = {}

    # Load genre mapping - prioritize comprehensive mapping
    try:
        genre_mapping = pd.read_csv("final_genre_mapping_complete_all.csv")

        # Standardize genre names to our target categories
        genre_standardization = {
            "True Crime": "True Crime",
            "Comedy": "Comedy",
            "News": "News & Politics",
            "News & Politics": "News & Politics",
            "Society & Culture": "Society & Culture",
            "Education": "Education",
            "History": "Education",  # Merge History into Education
            "Interview & Talk": "Interview & Talk",
            "Kids & Family": "Education",  # Merge Kids into Education
            "Leisure": "Entertainment",  # Merge Leisure into Entertainment
            "Fiction": "Entertainment",  # Merge Fiction into Entertainment
            "Entertainment": "Entertainment",
            "Sports": "Sports",
            "Business": "Business",
            "Religion & Spirituality": "Society & Culture",  # Merge into Society & Culture
            "TV & Film": "Entertainment",  # Merge into Entertainment
            "Arts": "Entertainment"  # Merge into Entertainment
        }

        genre_mapping["standardized_genre"] = genre_mapping["genre"].map(genre_standardization).fillna("Other")
        genre_map = dict(zip(genre_mapping["normalized_name"], genre_mapping["standardized_genre"]))
        print(f"   ✓ Loaded comprehensive genre mapping: {len(genre_map)} shows")
    except FileNotFoundError:
        try:
            genre_mapping = pd.read_csv("final_genre_mapping.csv")
            genre_mapping["standardized_genre"] = genre_mapping["genre"].map(genre_standardization).fillna("Other")
            genre_map = dict(zip(genre_mapping["normalized_name"], genre_mapping["standardized_genre"]))
            print(f"   ✓ Loaded final genre mapping: {len(genre_map)} shows")
        except FileNotFoundError:
            try:
                genre_mapping = pd.read_csv("comprehensive_genre_mapping_updated.csv")
                genre_mapping["standardized_genre"] = genre_mapping["genre"].fillna("Other")
                genre_map = dict(zip(genre_mapping["normalized_name"], genre_mapping["standardized_genre"]))
                print(f"   ✓ Loaded comprehensive genre mapping: {len(genre_map)} shows")
            except FileNotFoundError:
                print("   ⚠ No genre mapping found")
                genre_map = {}

    return country_map, genre_map

def create_comprehensive_classification_updates():
    """Apply final classification updates for missing data."""

    # Updated country mappings based on research
    country_updates = {
        "the daily": "US",
        "crime junkie": "US",
        "dateline nbc": "US",
        "morbid": "US",
        "mrballen strange dark mysterious stories": "US",
        "the meidastouch": "US",
        "the joe rogan experience": "US",
        "good mythical morning": "US",
        "stuff you should know": "US",
        "new heights": "US",
        "on purpose": "US",
        "the breakfast club": "US",
        "las culturistas": "US",
        "are you a charlotte": "US",
        "the steve harvey morning show": "US",
        "the ben shapiro": "US",
        "48 hours": "US",
        "my favorite murder": "US",
        "the herd with colin cowherd": "US",
        "conan obrien needs a friend": "US",
        "call her daddy": "US",
        "small town murder": "US",
        "not gonna lie with kylie kelce": "US",
        "wait wait dont tell me": "US",
        "up first from npr": "US",
        "the mel robbins": "US",
        "shawn ryan": "US",
        "the ramsey": "US",
        "bad friends": "US",
        "armchair expert": "US",
        "good hang": "US"
    }

    # Updated genre mappings
    genre_updates = {
        "the meidastouch": "News & Politics",
        "the joe rogan experience": "Interview & Talk",
        "good mythical morning": "Comedy",
        "stuff you should know": "Education",
        "new heights": "Sports",
        "on purpose": "Interview & Talk",
        "the breakfast club": "Entertainment",
        "las culturistas": "Comedy",
        "are you a charlotte": "Comedy",
        "the steve harvey morning show": "Entertainment",
        "the ben shapiro": "News & Politics",
        "my favorite murder": "True Crime",
        "the herd with colin cowherd": "Sports",
        "call her daddy": "Interview & Talk",
        "small town murder": "Comedy",
        "not gonna lie with kylie kelce": "Sports",
        "wait wait dont tell me": "Comedy",
        "up first from npr": "News & Politics",
        "the mel robbins": "Interview & Talk",
        "the ramsey": "Business",
        "bad friends": "Comedy",
        "armchair expert": "Interview & Talk",
        "good hang": "Comedy"
    }

    return country_updates, genre_updates

def create_unified_5platform_ranking():
    """Create unified ranking across all 5 platforms with advanced scoring."""

    print("\nCREATING UNIFIED 5-PLATFORM RANKING")
    print("=" * 50)

    # Load data
    spotify, youtube, amazon, apple, iheart = load_all_platform_data()
    country_map, genre_map = load_updated_mappings()

    # Get classification updates
    country_updates, genre_updates = create_comprehensive_classification_updates()

    # Apply updates to mappings
    country_map.update(country_updates)
    genre_map.update(genre_updates)

    # Get all unique shows across all platforms
    all_shows = set()
    if not spotify.empty:
        all_shows.update(spotify["normalized_name"].tolist())
    if not youtube.empty:
        all_shows.update(youtube["normalized_name"].tolist())
    if not amazon.empty:
        all_shows.update(amazon["normalized_name"].tolist())
    if not apple.empty:
        all_shows.update(apple["normalized_name"].tolist())
    if not iheart.empty:
        all_shows.update(iheart["normalized_name"].tolist())

    print(f"Total unique shows across 5 platforms: {len(all_shows)}")

    # Create master DataFrame
    ranking_df = pd.DataFrame({"show_name": list(all_shows)})

    # Merge platform data
    if not spotify.empty:
        # Aggregate Spotify data by normalized_name to handle potential duplicates
        spotify_metrics = spotify.groupby("normalized_name")["plays"].sum().reset_index()
        spotify_metrics = spotify_metrics.rename(columns={"plays": "spotify_plays"})
        ranking_df = ranking_df.merge(spotify_metrics, left_on="show_name", right_on="normalized_name", how="left")
        ranking_df = ranking_df.drop("normalized_name", axis=1)
    else:
        ranking_df["spotify_plays"] = 0

    if not youtube.empty:
        # Aggregate YouTube data by normalized_name to handle potential duplicates
        youtube_metrics = youtube.groupby("normalized_name")["views"].sum().reset_index()
        youtube_metrics = youtube_metrics.rename(columns={"views": "youtube_views"})
        ranking_df = ranking_df.merge(youtube_metrics, left_on="show_name", right_on="normalized_name", how="left")
        ranking_df = ranking_df.drop("normalized_name", axis=1)
    else:
        ranking_df["youtube_views"] = 0

    if not amazon.empty:
        # Aggregate Amazon data by normalized_name to handle duplicates (e.g., "Morbid")
        amazon_metrics = amazon.groupby("normalized_name")["Total Plays"].sum().reset_index()
        amazon_metrics = amazon_metrics.rename(columns={"Total Plays": "amazon_plays"})
        ranking_df = ranking_df.merge(amazon_metrics, left_on="show_name", right_on="normalized_name", how="left")
        ranking_df = ranking_df.drop("normalized_name", axis=1)
    else:
        ranking_df["amazon_plays"] = 0

    if not apple.empty:
        # Aggregate Apple data by normalized_name to handle potential duplicates
        apple_metrics = apple.groupby("normalized_name")["Plays (>30s)"].sum().reset_index()
        apple_metrics = apple_metrics.rename(columns={"Plays (>30s)": "apple_plays"})
        ranking_df = ranking_df.merge(apple_metrics, left_on="show_name", right_on="normalized_name", how="left")
        ranking_df = ranking_df.drop("normalized_name", axis=1)
    else:
        ranking_df["apple_plays"] = 0

    if not iheart.empty:
        # Aggregate iHeart data by normalized_name to handle potential duplicates
        iheart_metrics = iheart.groupby("normalized_name")["TOTAL STREAMS - YTD"].sum().reset_index()
        iheart_metrics = iheart_metrics.rename(columns={"TOTAL STREAMS - YTD": "iheart_streams"})
        ranking_df = ranking_df.merge(iheart_metrics, left_on="show_name", right_on="normalized_name", how="left")
        ranking_df = ranking_df.drop("normalized_name", axis=1)
    else:
        ranking_df["iheart_streams"] = 0

    # Fill missing values with 0
    metric_columns = ["spotify_plays", "youtube_views", "amazon_plays", "apple_plays", "iheart_streams"]
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
        (ranking_df["apple_plays"] > 0).astype(int) +
        (ranking_df["iheart_streams"] > 0).astype(int)
    )

    # Filter to shows with at least some data
    ranking_df = ranking_df[ranking_df["platforms_present"] > 0].copy()
    print(f"Shows with data across platforms: {len(ranking_df)}")

    # Apply geographical adjustment factors for global vs US consumption
    # YouTube: 7.5% factor (global -> US estimate, additional 50% discount applied)
    # Amazon: 65% factor (global -> US estimate)
    # Spotify, Apple, iHeart: 100% (already US-only data)
    ranking_df["youtube_views_us"] = ranking_df["youtube_views"] * 0.075
    ranking_df["amazon_plays_us"] = ranking_df["amazon_plays"] * 0.65

    # Calculate total consumption (normalized to US market)
    ranking_df["total_consumption"] = (
        ranking_df["spotify_plays"] +
        ranking_df["youtube_views_us"] +
        ranking_df["amazon_plays_us"] +
        ranking_df["apple_plays"] +
        ranking_df["iheart_streams"]
    )

    # 1. Total Consumption Score (65% weight)
    max_consumption = ranking_df["total_consumption"].max()
    ranking_df["consumption_score"] = (ranking_df["total_consumption"] / max_consumption * 100)

    # 2. Platform Reach Score (20% weight) - Best single platform performance
    # Use US-adjusted values for YouTube and Amazon
    platform_scores = []
    for _, row in ranking_df.iterrows():
        scores = []
        if row["spotify_plays"] > 0:
            scores.append(row["spotify_plays"] / ranking_df["spotify_plays"].max() * 100)
        if row["youtube_views_us"] > 0:
            scores.append(row["youtube_views_us"] / ranking_df["youtube_views_us"].max() * 100)
        if row["amazon_plays_us"] > 0:
            scores.append(row["amazon_plays_us"] / ranking_df["amazon_plays_us"].max() * 100)
        if row["apple_plays"] > 0:
            scores.append(row["apple_plays"] / ranking_df["apple_plays"].max() * 100)
        if row["iheart_streams"] > 0:
            scores.append(row["iheart_streams"] / ranking_df["iheart_streams"].max() * 100)

        platform_scores.append(max(scores) if scores else 0)

    ranking_df["platform_reach_score"] = platform_scores

    # 3. Platform Count Score (5% weight)
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
        ranking_df["consumption_score"] * 0.65 +     # 65% total consumption
        ranking_df["platform_reach_score"] * 0.2 +   # 20% platform reach
        ranking_df["platform_count_score"] * 0.05 +  # 5% platform count
        ranking_df["genre_rank_score"] * 0.1         # 10% within-genre popularity
    )

    # Final ranking
    ranking_df = ranking_df.sort_values("composite_score", ascending=False)
    ranking_df["rank"] = range(1, len(ranking_df) + 1)

    print(f"Final 5-platform rankings: {len(ranking_df)} shows")

    # Display top rankings
    print(f"\nTOP 15 US-NORMALIZED 5-PLATFORM PODCAST RANKINGS:")
    print("=" * 75)

    top_15 = ranking_df.head(15)
    for _, row in top_15.iterrows():
        platforms = []
        metrics = []

        if row["spotify_plays"] > 0:
            platforms.append("Spotify")
            metrics.append(f"Spotify: {row['spotify_plays']:,.0f} plays")
        if row["youtube_views"] > 0:
            platforms.append("YouTube")
            metrics.append(f"YouTube: {row['youtube_views_us']:,.0f} US est. ({row['youtube_views']:,.0f} global)")
        if row["amazon_plays"] > 0:
            platforms.append("Amazon")
            metrics.append(f"Amazon: {row['amazon_plays_us']:,.0f} US est. ({row['amazon_plays']:,.0f} global)")
        if row["apple_plays"] > 0:
            platforms.append("Apple")
            metrics.append(f"Apple: {row['apple_plays']:,.0f} plays")
        if row["iheart_streams"] > 0:
            platforms.append("iHeart")
            metrics.append(f"iHeart: {row['iheart_streams']:,.0f} streams")

        print(f"{row['rank']:2d}. {row['show_name'].title()}")
        print(f"    Score: {row['composite_score']:.1f} | Genre: {row['genre']} | Country: {row['country']}")
        print(f"    Platforms: {len(platforms)} ({', '.join(platforms)})")
        print(f"    Total Consumption: {row['total_consumption']:,.0f}")
        if metrics:
            print(f"    Top Metrics: {' | '.join(metrics[:3])}")  # Show top 3 metrics
        print()

    return ranking_df

def save_final_5platform_ranking(ranking_df):
    """Save the final comprehensive 5-platform ranking."""

    print("SAVING FINAL 5-PLATFORM RANKING")
    print("=" * 40)

    # Prepare output columns (include both original and US-adjusted values)
    output_columns = [
        "rank", "show_name", "composite_score", "genre", "country",
        "consumption_score", "platform_reach_score", "platform_count_score", "genre_rank_score",
        "total_consumption", "platforms_present",
        "spotify_plays", "youtube_views", "youtube_views_us", "amazon_plays", "amazon_plays_us", "apple_plays", "iheart_streams"
    ]

    # Save to CSV
    final_ranking = ranking_df[output_columns]
    final_ranking.to_csv("final_5platform_podcast_rankings.csv", index=False)

    print(f"✅ Saved final ranking: final_5platform_podcast_rankings.csv")
    print(f"   Total shows ranked: {len(final_ranking)}")

    # Show comprehensive statistics
    country_dist = ranking_df["country"].value_counts()
    genre_dist = ranking_df["genre"].value_counts()
    platform_dist = ranking_df["platforms_present"].value_counts()

    print(f"\nCOMPREHENSIVE STATISTICS:")
    print(f"  📊 Shows ranked: {len(final_ranking)}")
    print(f"  🌍 Countries: {len(country_dist)} ({', '.join(country_dist.head(5).index.tolist())})")
    print(f"  🎭 Genres: {len(genre_dist)} ({', '.join(genre_dist.head(3).index.tolist())})")
    print(f"  📱 Multi-platform shows (2+): {sum(platform_dist[platform_dist.index > 1])}")
    print(f"  🏆 5-platform shows: {platform_dist.get(5, 0)}")
    print(f"  🥉 4-platform shows: {platform_dist.get(4, 0)}")
    print(f"  🥈 3-platform shows: {platform_dist.get(3, 0)}")

    # Show unknown classifications remaining
    unknown_countries = len(ranking_df[ranking_df["country"] == "Unknown"])
    other_genres = len(ranking_df[ranking_df["genre"] == "Other"])

    classification_completeness = (len(ranking_df) - unknown_countries - other_genres) / len(ranking_df) * 100
    print(f"\n  🔍 Classification completeness: {classification_completeness:.1f}%")
    print(f"     Unknown countries: {unknown_countries}")
    print(f"     Other genres: {other_genres}")

    return final_ranking

if __name__ == "__main__":
    # Create comprehensive 5-platform ranking
    ranking_df = create_unified_5platform_ranking()

    # Save final results
    final_ranking = save_final_5platform_ranking(ranking_df)

    print(f"\n🎯 COMPLETE 5-PLATFORM PODCAST RANKING SYSTEM FINISHED!")
    print(f"   📋 Final CSV: final_5platform_podcast_rankings.csv")
    print(f"   🌟 {len(final_ranking)} globally ranked podcasts across 5 platforms")
    print(f"   🚀 Ready for comprehensive cross-platform analysis!")