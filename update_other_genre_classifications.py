#!/usr/bin/env python3
"""
Update genre classifications for shows currently marked as 'Other' based on Tavily research
"""

import pandas as pd
import re

def create_other_genre_updates():
    """Create comprehensive genre updates for shows marked as 'Other' based on Tavily research."""

    print("CREATING COMPREHENSIVE 'OTHER' GENRE UPDATES")
    print("=" * 55)

    # Based on Tavily research for top "Other" genre shows
    other_genre_updates = {
        # Business & Interview shows
        "the diary of a ceo": ("Business", "Steven Bartlett business/entrepreneurship interview podcast"),

        # News & Politics shows
        "rita panahi": ("News & Politics", "Sky News Australia political commentary show"),
        "brian tyler cohen": ("News & Politics", "Progressive political commentary podcast 'No Lie'"),
        "the luke beasley": ("News & Politics", "Progressive political commentary program"),
        "권순표의 뉴스 하이킥 2025": ("News & Politics", "Korean news and political commentary show"),
        "political analysis": ("News & Politics", "Political analysis and commentary content"),
        "hoy en negocios televisión": ("News & Politics", "Spanish business and news television program"),
        "banglavision world news banglavision": ("News & Politics", "Bangladeshi news and current affairs"),

        # True Crime & Legal shows
        "lawcrime sidebar": ("True Crime", "Law & Crime legal analysis and trial coverage podcast"),

        # Science & Education shows
        "the why files operation": ("Education", "Science, paranormal, and mystery educational content"),

        # Entertainment & Media shows
        "víctor y alba en vivo": ("Entertainment", "Spanish-language entertainment show"),
        "close the door": ("Entertainment", "Indonesian entertainment content"),
        "figuring out": ("Entertainment", "Indian entertainment and lifestyle content"),
        "podhub": ("Entertainment", "Indonesian entertainment podcast hub"),
        "ihip news": ("News & Politics", "News and current affairs content"),
        "dr insanity podcasts": ("Entertainment", "Entertainment and commentary content"),
        "the devory darkins": ("News & Politics", "Political commentary and news analysis"),

        # International content by language/region
        "curhat bang denny sumargo": ("Entertainment", "Indonesian celebrity interview and entertainment"),
        "ceo dan cinderella": ("Business", "Indonesian business and entrepreneurship content"),
        "las alucines": ("Comedy", "Mexican comedy and entertainment content"),
        "teenmaar varthalu by v6": ("News & Politics", "Indian Telugu news and current affairs"),
        "full surahs": ("Society & Culture", "Islamic religious and cultural content"),
        "a closer look late night": ("Comedy", "Late night comedy commentary content"),

        # Additional classifications from research
        "matt and shanes secret": ("Comedy", "Comedy podcast by Matt McCusker and Shane Gillis"),
        "candace": ("News & Politics", "Candace Owens political commentary"),
        "creepcast": ("Entertainment", "Horror and creepy story entertainment content"),
        "pbd": ("Business", "Patrick Bet-David business and entrepreneurship podcast"),
        "giggly squad": ("Comedy", "Comedy podcast by Hannah Berner and Paige DeSorbo"),
        "the basement yard": ("Comedy", "Comedy podcast by Joe Santagato and Frankie Alvarez"),
        "2 bears 1 cave": ("Comedy", "Comedy podcast by Tom Segura and Bert Kreischer"),
        "lex fridman": ("Interview & Talk", "AI, science, and technology interview podcast"),
        "your moms house": ("Comedy", "Comedy podcast by Tom Segura and Christina Pazsitzky"),
        "conspiracy theories": ("Entertainment", "Conspiracy theory entertainment content"),
        "the rewatchables": ("Entertainment", "Movie discussion and entertainment podcast"),
        "murder": ("True Crime", "True crime content and stories"),
        "serial killers": ("True Crime", "True crime podcast about serial killers"),
        "behind the bastards": ("Education", "Historical education about controversial figures"),
        "critical role": ("Entertainment", "Dungeons & Dragons entertainment content"),
        "the viall files": ("Interview & Talk", "Nick Viall relationship and interview podcast"),
        "club random": ("Interview & Talk", "Bill Maher interview and discussion podcast")
    }

    print(f"✓ Genre updates prepared for {len(other_genre_updates)} shows")

    return other_genre_updates

