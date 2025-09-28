#!/usr/bin/env python3
"""
Add missing Spotify shows to the union genre mapping
"""

import pandas as pd

def add_missing_shows():
    """Add the 4 missing Spotify shows to union genre mapping."""

    # Load existing union mapping
    union_df = pd.read_csv("union_genre_mapping.csv")

    # Define missing shows with their genres based on Tavily research
    missing_shows = [
        {
            "normalized_name": "allin with chamath jason sacks friedberg",
            "final_genre": "Business",
            "platform_genre": "",
            "research_genre": "",
            "tavily_genre": "Business",
            "source_summary": "Tavily research"
        },
        {
            "normalized_name": "candace",
            "final_genre": "News & Politics",
            "platform_genre": "",
            "research_genre": "",
            "tavily_genre": "News & Politics",
            "source_summary": "Tavily research"
        },
        {
            "normalized_name": "matt and shanes secret podcast",
            "final_genre": "Comedy",
            "platform_genre": "",
            "research_genre": "",
            "tavily_genre": "Comedy",
            "source_summary": "Tavily research"
        },
        {
            "normalized_name": "the megyn kelly show",
            "final_genre": "News & Politics",
            "platform_genre": "",
            "research_genre": "",
            "tavily_genre": "News & Politics",
            "source_summary": "Tavily research"
        }
    ]

    # Add missing shows to dataframe
    missing_df = pd.DataFrame(missing_shows)
    updated_df = pd.concat([union_df, missing_df], ignore_index=True)

    # Sort by normalized name for consistency
    updated_df = updated_df.sort_values("normalized_name")

    # Save updated mapping
    updated_df.to_csv("union_genre_mapping.csv", index=False)

    print("ADDED MISSING SPOTIFY SHOWS TO GENRE MAPPING")
    print("=" * 50)
    print(f"Previous total: {len(union_df)} shows")
    print(f"Added: {len(missing_shows)} shows")
    print(f"New total: {len(updated_df)} shows")

    print(f"\nAdded shows:")
    for show in missing_shows:
        print(f"  - {show['normalized_name']} -> {show['final_genre']}")

    return updated_df

if __name__ == "__main__":
    add_missing_shows()