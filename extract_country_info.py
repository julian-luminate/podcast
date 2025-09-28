#!/usr/bin/env python3
"""
Extract country information from all platforms and create unified country mapping
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

def extract_country_data():
    """Extract country information from all platforms."""

    print("EXTRACTING COUNTRY INFORMATION FROM ALL PLATFORMS")
    print("=" * 60)

    country_mapping = {}
    data_dir = Path("data")

    # 1. YouTube - Has explicit country data
    print("1. YouTube Platform:")
    try:
        youtube = pd.read_csv(data_dir / "youtube.csv")
        youtube_country_data = {}

        for _, row in youtube.iterrows():
            if pd.notna(row.get("playlist_name")) and pd.notna(row.get("FeatureCountry")):
                normalized_name = normalize_show_name(row["playlist_name"])
                country = row["FeatureCountry"]
                youtube_country_data[normalized_name] = country

        print(f"   Found country data for {len(youtube_country_data)} YouTube shows")

        # Sample countries
        countries = set(youtube_country_data.values())
        print(f"   Countries found: {sorted(countries)}")

        # Add to master mapping
        for show, country in youtube_country_data.items():
            country_mapping[show] = {
                "country": country,
                "source": "YouTube"
            }

    except Exception as e:
        print(f"   Error loading YouTube: {e}")

    # 2. Spotify - Assume US (mentioned in project docs)
    print("\n2. Spotify Platform:")
    try:
        spotify = pd.read_csv(data_dir / "spotify.csv", skiprows=7)
        spotify.columns = ["show_name", "spotify_plays", "category"]
        spotify = spotify.dropna()

        spotify_shows = []
        for _, row in spotify.iterrows():
            normalized_name = normalize_show_name(row["show_name"])
            spotify_shows.append(normalized_name)

            # Only add if not already in mapping (YouTube takes priority)
            if normalized_name not in country_mapping:
                country_mapping[normalized_name] = {
                    "country": "US",
                    "source": "Spotify (US-focused platform)"
                }

        print(f"   Found {len(spotify_shows)} Spotify shows (assumed US)")

    except Exception as e:
        print(f"   Error loading Spotify: {e}")

    # 3. Amazon - Check for any country indicators
    print("\n3. Amazon Platform:")
    try:
        amazon = pd.read_csv(data_dir / "amazon.csv", skiprows=2)
        amazon = amazon.dropna(subset=["Show Title"])

        amazon_shows = []
        for _, row in amazon.iterrows():
            normalized_name = normalize_show_name(row["Show Title"])
            amazon_shows.append(normalized_name)

            # Infer country from language/content
            show_title = str(row["Show Title"]).lower()
            country = "Unknown"

            # German content
            if any(word in show_title for word in ["die ", "der ", "das ", "und ", "mit "]):
                country = "Germany"
            # Spanish content
            elif any(word in show_title for word in ["la ", "el ", "con ", "de ", "caso"]):
                country = "Spain/Latin America"
            # Japanese content
            elif any(char in show_title for char in "の日曜天国"):
                country = "Japan"
            # Default to US for English content
            else:
                country = "US"

            # Only add if not already in mapping
            if normalized_name not in country_mapping:
                country_mapping[normalized_name] = {
                    "country": country,
                    "source": f"Amazon (inferred from content)"
                }

        print(f"   Found {len(amazon_shows)} Amazon shows (inferred countries)")

    except Exception as e:
        print(f"   Error loading Amazon: {e}")

    # 4. iHeart - Assume US (US-focused platform)
    print("\n4. iHeart Platform:")
    try:
        iheart = pd.read_csv(data_dir / "iheart_platform_nominations.csv", skiprows=2)
        iheart.columns = ["rank", "show_name", "iheart_listeners", "iheart_streams", "iheart_completion", "iheart_followers"]
        iheart = iheart.dropna(subset=["show_name"])

        iheart_shows = []
        for _, row in iheart.iterrows():
            normalized_name = normalize_show_name(row["show_name"])
            iheart_shows.append(normalized_name)

            # Only add if not already in mapping
            if normalized_name not in country_mapping:
                country_mapping[normalized_name] = {
                    "country": "US",
                    "source": "iHeart (US platform)"
                }

        print(f"   Found {len(iheart_shows)} iHeart shows (assumed US)")

    except Exception as e:
        print(f"   Error loading iHeart: {e}")

    print(f"\nTOTAL COUNTRY MAPPINGS: {len(country_mapping)}")

    # Count by country
    country_counts = {}
    for show_data in country_mapping.values():
        country = show_data["country"]
        country_counts[country] = country_counts.get(country, 0) + 1

    print("\nCOUNTRY DISTRIBUTION:")
    for country, count in sorted(country_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"   {country}: {count} shows")

    return country_mapping

def save_country_mapping(country_mapping):
    """Save country mapping to CSV."""

    # Convert to DataFrame format
    df_data = []
    for show, data in country_mapping.items():
        df_data.append({
            "normalized_name": show,
            "country": data["country"],
            "source": data["source"]
        })

    df = pd.DataFrame(df_data)
    df = df.sort_values("normalized_name")
    df.to_csv("country_mapping.csv", index=False)

    print(f"\n✓ Saved country mapping to country_mapping.csv ({len(df)} shows)")

    # Show sample
    print("\nSAMPLE MAPPINGS:")
    for _, row in df.head(10).iterrows():
        print(f"   {row['normalized_name']} -> {row['country']} ({row['source']})")

if __name__ == "__main__":
    mapping = extract_country_data()
    save_country_mapping(mapping)