def apply_other_genre_updates():
    """Apply genre updates to existing mappings for 'Other' shows."""

    print("\nAPPLYING 'OTHER' GENRE UPDATES")
    print("=" * 35)

    # Get update data
    other_updates = create_other_genre_updates()

    # Load existing genre mapping
    try:
        genre_df = pd.read_csv("final_genre_mapping.csv")
        print(f"Loaded existing genre mapping: {len(genre_df)} shows")
    except FileNotFoundError:
        genre_df = pd.DataFrame(columns=["normalized_name", "genre", "source"])
        print("Created new genre mapping")

    # Update existing entries and add new ones
    updated_genre_data = []
    existing_shows = set(genre_df["normalized_name"]) if not genre_df.empty else set()

    # Add existing data (with updates for 'Other' shows)
    for _, row in genre_df.iterrows():
        show_name = row["normalized_name"]
        if show_name in other_updates:
            # Update the genre for this show
            new_genre, description = other_updates[show_name]
            updated_genre_data.append({
                "normalized_name": show_name,
                "genre": new_genre,
                "source": f"Tavily research update: {description}"
            })
            print(f"  ✓ Updated: {show_name} -> {new_genre}")
        else:
            # Keep existing classification
            updated_genre_data.append({
                "normalized_name": show_name,
                "genre": row["genre"],
                "source": row["source"]
            })

    # Add any new shows not in existing mapping
    for show, (genre, description) in other_updates.items():
        if show not in existing_shows:
            updated_genre_data.append({
                "normalized_name": show,
                "genre": genre,
                "source": f"Tavily research: {description}"
            })
            print(f"  + Added: {show} -> {genre}")

    # Create updated DataFrame
    updated_genre_df = pd.DataFrame(updated_genre_data)
    updated_genre_df = updated_genre_df.drop_duplicates(subset=["normalized_name"], keep="first")

    # Save updated mapping
    updated_genre_df.to_csv("final_genre_mapping_updated.csv", index=False)

    print(f"✓ Updated genre mapping: {len(updated_genre_df)} shows")

    # Show updated distributions
    genre_dist = updated_genre_df["genre"].value_counts()
    print(f"\nUpdated genre distribution:")
    for genre, count in genre_dist.head(10).items():
        print(f"  {genre}: {count} shows")

    return updated_genre_df

def regenerate_rankings_with_updates():
    """Regenerate final rankings with updated genre classifications."""

    print(f"\nREGENERATING RANKINGS WITH UPDATED GENRES")
    print("=" * 45)

    # Run the complete ranking system with updated mappings
    import subprocess
    result = subprocess.run(["python3", "complete_5platform_ranking_system.py"],
                          capture_output=True, text=True)

    if result.returncode == 0:
        print("✓ Successfully regenerated rankings with updated genres")

        # Load and analyze the results
        try:
            final_rankings = pd.read_csv("final_5platform_podcast_rankings.csv")

            # Check genre improvements
            other_count = len(final_rankings[final_rankings["genre"] == "Other"])
            total_shows = len(final_rankings)

            print(f"\nFinal genre classification results:")
            print(f"  Total shows ranked: {total_shows}")
            print(f"  Shows still with 'Other' genre: {other_count}")
            print(f"  Genre classification improvement: {((total_shows - other_count) / total_shows * 100):.1f}% classified")

            # Show top 10 with updated genres
            print(f"\nTop 10 shows with updated genres:")
            print("-" * 50)
            top_10 = final_rankings.head(10)
            for _, row in top_10.iterrows():
                print(f"{row['rank']:2d}. {row['show_name'].title()}")
                print(f"    Genre: {row['genre']} | Country: {row['country']} | Score: {row['composite_score']:.1f}")

            return final_rankings

        except FileNotFoundError:
            print("✗ Could not load final rankings file")
            return None
    else:
        print(f"✗ Error regenerating rankings: {result.stderr}")
        return None

if __name__ == "__main__":
    # Apply genre updates for 'Other' shows
    updated_genre_mapping = apply_other_genre_updates()

    # Regenerate final rankings
    final_rankings = regenerate_rankings_with_updates()

    print(f"\n🎯 'OTHER' GENRE CLASSIFICATION UPDATE COMPLETE!")
    if final_rankings is not None:
        print(f"   Updated CSV: final_5platform_podcast_rankings.csv")
        print(f"   Significantly improved genre classification coverage!")