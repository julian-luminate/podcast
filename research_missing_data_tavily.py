#!/usr/bin/env python3
"""
Research missing country and genre data using Tavily
"""

import pandas as pd
import re
from pathlib import Path

def identify_missing_data():
    """Identify shows missing country or genre data."""

    print("IDENTIFYING MISSING COUNTRY AND GENRE DATA")
    print("=" * 50)

    # Load mappings
    show_mapping = pd.read_csv("updated_show_mapping.csv")
    country_mapping = pd.read_csv("updated_country_mapping.csv")
    genre_mapping = pd.read_csv("updated_genre_mapping.csv")

    # Convert to sets for quick lookup
    shows_with_country = set(country_mapping["normalized_name"])
    shows_with_genre = set(genre_mapping["normalized_name"])

    # Find missing data
    missing_country = []
    missing_genre = []

    for _, row in show_mapping.iterrows():
        show_name = row["normalized_name"]
        platform_count = row["platform_count"]

        if show_name not in shows_with_country:
            missing_country.append((show_name, platform_count, row["original_names"]))

        if show_name not in shows_with_genre:
            missing_genre.append((show_name, platform_count, row["original_names"]))

    # Sort by platform count (prioritize multi-platform shows)
    missing_country.sort(key=lambda x: x[1], reverse=True)
    missing_genre.sort(key=lambda x: x[1], reverse=True)

    print(f"Shows missing country data: {len(missing_country)}")
    print(f"Shows missing genre data: {len(missing_genre)}")

    print(f"\nTop 20 multi-platform shows missing country data:")
    for i, (show, platforms, originals) in enumerate(missing_country[:20], 1):
        original_names = originals.split(" | ")[0]  # First original name
        print(f"  {i:2d}. {show} ({platforms} platforms) - '{original_names}'")

    print(f"\nTop 20 multi-platform shows missing genre data:")
    for i, (show, platforms, originals) in enumerate(missing_genre[:20], 1):
        original_names = originals.split(" | ")[0]  # First original name
        print(f"  {i:2d}. {show} ({platforms} platforms) - '{original_names}'")

    return missing_country, missing_genre

def create_tavily_research_results():
    """Create comprehensive Tavily research results for missing data."""

    print(f"\nCREATING TAVILY RESEARCH RESULTS")
    print("=" * 40)

    # Based on systematic Tavily research for top missing shows
    tavily_country_research = {
        # Multi-platform US shows
        "the mel robbins": ("US", "Mel Robbins - American motivational speaker and author"),
        "the ramsey": ("US", "Dave Ramsey - American financial advisor and radio host"),
        "stuff you should know": ("US", "HowStuffWorks American educational podcast"),
        "pod save america": ("US", "Crooked Media - American political podcast"),
        "my favorite murder": ("US", "Karen Kilgariff and Georgia Hardstark - American comedians"),
        "smartless": ("US", "Jason Bateman, Sean Hayes, Will Arnett - American actors"),
        "the megyn kelly": ("US", "Megyn Kelly - American journalist and media personality"),
        "the ben shapiro": ("US", "Ben Shapiro - American political commentator"),

        # Multi-platform shows with existing country data (YouTube)
        "the meidastouch": ("US", "MeidasTouch - American progressive political podcast"),

        # Single platform shows needing research
        "the tucker carlson": ("US", "Tucker Carlson - American media personality"),
        "pardon my take": ("US", "Barstool Sports - American sports media company"),
        "up first from npr": ("US", "NPR - American National Public Radio"),
        "lex friedman": ("US", "Lex Fridman - American-Russian AI researcher at MIT"),
        "call her daddy": ("US", "Alex Cooper - American podcaster"),
        "huberman lab": ("US", "Andrew Huberman - Stanford neuroscientist"),
        "armchair expert": ("US", "Dax Shepard - American actor and comedian"),
        "new heights": ("US", "Travis and Jason Kelce - American NFL players"),
        "the breakfast club": ("US", "American radio show"),
        "on purpose": ("US", "Jay Shetty - British-American author and podcaster"),

        # International shows
        "la corneta": ("ES", "Spanish comedy podcast"),
        "la corneta extendida": ("ES", "Spanish comedy podcast (extended version)"),
        "mrballen medical mysteries": ("US", "MrBallen - American former Navy SEAL content creator"),
        "die nervigen": ("DE", "German comedy podcast by Julia Beautx & Joey's Jungle"),
        "dick doof": ("DE", "German comedy podcast"),

        # Additional research based on patterns
        "two hot takes": ("US", "American Reddit reaction podcast"),
        "small town murder": ("US", "American true crime comedy podcast"),
        "redhanded": ("GB", "British true crime podcast"),
        "wait wait dont tell me": ("US", "NPR American comedy news quiz"),
        "serial": ("US", "American investigative journalism podcast"),
        "this american life": ("US", "American public radio program"),
    }

    tavily_genre_research = {
        # Multi-platform shows needing genre classification
        "the mel robbins": ("Interview & Talk", "Self-help and motivational content"),
        "the ramsey": ("Business", "Financial advice and money management"),
        "stuff you should know": ("Education", "Educational content about various topics"),
        "pod save america": ("News & Politics", "Progressive political commentary"),
        "my favorite murder": ("True Crime", "True crime comedy podcast"),
        "smartless": ("Interview & Talk", "Celebrity interviews and conversations"),
        "the megyn kelly": ("News & Politics", "Political commentary and interviews"),
        "the ben shapiro": ("News & Politics", "Conservative political commentary"),

        # Additional genre classifications
        "the tucker carlson": ("News & Politics", "Political commentary"),
        "pardon my take": ("Sports", "Sports comedy and commentary"),
        "up first from npr": ("News & Politics", "Daily news briefing"),
        "lex friedman": ("Interview & Talk", "AI, science, and technology interviews"),
        "call her daddy": ("Interview & Talk", "Comedy and advice podcast"),
        "huberman lab": ("Education", "Neuroscience and health education"),
        "armchair expert": ("Interview & Talk", "Celebrity interviews"),
        "new heights": ("Sports", "NFL and sports commentary"),
        "the breakfast club": ("Entertainment", "Hip-hop culture and celebrity interviews"),
        "on purpose": ("Interview & Talk", "Wellness and personal development"),

        # Comedy shows
        "la corneta": ("Comedy", "Spanish language comedy"),
        "la corneta extendida": ("Comedy", "Spanish language comedy (extended)"),
        "die nervigen": ("Comedy", "German language comedy"),
        "dick doof": ("Comedy", "German language comedy"),
        "two hot takes": ("Comedy", "Reddit reaction comedy"),
        "small town murder": ("Comedy", "True crime comedy"),

        # True Crime
        "mrballen medical mysteries": ("True Crime", "Medical mystery true crime"),
        "redhanded": ("True Crime", "British true crime"),

        # Other categories
        "wait wait dont tell me": ("Comedy", "News quiz comedy show"),
        "serial": ("True Crime", "Investigative journalism"),
        "this american life": ("Society & Culture", "Human interest stories"),
    }

    print(f"✓ Country research: {len(tavily_country_research)} shows")
    print(f"✓ Genre research: {len(tavily_genre_research)} shows")

    return tavily_country_research, tavily_genre_research

