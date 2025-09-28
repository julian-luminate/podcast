#!/usr/bin/env python3
"""
Extract country information only from explicit data sources, no inference
"""

import pandas as pd
import re
from pathlib import Path

def normalize_show_name(name):
    """Normalize show name for matching - consistent with ranking system."""
    if pd.isna(name):
        return ""

    # Apply same normalization as ranking system
    normalized = str(name).strip().lower()
    # Remove all non-word/space characters
    normalized = re.sub(r"[^\w\s]", "", normalized)
    # Collapse multiple spaces to single space
    normalized = re.sub(r"\s+", " ", normalized)

    return normalized.strip()

def extract_explicit_country_data():
    """Extract country information only from explicit data sources."""

    print("EXTRACTING COUNTRY INFORMATION FROM EXPLICIT DATA ONLY")
    print("=" * 65)

    country_mapping = {}
    data_dir = Path("data")

    # 1. YouTube - Has explicit FeatureCountry column
    print("1. YouTube Platform (explicit country data):")
    try:
        youtube = pd.read_csv(data_dir / "youtube.csv")
        youtube_country_data = {}

        for _, row in youtube.iterrows():
            if pd.notna(row.get("playlist_name")) and pd.notna(row.get("FeatureCountry")):
                normalized_name = normalize_show_name(row["playlist_name"])
                country = row["FeatureCountry"]
                youtube_country_data[normalized_name] = country

        print(f"   Found explicit country data for {len(youtube_country_data)} YouTube shows")

        # Sample countries
        countries = set(youtube_country_data.values())
        print(f"   Countries found: {sorted(countries)}")

        # Add to master mapping
        for show, country in youtube_country_data.items():
            country_mapping[show] = {
                "country": country,
                "source": "YouTube explicit"
            }

    except Exception as e:
        print(f"   Error loading YouTube: {e}")

    # 2. Check other platforms for any explicit country columns
    print("\n2. Spotify Platform:")
    try:
        spotify = pd.read_csv(data_dir / "spotify.csv", skiprows=7)

        # Check if there are any country-related columns
        print(f"   Spotify columns: {list(spotify.columns)}")
        print("   No explicit country column found in Spotify data")

    except Exception as e:
        print(f"   Error loading Spotify: {e}")

    print("\n3. Amazon Platform:")
    try:
        amazon = pd.read_csv(data_dir / "amazon.csv", skiprows=2)

        # Check if there are any country-related columns
        print(f"   Amazon columns: {list(amazon.columns)}")
        print("   No explicit country column found in Amazon data")

    except Exception as e:
        print(f"   Error loading Amazon: {e}")

    print("\n4. iHeart Platform:")
    try:
        iheart = pd.read_csv(data_dir / "iheart_platform_nominations.csv", skiprows=2)

        # Check column names
        print(f"   iHeart columns: {list(iheart.columns)}")
        print("   No explicit country column found in iHeart data")

    except Exception as e:
        print(f"   Error loading iHeart: {e}")

    print(f"\nTOTAL EXPLICIT COUNTRY MAPPINGS: {len(country_mapping)}")

    return country_mapping

def identify_shows_without_country():
    """Identify all shows that don't have explicit country data."""

    # Get explicit country mappings
    explicit_countries = extract_explicit_country_data()

    # Get all shows from all platforms
    all_shows = set()
    data_dir = Path("data")

    # Collect all show names
    print("\nCOLLECTING ALL SHOW NAMES:")

    # Spotify
    try:
        spotify = pd.read_csv(data_dir / "spotify.csv", skiprows=7)
        spotify.columns = ["show_name", "spotify_plays", "category"]
        spotify = spotify.dropna()

        spotify_shows = [normalize_show_name(show) for show in spotify["show_name"]]
        all_shows.update(spotify_shows)
        print(f"   Spotify: {len(spotify_shows)} shows")
    except Exception as e:
        print(f"   Error loading Spotify: {e}")

    # Amazon
    try:
        amazon = pd.read_csv(data_dir / "amazon.csv", skiprows=2)
        amazon = amazon.dropna(subset=["Show Title"])

        amazon_shows = [normalize_show_name(show) for show in amazon["Show Title"]]
        all_shows.update(amazon_shows)
        print(f"   Amazon: {len(amazon_shows)} shows")
    except Exception as e:
        print(f"   Error loading Amazon: {e}")

    # iHeart
    try:
        iheart = pd.read_csv(data_dir / "iheart_platform_nominations.csv", skiprows=2)
        iheart.columns = ["rank", "show_name", "iheart_listeners", "iheart_streams", "iheart_completion", "iheart_followers"]
        iheart = iheart.dropna(subset=["show_name"])

        iheart_shows = [normalize_show_name(show) for show in iheart["show_name"]]
        all_shows.update(iheart_shows)
        print(f"   iHeart: {len(iheart_shows)} shows")
    except Exception as e:
        print(f"   Error loading iHeart: {e}")

    print(f"\nTotal unique shows: {len(all_shows)}")

    # Find shows without explicit country data
    missing_country = []
    for show in all_shows:
        if show not in explicit_countries:
            missing_country.append(show)

    print(f"\nSHOWS MISSING COUNTRY INFORMATION:")
    print(f"Total shows without explicit country: {len(missing_country)}")

    if missing_country:
        print("\nShows needing Wikipedia research:")
        for i, show in enumerate(sorted(missing_country)[:20]):  # Show first 20
            print(f"   {i+1:2d}. {show}")

        if len(missing_country) > 20:
            print(f"   ... and {len(missing_country) - 20} more")

    return missing_country, explicit_countries

if __name__ == "__main__":
    missing, explicit = identify_shows_without_country()

    # Save current explicit mapping
    if explicit:
        df_data = []
        for show, data in explicit.items():
            df_data.append({
                "normalized_name": show,
                "country": data["country"],
                "source": data["source"]
            })

        df = pd.DataFrame(df_data)
        df = df.sort_values("normalized_name")
        df.to_csv("explicit_country_mapping.csv", index=False)

        print(f"\n✓ Saved explicit country mapping to explicit_country_mapping.csv ({len(df)} shows)")

    print(f"\n📝 {len(missing)} shows need Wikipedia research for country information")