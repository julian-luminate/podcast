#!/usr/bin/env python3
"""
Update the Japanese show genre from Other to Comedy based on Tavily research
"""

import pandas as pd

def fix_other_genre_show():
    """Update 安住紳一郎の日曜天国 from Other to Comedy genre."""

    # Load union genre mapping
    union_df = pd.read_csv("union_genre_mapping.csv")

    # Find and update the Japanese show
    japanese_show = "安住紳一郎の日曜天国"

    # Check current mapping (should show normalized name)
    print("UPDATING JAPANESE SHOW GENRE")
    print("=" * 40)

    # Look for the show by checking if it contains similar characters
    japanese_mask = union_df['normalized_name'].str.contains('安住紳一郎', na=False)

    if japanese_mask.any():
        current_row = union_df[japanese_mask].iloc[0]
        print(f"Found show: {current_row['normalized_name']}")
        print(f"Current genre: {current_row['final_genre']}")
        print(f"Current sources: {current_row['source_summary']}")

        # Update the genre based on Tavily research
        union_df.loc[japanese_mask, 'final_genre'] = 'Comedy'
        union_df.loc[japanese_mask, 'tavily_genre'] = 'Comedy'

        # Update source summary
        current_sources = current_row['source_summary']
        if 'Tavily research' not in current_sources:
            new_sources = current_sources + ' + Tavily research' if current_sources else 'Tavily research'
            union_df.loc[japanese_mask, 'source_summary'] = new_sources

        # Save updated mapping
        union_df.to_csv("union_genre_mapping.csv", index=False)

        print(f"Updated to: Comedy")
        print(f"Research evidence: TBS radio comedy talk show format")
        print("✓ Genre mapping updated successfully")

    else:
        print("Japanese show not found in mapping")
        # Try to find any show with "Other" genre
        other_shows = union_df[union_df['final_genre'] == 'Other']
        if len(other_shows) > 0:
            print(f"Found {len(other_shows)} shows with Other genre:")
            for _, row in other_shows.iterrows():
                print(f"  - {row['normalized_name']}")
        else:
            print("No shows found with Other genre")

if __name__ == "__main__":
    fix_other_genre_show()