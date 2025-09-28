#!/usr/bin/env python3
"""
Create unified genre mapping from platform data + Tavily research
"""

import pandas as pd
from pathlib import Path

def normalize_show_name(name):
    """Normalize show name for matching - consistent with ranking system."""
    if pd.isna(name):
        return ""

    # Apply same normalization as ranking system
    normalized = str(name).strip().lower()
    # Remove all non-word/space characters (same as ranking system regex)
    import re
    normalized = re.sub(r"[^\w\s]", "", normalized)
    # Collapse multiple spaces to single space
    normalized = re.sub(r"\s+", " ", normalized)

    return normalized.strip()

def is_valid_genre(genre_text):
    """Check if a platform category is actually a genre (not ranking/status)."""
    if pd.isna(genre_text) or not genre_text:
        return False

    # Skip non-genre categories
    invalid_categories = ['top 25', 'honorable mention', 'kids & family', 'fiction', 'leisure']
    genre_lower = str(genre_text).lower().strip()

    return genre_lower not in invalid_categories

def extract_platform_genres():
    """Extract genres provided by each platform."""

    platform_genres = {}

    # Amazon has explicit Category Name column
    print("Extracting Amazon platform genres...")
    try:
        amazon = pd.read_csv("data/amazon.csv", skiprows=2)
        amazon = amazon.dropna(subset=["Show Title"])

        amazon_count = 0
        for _, row in amazon.iterrows():
            if pd.notna(row.get("Category Name")) and is_valid_genre(row["Category Name"]):
                normalized_name = normalize_show_name(row["Show Title"])
                platform_genres[normalized_name] = {
                    "platform_genre": row["Category Name"],
                    "source": "Amazon platform"
                }
                amazon_count += 1

        print(f"Found {amazon_count} valid Amazon genres")
    except Exception as e:
        print(f"Error loading Amazon genres: {e}")

    # Check if Spotify has genre information
    print("Checking Spotify for genre data...")
    try:
        spotify = pd.read_csv("data/spotify.csv", skiprows=7)
        spotify.columns = ["show_name", "spotify_plays", "category"]

        spotify_genres = 0
        for _, row in spotify.iterrows():
            if pd.notna(row.get("category")) and is_valid_genre(row["category"]):
                normalized_name = normalize_show_name(row["show_name"])
                if normalized_name not in platform_genres:
                    platform_genres[normalized_name] = {
                        "platform_genre": row["category"],
                        "source": "Spotify platform"
                    }
                    spotify_genres += 1

        print(f"Found {spotify_genres} valid Spotify genres")
    except Exception as e:
        print(f"Error loading Spotify genres: {e}")

    return platform_genres

def load_existing_research():
    """Load existing genre research data."""

    research_genres = {}

    # Load refined genre master (platform + internet research)
    try:
        refined_df = pd.read_csv("data_refined_genres/refined_genre_master.csv")

        for _, row in refined_df.iterrows():
            normalized_name = normalize_show_name(row["show_name"])
            research_genres[normalized_name] = {
                "original_genre": row.get("genre", ""),
                "refined_genre": row["refined_genre"],
                "source": row.get("source", "Previous research")
            }

        print(f"Loaded {len(research_genres)} shows from previous research")
    except Exception as e:
        print(f"Error loading refined genres: {e}")

    # Load Tavily research
    tavily_genres = {}
    try:
        tavily_df = pd.read_csv("tavily_normalized_genre_mapping.csv")

        for _, row in tavily_df.iterrows():
            normalized_name = row["normalized_name"]
            tavily_genres[normalized_name] = {
                "tavily_genre": row["tavily_genre"],
                "source": "Tavily research"
            }

        print(f"Loaded {len(tavily_genres)} shows from Tavily research")
    except Exception as e:
        print(f"Error loading Tavily genres: {e}")

    return research_genres, tavily_genres

def map_to_standard_genres(genre_text):
    """Map any genre text to our 8 standard categories."""

    if pd.isna(genre_text) or not genre_text:
        return "Other"

    genre_lower = str(genre_text).lower()

    # True Crime
    if any(term in genre_lower for term in ['true crime', 'crime', 'murder', 'mystery']):
        return "True Crime"

    # News & Politics
    if any(term in genre_lower for term in ['news', 'politics', 'political', 'current events']):
        return "News & Politics"

    # Comedy
    if any(term in genre_lower for term in ['comedy', 'humor', 'funny', 'comedic']):
        return "Comedy"

    # Interview & Talk
    if any(term in genre_lower for term in ['interview', 'talk', 'conversation', 'chat']):
        return "Interview & Talk"

    # Sports
    if any(term in genre_lower for term in ['sports', 'football', 'basketball', 'baseball', 'athletic']):
        return "Sports"

    # Business
    if any(term in genre_lower for term in ['business', 'finance', 'financial', 'investing', 'money', 'entrepreneurship']):
        return "Business"

    # Education
    if any(term in genre_lower for term in ['education', 'science', 'learning', 'academic', 'history', 'psychology']):
        return "Education"

    # Entertainment
    if any(term in genre_lower for term in ['entertainment', 'pop culture', 'celebrity', 'lifestyle', 'variety']):
        return "Entertainment"

    return "Other"

