#!/usr/bin/env python3
"""
Rebuild complete podcast analysis with updated data
"""

import pandas as pd
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

def load_and_process_data():
    """Load and process all available data files."""

    print("REBUILDING PODCAST ANALYSIS WITH UPDATED DATA")
    print("=" * 60)

    data_dir = Path("data")
    all_shows = {}

    # 1. Load Spotify data
    print("\n1. Processing Spotify data...")
    try:
        spotify = pd.read_csv(data_dir / "spotify.csv", skiprows=7)
        spotify.columns = ["rank", "show_name", "plays"]

        # Clean plays column (remove commas)
        spotify["plays"] = spotify["plays"].str.replace(",", "").astype(float)
        spotify = spotify.dropna()

        # Normalize show names
        spotify["normalized_name"] = spotify["show_name"].apply(normalize_show_name)

        print(f"   ✓ Loaded {len(spotify)} Spotify shows")

        # Add to master collection
        for _, row in spotify.iterrows():
            norm_name = row["normalized_name"]
            if norm_name not in all_shows:
                all_shows[norm_name] = {"original_names": [], "platforms": {}}
            all_shows[norm_name]["original_names"].append(row["show_name"])
            all_shows[norm_name]["platforms"]["spotify"] = {
                "plays": row["plays"],
                "rank": row["rank"]
            }

    except Exception as e:
        print(f"   ✗ Error loading Spotify: {e}")
        spotify = pd.DataFrame()

    # 2. Load YouTube data
    print("\n2. Processing YouTube data...")
    try:
        youtube = pd.read_csv(data_dir / "youtube.csv")
        youtube = youtube.dropna(subset=["playlist_name"])

        # Normalize show names
        youtube["normalized_name"] = youtube["playlist_name"].apply(normalize_show_name)

        print(f"   ✓ Loaded {len(youtube)} YouTube shows")

        # Add to master collection
        for _, row in youtube.iterrows():
            norm_name = row["normalized_name"]
            if norm_name not in all_shows:
                all_shows[norm_name] = {"original_names": [], "platforms": {}}
            all_shows[norm_name]["original_names"].append(row["playlist_name"])
            all_shows[norm_name]["platforms"]["youtube"] = {
                "views": row["views"],
                "watchtime_hrs": row["watchtime_hrs"],
                "country": row["FeatureCountry"]
            }

    except Exception as e:
        print(f"   ✗ Error loading YouTube: {e}")
        youtube = pd.DataFrame()

    # 3. Load Amazon data
    print("\n3. Processing Amazon data...")
    try:
        amazon = pd.read_csv(data_dir / "amazon.csv")
        amazon = amazon.dropna(subset=["Show Title"])

        # Normalize show names
        amazon["normalized_name"] = amazon["Show Title"].apply(normalize_show_name)

        print(f"   ✓ Loaded {len(amazon)} Amazon shows")

        # Add to master collection
        for _, row in amazon.iterrows():
            norm_name = row["normalized_name"]
            if norm_name not in all_shows:
                all_shows[norm_name] = {"original_names": [], "platforms": {}}
            all_shows[norm_name]["original_names"].append(row["Show Title"])
            all_shows[norm_name]["platforms"]["amazon"] = {
                "total_plays": row["Total Plays"],
                "customers": row["Customers"],
                "category": row["Category Name"],
                "completion_rate": row["Average Completion Rate"]
            }

    except Exception as e:
        print(f"   ✗ Error loading Amazon: {e}")
        amazon = pd.DataFrame()

    # 4. Load Apple data
    print("\n4. Processing Apple data...")
    try:
        apple = pd.read_csv(data_dir / "apple.csv")
        apple = apple.dropna(subset=["Podcast"])

        # Normalize show names
        apple["normalized_name"] = apple["Podcast"].apply(normalize_show_name)

        print(f"   ✓ Loaded {len(apple)} Apple shows")

        # Add to master collection
        for _, row in apple.iterrows():
            norm_name = row["normalized_name"]
            if norm_name not in all_shows:
                all_shows[norm_name] = {"original_names": [], "platforms": {}}
            all_shows[norm_name]["original_names"].append(row["Podcast"])
            all_shows[norm_name]["platforms"]["apple"] = {
                "plays_30s": row["Plays (>30s)"],
                "rank": row["Rank"]
            }

    except Exception as e:
        print(f"   ✗ Error loading Apple: {e}")
        apple = pd.DataFrame()

    # 5. Skip iHeart for now (Excel file needs conversion)
    print("\n5. Skipping iHeart data (Excel file - needs conversion)")

    print(f"\nSUMMARY:")
    print(f"  Total unique shows identified: {len(all_shows)}")

    # Show platform distribution
    platform_counts = {}
    for show_data in all_shows.values():
        for platform in show_data["platforms"].keys():
            platform_counts[platform] = platform_counts.get(platform, 0) + 1

    print(f"  Platform distribution:")
    for platform, count in platform_counts.items():
        print(f"    {platform.capitalize()}: {count} shows")

    # Show cross-platform matches
    multi_platform = sum(1 for show_data in all_shows.values()
                        if len(show_data["platforms"]) > 1)
    print(f"  Shows on multiple platforms: {multi_platform}")

    return all_shows, spotify, youtube, amazon, apple

