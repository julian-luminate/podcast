#!/usr/bin/env python3
"""
Update country classifications for shows currently marked as 'Unknown' based on Tavily research
"""

import pandas as pd

def create_unknown_country_updates():
    """Create comprehensive country updates for shows marked as 'Unknown' based on Tavily research."""

    print("CREATING COMPREHENSIVE 'UNKNOWN' COUNTRY UPDATES")
    print("=" * 60)

    # Based on Tavily research for shows with 'Unknown' country
    unknown_country_updates = {
        # US-based shows - News & Media
        "2020": ("US", "ABC News - American television newsmagazine program"),
        "npr news now": ("US", "NPR - National Public Radio, American public broadcasting"),
        "the bill simmons": ("US", "The Ringer - American sports media company founded by Bill Simmons"),
        "the toast": ("US", "Jackie & Claudia Oshry - American podcast by Dear Media"),
        "distractible": ("US", "Markiplier (Mark Fischbach), Wade Barnes, Bob Muyskens - American YouTubers"),
        "the deck": ("US", "Ashley Flowers/audiochuck - American true crime podcast company"),
        "the joe budden": ("US", "Joe Budden - American rapper and media personality based in New York"),
        "the bobby bones": ("US", "Bobby Bones Show - Nashville-based iHeart Radio country music program"),
        "last on the left": ("US", "Last Podcast on the Left - American comedy horror podcast"),
        "snapped women who murder": ("US", "Oxygen Network - American true crime television series"),
        "serial killers": ("US", "Parcast/Spotify - American true crime podcast network"),
        "behind the bastards": ("US", "Robert Evans - American journalist and podcaster"),
        "joel osteen": ("US", "Joel Osteen - American televangelist based in Houston, Texas"),
        "matt and shanes secret": ("US", "Matt McCusker and Shane Gillis - American comedians"),
        "murder in america": ("US", "American true crime podcast series"),
        "sword and scale": ("US", "Mike Boudet - American true crime podcast"),
        "the dan le batard": ("US", "Dan Le Batard - American sports media personality, ESPN/Meadowlark Media"),
        "the ezra klein": ("US", "Ezra Klein - American journalist, New York Times columnist"),

        # UK-based shows
        "the rest is history": ("GB", "Tom Holland and Dominic Sandbrook - British historians"),

        # Shows that need more specific research (keeping as Unknown for now but adding source notes)
        "": ("Unknown", "Empty show name - needs data cleaning"),
    }

    print(f"✓ Country updates prepared for {len(unknown_country_updates)} shows")

    return unknown_country_updates

def apply_unknown_country_updates():
    """Apply country updates to existing mappings for 'Unknown' shows."""

    print("\nAPPLYING 'UNKNOWN' COUNTRY UPDATES")
    print("=" * 40)

    # Get update data
    unknown_updates = create_unknown_country_updates()

    # Load existing country mapping
    try:
        country_df = pd.read_csv("final_country_mapping.csv")
        print(f"Loaded existing country mapping: {len(country_df)} shows")
    except FileNotFoundError:
        country_df = pd.DataFrame(columns=["normalized_name", "country", "source"])
        print("Created new country mapping")

    # Update existing entries and add new ones
    updated_country_data = []
    existing_shows = set(country_df["normalized_name"]) if not country_df.empty else set()

    # Add existing data (with updates for 'Unknown' shows)
    for _, row in country_df.iterrows():
        show_name = row["normalized_name"]
        if show_name in unknown_updates:
            # Update the country for this show
            new_country, description = unknown_updates[show_name]
            updated_country_data.append({
                "normalized_name": show_name,
                "country": new_country,
                "source": f"Tavily research update: {description}"
            })
            print(f"  ✓ Updated: {show_name} -> {new_country}")
        else:
            # Keep existing classification
            updated_country_data.append({
                "normalized_name": show_name,
                "country": row["country"],
                "source": row["source"]
            })

    # Add any new shows not in existing mapping
    for show, (country, description) in unknown_updates.items():
        if show not in existing_shows:
            updated_country_data.append({
                "normalized_name": show,
                "country": country,
                "source": f"Tavily research: {description}"
            })
            print(f"  + Added: {show} -> {country}")

    # Create updated DataFrame
    updated_country_df = pd.DataFrame(updated_country_data)
    updated_country_df = updated_country_df.drop_duplicates(subset=["normalized_name"], keep="first")

    # Save updated mapping
    updated_country_df.to_csv("final_country_mapping_updated.csv", index=False)

    print(f"✓ Updated country mapping: {len(updated_country_df)} shows")

    # Show updated distributions
    country_dist = updated_country_df["country"].value_counts()
    print(f"\nUpdated country distribution:")
    for country, count in country_dist.head(10).items():
        print(f"  {country}: {count} shows")

    return updated_country_df

def regenerate_rankings_with_updated_countries():
    """Regenerate final rankings with updated country classifications."""

    print(f"\nREGENERATING RANKINGS WITH UPDATED COUNTRIES")
    print("=" * 50)

    # Run the complete ranking system with updated mappings
    import subprocess
    result = subprocess.run(["python3", "complete_5platform_ranking_system.py"],
                          capture_output=True, text=True)

    if result.returncode == 0:
        print("✓ Successfully regenerated rankings with updated countries")

        # Load and analyze the results
        try:
            final_rankings = pd.read_csv("final_5platform_podcast_rankings.csv")

            # Check country improvements
            unknown_count = len(final_rankings[final_rankings["country"] == "Unknown"])
            total_shows = len(final_rankings)

            print(f"\nFinal country classification results:")
            print(f"  Total shows ranked: {total_shows}")
            print(f"  Shows still with 'Unknown' country: {unknown_count}")
            print(f"  Country classification improvement: {((total_shows - unknown_count) / total_shows * 100):.1f}% classified")

            # Show country distribution
            country_dist = final_rankings["country"].value_counts()
            print(f"\nTop 10 countries represented:")
            for country, count in country_dist.head(10).items():
                print(f"  {country}: {count} shows")

            return final_rankings

        except FileNotFoundError:
            print("✗ Could not load final rankings file")
            return None
    else:
        print(f"✗ Error regenerating rankings: {result.stderr}")
        return None

if __name__ == "__main__":
    # Apply country updates for 'Unknown' shows
    updated_country_mapping = apply_unknown_country_updates()

    # Regenerate final rankings
    final_rankings = regenerate_rankings_with_updated_countries()

    print(f"\n🎯 'UNKNOWN' COUNTRY CLASSIFICATION UPDATE COMPLETE!")
    if final_rankings is not None:
        print(f"   Updated CSV: final_5platform_podcast_rankings.csv")
        print(f"   Significantly improved country classification coverage!")