def create_union_mapping():
    """Create comprehensive union of all genre sources."""

    print("CREATING UNION GENRE MAPPING")
    print("=" * 50)

    # Get all sources
    platform_genres = extract_platform_genres()
    research_genres, tavily_genres = load_existing_research()

    # Create union mapping
    union_mapping = {}

    # Get all unique shows
    all_shows = set()
    all_shows.update(platform_genres.keys())
    all_shows.update(research_genres.keys())
    all_shows.update(tavily_genres.keys())

    print(f"\nTotal unique shows across all sources: {len(all_shows)}")

    # Create comprehensive mapping for each show
    for show in all_shows:
        show_data = {
            "normalized_name": show,
            "platform_genre": "",
            "research_genre": "",
            "tavily_genre": "",
            "final_genre": "",
            "sources": []
        }

        # Add platform data
        if show in platform_genres:
            show_data["platform_genre"] = platform_genres[show]["platform_genre"]
            show_data["sources"].append(platform_genres[show]["source"])

        # Add research data
        if show in research_genres:
            show_data["research_genre"] = research_genres[show]["refined_genre"]
            show_data["sources"].append(research_genres[show]["source"])

        # Add Tavily data
        if show in tavily_genres:
            show_data["tavily_genre"] = tavily_genres[show]["tavily_genre"]
            show_data["sources"].append(tavily_genres[show]["source"])

        # Determine final genre (priority: Platform > Tavily > Research)
        if show_data["platform_genre"]:
            show_data["final_genre"] = map_to_standard_genres(show_data["platform_genre"])
        elif show_data["tavily_genre"]:
            show_data["final_genre"] = show_data["tavily_genre"]
        elif show_data["research_genre"]:
            show_data["final_genre"] = show_data["research_genre"]
        else:
            show_data["final_genre"] = "Other"

        show_data["source_summary"] = " + ".join(show_data["sources"])
        union_mapping[show] = show_data

    return union_mapping

def analyze_union_results(union_mapping):
    """Analyze the results of union mapping."""

    print("\nUNION MAPPING ANALYSIS")
    print("=" * 30)

    # Count by source combinations
    source_stats = {}
    genre_stats = {}

    for show_data in union_mapping.values():
        sources = show_data["source_summary"]
        genre = show_data["final_genre"]

        source_stats[sources] = source_stats.get(sources, 0) + 1
        genre_stats[genre] = genre_stats.get(genre, 0) + 1

    print("SOURCES COVERAGE:")
    for source, count in sorted(source_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {source}: {count} shows")

    print(f"\nFINAL GENRE DISTRIBUTION:")
    for genre, count in sorted(genre_stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  {genre}: {count} shows")

    # Examples of multi-source shows
    print(f"\nSAMPLE MULTI-SOURCE MAPPINGS:")
    multi_source = [(k, v) for k, v in union_mapping.items() if len(v["sources"]) > 1]
    for show, data in multi_source[:10]:
        print(f"  {show} -> {data['final_genre']}")
        if data["platform_genre"]:
            print(f"    Platform: {data['platform_genre']}")
        if data["research_genre"]:
            print(f"    Research: {data['research_genre']}")
        if data["tavily_genre"]:
            print(f"    Tavily: {data['tavily_genre']}")
        print(f"    Sources: {data['source_summary']}")
        print()

def save_union_mapping(union_mapping):
    """Save the union mapping to CSV."""

    # Create DataFrame
    df_data = []
    for show, data in union_mapping.items():
        df_data.append({
            "normalized_name": show,
            "final_genre": data["final_genre"],
            "platform_genre": data["platform_genre"],
            "research_genre": data["research_genre"],
            "tavily_genre": data["tavily_genre"],
            "source_summary": data["source_summary"]
        })

    df = pd.DataFrame(df_data)
    df.to_csv("union_genre_mapping.csv", index=False)

    print(f"\nSaved union mapping with {len(df)} shows to union_genre_mapping.csv")

if __name__ == "__main__":
    union_mapping = create_union_mapping()
    analyze_union_results(union_mapping)
    save_union_mapping(union_mapping)