def analyze_show_matching(all_shows):
    """Analyze show matching across platforms."""

    print(f"\nCROSS-PLATFORM MATCHING ANALYSIS")
    print("=" * 40)

    # Group by number of platforms
    by_platform_count = {}
    for norm_name, show_data in all_shows.items():
        count = len(show_data["platforms"])
        if count not in by_platform_count:
            by_platform_count[count] = []
        by_platform_count[count].append((norm_name, show_data))

    for platform_count in sorted(by_platform_count.keys(), reverse=True):
        shows = by_platform_count[platform_count]
        print(f"\n{platform_count} platform(s): {len(shows)} shows")

        if platform_count > 1:
            # Show first few examples
            for norm_name, show_data in shows[:5]:
                platforms = list(show_data["platforms"].keys())
                original_names = show_data["original_names"]
                print(f"  • {norm_name}")
                print(f"    Platforms: {', '.join(platforms)}")
                print(f"    Original names: {original_names}")

    return by_platform_count

def extract_countries_and_genres(all_shows):
    """Extract country and genre information from available data."""

    print(f"\nEXTRACTING COUNTRY AND GENRE DATA")
    print("=" * 40)

    country_mapping = {}
    genre_mapping = {}

    for norm_name, show_data in all_shows.items():
        platforms = show_data["platforms"]

        # Extract country from YouTube if available
        if "youtube" in platforms and "country" in platforms["youtube"]:
            country = platforms["youtube"]["country"]
            if pd.notna(country) and country != "":
                country_mapping[norm_name] = {
                    "country": country,
                    "source": "YouTube FeatureCountry"
                }

        # Extract genre from Amazon if available
        if "amazon" in platforms and "category" in platforms["amazon"]:
            category = platforms["amazon"]["category"]
            if pd.notna(category) and category != "":
                genre_mapping[norm_name] = {
                    "genre": category,
                    "source": "Amazon Category"
                }

    print(f"  Country data found: {len(country_mapping)} shows")
    print(f"  Genre data found: {len(genre_mapping)} shows")

    # Show country distribution
    if country_mapping:
        country_dist = {}
        for data in country_mapping.values():
            country = data["country"]
            country_dist[country] = country_dist.get(country, 0) + 1

        print(f"\n  Country distribution:")
        for country, count in sorted(country_dist.items(), key=lambda x: -x[1]):
            print(f"    {country}: {count} shows")

    # Show genre distribution
    if genre_mapping:
        genre_dist = {}
        for data in genre_mapping.values():
            genre = data["genre"]
            genre_dist[genre] = genre_dist.get(genre, 0) + 1

        print(f"\n  Genre distribution:")
        for genre, count in sorted(genre_dist.items(), key=lambda x: -x[1]):
            print(f"    {genre}: {count} shows")

    return country_mapping, genre_mapping

def save_analysis_results(all_shows, country_mapping, genre_mapping):
    """Save analysis results to files."""

    print(f"\nSAVING ANALYSIS RESULTS")
    print("=" * 30)

    # 1. Save normalized show mapping
    show_mapping_data = []
    for norm_name, show_data in all_shows.items():
        platforms = list(show_data["platforms"].keys())
        original_names = show_data["original_names"]

        show_mapping_data.append({
            "normalized_name": norm_name,
            "platforms": ", ".join(platforms),
            "platform_count": len(platforms),
            "original_names": " | ".join(original_names)
        })

    show_mapping_df = pd.DataFrame(show_mapping_data)
    show_mapping_df = show_mapping_df.sort_values("platform_count", ascending=False)
    show_mapping_df.to_csv("updated_show_mapping.csv", index=False)
    print(f"  ✓ Saved show mapping: updated_show_mapping.csv ({len(show_mapping_df)} shows)")

    # 2. Save country mapping
    if country_mapping:
        country_df = pd.DataFrame([
            {"normalized_name": name, "country": data["country"], "source": data["source"]}
            for name, data in country_mapping.items()
        ])
        country_df.to_csv("updated_country_mapping.csv", index=False)
        print(f"  ✓ Saved country mapping: updated_country_mapping.csv ({len(country_df)} shows)")

    # 3. Save genre mapping
    if genre_mapping:
        genre_df = pd.DataFrame([
            {"normalized_name": name, "genre": data["genre"], "source": data["source"]}
            for name, data in genre_mapping.items()
        ])
        genre_df.to_csv("updated_genre_mapping.csv", index=False)
        print(f"  ✓ Saved genre mapping: updated_genre_mapping.csv ({len(genre_df)} shows)")

    return show_mapping_df

if __name__ == "__main__":
    # Load and process all data
    all_shows, spotify, youtube, amazon, apple = load_and_process_data()

    # Analyze matching
    by_platform_count = analyze_show_matching(all_shows)

    # Extract countries and genres
    country_mapping, genre_mapping = extract_countries_and_genres(all_shows)

    # Save results
    show_mapping_df = save_analysis_results(all_shows, country_mapping, genre_mapping)

    print(f"\n🎯 REBUILD COMPLETE!")
    print(f"   Next steps: Research missing countries/genres, then rebuild ranking system")