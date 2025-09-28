#!/usr/bin/env python3
"""
Create comprehensive country mapping from explicit data + Wikipedia research
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

def create_comprehensive_country_mapping():
    """Create comprehensive country mapping from explicit data + Wikipedia research."""

    print("CREATING COMPREHENSIVE COUNTRY MAPPING")
    print("=" * 50)

    # Start with explicit mapping from YouTube data
    explicit_mapping = {}
    try:
        explicit_df = pd.read_csv("explicit_country_mapping.csv")
        explicit_mapping = dict(zip(explicit_df['normalized_name'],
                                  zip(explicit_df['country'], explicit_df['source'])))
        print(f"✓ Loaded explicit YouTube country mapping: {len(explicit_mapping)} shows")
    except FileNotFoundError:
        print("⚠ No explicit country mapping found")

    # Wikipedia research results based on our searches
    wikipedia_research = {
        # Research conducted via Wikipedia
        "2 bears 1 cave with tom segura bert kreischer": ("US", "Wikipedia - American comedians Tom Segura and Bert Kreischer"),
        "allin with chamath jason sacks friedberg": ("US", "Wikipedia - American business podcast by venture capitalists"),
        "armchair expert with dax shepard": ("US", "Wikipedia - American actors Dax Shepard and Monica Padman"),
        "call her daddy": ("US", "Wikipedia - American podcast by Alex Cooper, formerly Barstool Sports"),
        "crime junkie": ("US", "Wikipedia - Indianapolis, Indiana based true crime podcast"),
        "dateline nbc": ("US", "Wikipedia - American television news magazine show by NBC"),
        "distractible": ("US", "Wikipedia - American podcast by Markiplier and co-hosts"),
        "huberman lab": ("US", "Wikipedia - Stanford University neuroscientist Andrew Huberman"),

        # Additional US shows based on platform and context knowledge
        "2020": ("US", "ABC News program - US broadcaster"),
        "bad friends": ("US", "US comedy podcast"),
        "candace": ("US", "Candace Owens - US political commentator"),
        "dick doof": ("US", "US comedy podcast"),
        "good hang with amy poehler": ("US", "Amy Poehler - US comedian/actress"),
        "hidden brain": ("US", "NPR show - US public radio"),
        "crook county": ("US", "US true crime podcast"),

        # German language podcasts
        "die drei rabauken": ("DE", "German language podcast"),
        "die nervigen": ("DE", "German language podcast"),
        "hobbylos": ("DE", "German language podcast"),
        "kottbruder germanletsplay paluten": ("DE", "German language gaming podcast"),

        # Additional international shows can be added here as research continues
    }

    # Combine explicit mapping and Wikipedia research
    comprehensive_mapping = {}

    # Add explicit mappings
    for show, (country, source) in explicit_mapping.items():
        comprehensive_mapping[show] = {
            "country": country,
            "source": source,
            "confidence": "explicit"
        }

    # Add Wikipedia research
    for show, (country, source) in wikipedia_research.items():
        comprehensive_mapping[show] = {
            "country": country,
            "source": source,
            "confidence": "wikipedia_research"
        }

    print(f"✓ Added Wikipedia research: {len(wikipedia_research)} shows")
    print(f"✓ Total comprehensive mapping: {len(comprehensive_mapping)} shows")

    return comprehensive_mapping

def get_all_unique_shows():
    """Get all unique shows from all platforms."""
    all_shows = set()
    data_dir = Path("data")

    # Spotify
    try:
        spotify = pd.read_csv(data_dir / "spotify.csv", skiprows=7)
        spotify.columns = ["show_name", "spotify_plays", "category"]
        spotify = spotify.dropna()
        spotify_shows = [normalize_show_name(show) for show in spotify["show_name"]]
        all_shows.update(spotify_shows)
        print(f"  Spotify: {len(spotify_shows)} shows")
    except Exception as e:
        print(f"  Error loading Spotify: {e}")

    # YouTube
    try:
        youtube = pd.read_csv(data_dir / "youtube.csv")
        youtube = youtube.dropna(subset=["playlist_name"])
        youtube_shows = [normalize_show_name(show) for show in youtube["playlist_name"]]
        all_shows.update(youtube_shows)
        print(f"  YouTube: {len(youtube_shows)} shows")
    except Exception as e:
        print(f"  Error loading YouTube: {e}")

    # Amazon
    try:
        amazon = pd.read_csv(data_dir / "amazon.csv", skiprows=2)
        amazon = amazon.dropna(subset=["Show Title"])
        amazon_shows = [normalize_show_name(show) for show in amazon["Show Title"]]
        all_shows.update(amazon_shows)
        print(f"  Amazon: {len(amazon_shows)} shows")
    except Exception as e:
        print(f"  Error loading Amazon: {e}")

    # iHeart
    try:
        iheart = pd.read_csv(data_dir / "iheart_platform_nominations.csv", skiprows=2)
        iheart.columns = ["rank", "show_name", "iheart_listeners", "iheart_streams", "iheart_completion", "iheart_followers"]
        iheart = iheart.dropna(subset=["show_name"])
        iheart_shows = [normalize_show_name(show) for show in iheart["show_name"]]
        all_shows.update(iheart_shows)
        print(f"  iHeart: {len(iheart_shows)} shows")
    except Exception as e:
        print(f"  Error loading iHeart: {e}")

    print(f"  Total unique shows: {len(all_shows)}")
    return all_shows

def save_comprehensive_mapping():
    """Save comprehensive country mapping and analyze coverage."""

    comprehensive_mapping = create_comprehensive_country_mapping()
    all_shows = get_all_unique_shows()

    # Create DataFrame
    mapping_data = []
    for show, data in comprehensive_mapping.items():
        mapping_data.append({
            "normalized_name": show,
            "country": data["country"],
            "source": data["source"],
            "confidence": data["confidence"]
        })

    df = pd.DataFrame(mapping_data)
    df = df.sort_values("normalized_name")

    # Save comprehensive mapping
    df.to_csv("comprehensive_country_mapping.csv", index=False)
    print(f"\n✓ Saved comprehensive country mapping: {len(df)} shows")

    # Analyze coverage
    mapped_shows = set(df["normalized_name"])
    unmapped_shows = all_shows - mapped_shows

    print(f"\nCOUNTRY MAPPING COVERAGE:")
    print(f"  Total shows across all platforms: {len(all_shows)}")
    print(f"  Shows with country mapping: {len(mapped_shows)}")
    print(f"  Shows still missing country: {len(unmapped_shows)}")
    print(f"  Coverage: {len(mapped_shows)/len(all_shows)*100:.1f}%")

    # Show country distribution
    country_counts = df["country"].value_counts()
    print(f"\nCOUNTRY DISTRIBUTION:")
    for country, count in country_counts.items():
        print(f"  {country}: {count} shows")

    # Show unmapped shows (first 10)
    if unmapped_shows:
        print(f"\nREMAINING UNMAPPED SHOWS (first 10):")
        for i, show in enumerate(sorted(unmapped_shows)[:10], 1):
            print(f"  {i:2d}. {show}")
        if len(unmapped_shows) > 10:
            print(f"      ... and {len(unmapped_shows) - 10} more")

    return df

if __name__ == "__main__":
    mapping_df = save_comprehensive_mapping()