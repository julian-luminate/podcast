#!/usr/bin/env python3
"""
Comprehensive fix for Unknown countries and Other genres based on Tavily research
"""

import pandas as pd
import re
from pathlib import Path

def create_comprehensive_classification_updates():
    """Create comprehensive updates for Unknown countries and Other genres."""

    print("CREATING COMPREHENSIVE CLASSIFICATION UPDATES")
    print("=" * 55)

    # Based on Tavily research and content analysis
    country_updates = {
        # Top shows missing country classification
        "the daily": ("US", "New York Times - American news organization"),
        "crime junkie": ("US", "Ashley Flowers and Brit Prawat - Indianapolis, Indiana based"),
        "dateline nbc": ("US", "NBC - American television network"),
        "morbid": ("US", "American true crime podcast hosts"),
        "mrballen strange dark mysterious stories": ("US", "John Allen - American former Navy SEAL"),

        # Additional US shows
        "the mel robbins": ("US", "Mel Robbins - American motivational speaker"),
        "stuff you should know": ("US", "HowStuffWorks - American educational media"),
        "pod save america": ("US", "Crooked Media - American political podcast company"),
        "my favorite murder": ("US", "Karen Kilgariff and Georgia Hardstark - American comedians"),
        "smartless": ("US", "Jason Bateman, Sean Hayes, Will Arnett - American actors"),
        "the megyn kelly": ("US", "Megyn Kelly - American journalist"),
        "the ben shapiro": ("US", "Ben Shapiro - American political commentator"),
        "armchair expert": ("US", "Dax Shepard - American actor and comedian"),
        "this past weekend": ("US", "Theo Von - American comedian"),
        "the tucker carlson": ("US", "Tucker Carlson - American media personality"),
        "call her daddy": ("US", "Alex Cooper - American podcaster"),
        "huberman lab": ("US", "Andrew Huberman - Stanford neuroscientist"),
        "new heights": ("US", "Travis and Jason Kelce - American NFL players"),
        "up first from npr": ("US", "NPR - American National Public Radio"),
        "wait wait dont tell me": ("US", "NPR - American comedy news quiz"),
        "on purpose": ("US", "Jay Shetty - British-American author based in US"),
        "the breakfast club": ("US", "American hip-hop radio show"),
        "lex friedman": ("US", "Lex Fridman - American-Russian AI researcher at MIT"),

        # International shows
        "redhanded": ("GB", "British true crime podcast"),
        "la corneta": ("ES", "Spanish language comedy podcast"),
        "la corneta extendida": ("ES", "Spanish language comedy podcast extended"),
        "die nervigen": ("DE", "German comedy podcast by Julia Beautx & Joey's Jungle"),
        "dick doof": ("DE", "German comedy podcast"),
        "安住紳一郎の日曜天国": ("JP", "Japanese radio show by TBS Radio"),

        # Other shows that can be inferred
        "two hot takes": ("US", "American Reddit reaction podcast"),
        "small town murder": ("US", "American true crime comedy podcast"),
        "serial": ("US", "American investigative journalism podcast"),
        "this american life": ("US", "American public radio program"),
    }

    genre_updates = {
        # Top shows needing genre classification
        "the meidastouch": ("News & Politics", "Progressive political commentary podcast"),
        "the joe rogan experience": ("Interview & Talk", "Long-form conversations and interviews"),
        "good mythical morning": ("Comedy", "Comedy variety show"),
        "김어준의 겸손은힘들다 뉴스공장": ("News & Politics", "Korean news and political commentary"),

        # Interview and Talk shows
        "the mel robbins": ("Interview & Talk", "Self-help and motivational interviews"),
        "smartless": ("Interview & Talk", "Celebrity interviews and conversations"),
        "armchair expert": ("Interview & Talk", "Celebrity interviews and discussions"),
        "call her daddy": ("Interview & Talk", "Comedy and advice podcast"),
        "on purpose": ("Interview & Talk", "Wellness and personal development interviews"),
        "lex friedman": ("Interview & Talk", "AI, science, and technology interviews"),

        # News & Politics
        "the tucker carlson": ("News & Politics", "Political commentary"),
        "up first from npr": ("News & Politics", "Daily news briefing"),
        "breaking points": ("News & Politics", "Political commentary and analysis"),

        # Comedy
        "this past weekend": ("Comedy", "Comedy podcast with Theo Von"),
        "kill tony": ("Comedy", "Live comedy podcast"),
        "the toast": ("Comedy", "Comedy podcast by Claudia and Jackie Oshry"),
        "wait wait dont tell me": ("Comedy", "NPR comedy news quiz show"),
        "two hot takes": ("Comedy", "Reddit reaction comedy podcast"),
        "small town murder": ("Comedy", "True crime comedy podcast"),
        "smosh reads reddit stories": ("Comedy", "Reddit reaction comedy"),

        # Business & Education
        "the ramsey": ("Business", "Financial advice and money management"),
        "stuff you should know": ("Education", "Educational content about various topics"),
        "huberman lab": ("Education", "Neuroscience and health education"),
        "financial audit": ("Business", "Personal finance analysis"),

        # True Crime
        "murder mystery makeup": ("True Crime", "True crime with makeup tutorials"),

        # Entertainment
        "the breakfast club": ("Entertainment", "Hip-hop culture and celebrity interviews"),

        # Sports
        "new heights": ("Sports", "NFL and sports commentary"),

        # Society & Culture
        "this american life": ("Society & Culture", "Human interest stories and cultural commentary"),
        "serial": ("Society & Culture", "Investigative journalism and storytelling"),
    }

    print(f"✓ Country updates prepared: {len(country_updates)} shows")
    print(f"✓ Genre updates prepared: {len(genre_updates)} shows")

    return country_updates, genre_updates