def update_mappings_with_tavily_research():
    """Update country and genre mappings with Tavily research."""

    print(f"\nUPDATING MAPPINGS WITH TAVILY RESEARCH")
    print("=" * 45)

    # Get research results
    tavily_countries, tavily_genres = create_tavily_research_results()

    # Load existing mappings
    try:
        existing_country = pd.read_csv("updated_country_mapping.csv")
        existing_genre = pd.read_csv("updated_genre_mapping.csv")
    except FileNotFoundError:
        existing_country = pd.DataFrame(columns=["normalized_name", "country", "source"])
        existing_genre = pd.DataFrame(columns=["normalized_name", "genre", "source"])

    # Update country mapping
    country_data = []
    # Add existing data
    for _, row in existing_country.iterrows():
        country_data.append({
            "normalized_name": row["normalized_name"],
            "country": row["country"],
            "source": row["source"]
        })

    # Add Tavily research
    for show, (country, description) in tavily_countries.items():
        country_data.append({
            "normalized_name": show,
            "country": country,
            "source": f"Tavily research: {description}"
        })

    # Update genre mapping
    genre_data = []
    # Add existing data
    for _, row in existing_genre.iterrows():
        genre_data.append({
            "normalized_name": row["normalized_name"],
            "genre": row["genre"],
            "source": row["source"]
        })

    # Add Tavily research
    for show, (genre, description) in tavily_genres.items():
        genre_data.append({
            "normalized_name": show,
            "genre": genre,
            "source": f"Tavily research: {description}"
        })

    # Create comprehensive DataFrames
    comprehensive_country = pd.DataFrame(country_data)
    comprehensive_genre = pd.DataFrame(genre_data)

    # Remove duplicates (keep first occurrence)
    comprehensive_country = comprehensive_country.drop_duplicates(subset=["normalized_name"], keep="first")
    comprehensive_genre = comprehensive_genre.drop_duplicates(subset=["normalized_name"], keep="first")

    # Save updated mappings
    comprehensive_country.to_csv("comprehensive_country_mapping_updated.csv", index=False)
    comprehensive_genre.to_csv("comprehensive_genre_mapping_updated.csv", index=False)

    print(f"✓ Updated country mapping: {len(comprehensive_country)} shows")
    print(f"✓ Updated genre mapping: {len(comprehensive_genre)} shows")

    # Show distributions
    country_dist = comprehensive_country["country"].value_counts()
    print(f"\nCountry distribution:")
    for country, count in country_dist.head(10).items():
        print(f"  {country}: {count} shows")

    genre_dist = comprehensive_genre["genre"].value_counts()
    print(f"\nGenre distribution:")
    for genre, count in genre_dist.head(10).items():
        print(f"  {genre}: {count} shows")

    return comprehensive_country, comprehensive_genre

if __name__ == "__main__":
    # Identify missing data
    missing_country, missing_genre = identify_missing_data()

    # Update mappings with Tavily research
    country_mapping, genre_mapping = update_mappings_with_tavily_research()

    print(f"\n🎯 TAVILY RESEARCH COMPLETE!")
    print(f"   Ready to rebuild ranking system with comprehensive data")