def apply_classification_updates():
    """Apply comprehensive classification updates to existing mappings."""

    print("\nAPPLYING CLASSIFICATION UPDATES")
    print("=" * 40)

    # Get update data
    country_updates, genre_updates = create_comprehensive_classification_updates()

    # Load existing mappings
    try:
        country_df = pd.read_csv("comprehensive_country_mapping_updated.csv")
        print(f"Loaded existing country mapping: {len(country_df)} shows")
    except FileNotFoundError:
        country_df = pd.DataFrame(columns=["normalized_name", "country", "source"])
        print("Created new country mapping")

    try:
        genre_df = pd.read_csv("comprehensive_genre_mapping_updated.csv")
        print(f"Loaded existing genre mapping: {len(genre_df)} shows")
    except FileNotFoundError:
        genre_df = pd.DataFrame(columns=["normalized_name", "genre", "source"])
        print("Created new genre mapping")

    # Apply country updates
    country_data = []
    existing_countries = set(country_df["normalized_name"]) if not country_df.empty else set()

    # Add existing data
    for _, row in country_df.iterrows():
        country_data.append({
            "normalized_name": row["normalized_name"],
            "country": row["country"],
            "source": row["source"]
        })

    # Add new updates
    for show, (country, description) in country_updates.items():
        if show not in existing_countries:
            country_data.append({
                "normalized_name": show,
                "country": country,
                "source": f"Tavily research: {description}"
            })

    # Apply genre updates
    genre_data = []
    existing_genres = set(genre_df["normalized_name"]) if not genre_df.empty else set()

    # Add existing data
    for _, row in genre_df.iterrows():
        genre_data.append({
            "normalized_name": row["normalized_name"],
            "genre": row["genre"],
            "source": row["source"]
        })

    # Add new updates
    for show, (genre, description) in genre_updates.items():
        if show not in existing_genres:
            genre_data.append({
                "normalized_name": show,
                "genre": genre,
                "source": f"Tavily research: {description}"
            })

    # Create updated DataFrames
    updated_country = pd.DataFrame(country_data).drop_duplicates(subset=["normalized_name"], keep="first")
    updated_genre = pd.DataFrame(genre_data).drop_duplicates(subset=["normalized_name"], keep="first")

    # Save updated mappings
    updated_country.to_csv("final_country_mapping.csv", index=False)
    updated_genre.to_csv("final_genre_mapping.csv", index=False)

    print(f"✓ Updated country mapping: {len(updated_country)} shows")
    print(f"✓ Updated genre mapping: {len(updated_genre)} shows")

    # Show distributions
    country_dist = updated_country["country"].value_counts()
    genre_dist = updated_genre["genre"].value_counts()

    print(f"\nFinal country distribution:")
    for country, count in country_dist.head(8).items():
        print(f"  {country}: {count} shows")

    print(f"\nFinal genre distribution:")
    for genre, count in genre_dist.head(8).items():
        print(f"  {genre}: {count} shows")

    return updated_country, updated_genre

def regenerate_final_rankings():
    """Regenerate final rankings with complete classifications."""

    print(f"\nREGENERATING FINAL RANKINGS WITH COMPLETE DATA")
    print("=" * 55)

    # Load the ranking system and run with updated mappings
    import subprocess
    result = subprocess.run(["python", "updated_podcast_ranking_system.py"],
                          capture_output=True, text=True)

    if result.returncode == 0:
        print("✓ Successfully regenerated rankings")

        # Load and analyze the final results
        try:
            final_rankings = pd.read_csv("updated_podcast_cross_platform_rankings.csv")

            # Check for remaining unknowns
            unknown_countries = len(final_rankings[final_rankings["country"] == "Unknown"])
            other_genres = len(final_rankings[final_rankings["genre"] == "Other"])

            print(f"\nFinal classification status:")
            print(f"  Total shows ranked: {len(final_rankings)}")
            print(f"  Shows with Unknown country: {unknown_countries}")
            print(f"  Shows with Other genre: {other_genres}")
            print(f"  Classification completeness: {((len(final_rankings) - unknown_countries - other_genres) / len(final_rankings) * 100):.1f}%")

            # Show top 10
            print(f"\nTop 10 Final Rankings:")
            print("-" * 50)
            top_10 = final_rankings.head(10)
            for _, row in top_10.iterrows():
                print(f"{row['rank']:2d}. {row['show_name'].title()}")
                print(f"    Score: {row['composite_score']:.1f} | {row['genre']} | {row['country']}")
                print(f"    Platforms: {row['platforms_present']} | Consumption: {row['total_consumption']:,.0f}")

            return final_rankings

        except FileNotFoundError:
            print("✗ Could not load final rankings file")
            return None
    else:
        print(f"✗ Error regenerating rankings: {result.stderr}")
        return None

if __name__ == "__main__":
    # Apply classification updates
    updated_country, updated_genre = apply_classification_updates()

    # Regenerate final rankings
    final_rankings = regenerate_final_rankings()

    print(f"\n🎯 COMPREHENSIVE CLASSIFICATION FIX COMPLETE!")
    if final_rankings is not None:
        print(f"   Final CSV: updated_podcast_cross_platform_rankings.csv ({len(final_rankings)} shows)")
        print(f"   Ready for analysis with greatly improved country and genre coverage!")