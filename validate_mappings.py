#!/usr/bin/env python3
"""
Validate genre and country mappings against original source data.
"""

import pandas as pd
import re


def normalize_name(name):
    """Same normalization as ranking system."""
    if pd.isna(name) or not name:
        return ''
    normalized = str(name).strip().lower()

    suffixes = [
        r'\s+the\s+podcast$',
        r'\s+podcast$',
        r'\s+the\s+show$',
        r'\s+show$',
        r'\s+with\s+stugotz$',
        r'\s+with\s+dax\s+shepard$',
        r'\s+with\s+karen\s+kilgariff\s+and\s+georgia\s+hardstark$',
        r'\s+with\s+matt\s+rogers\s+and\s+bowen\s+yang$',
        r'\s+with\s+rhett\s+link$',
        r'\s+w\s+theo\s+von$',
        r'\s+w/\s+theo\s+von$',
    ]

    for suffix in suffixes:
        normalized = re.sub(suffix, '', normalized, flags=re.IGNORECASE)

    normalized = re.sub(r'[^\w\s]', '', normalized)
    normalized = re.sub(r'\s+', ' ', normalized).strip()

    return normalized


def check_amazon_genres():
    """Check Amazon Category Name against our genre mapping."""
    print("=== VALIDATING AMAZON GENRES ===\n")

    amazon = pd.read_csv('data/amazon.csv', skiprows=2, low_memory=False)
    amazon_clean = amazon.dropna(subset=['Show Title'])
    amazon_clean['normalized'] = amazon_clean['Show Title'].apply(normalize_name)

    # Load our genre mapping
    genre_map = pd.read_csv('union_genre_mapping.csv')

    issues = []
    matches = []

    for _, row in amazon_clean.iterrows():
        show_name = row['Show Title']
        amazon_genre = row['Category Name']
        normalized = row['normalized']

        # Find in our mapping
        our_mapping = genre_map[genre_map['normalized_name'] == normalized]

        if len(our_mapping) > 0:
            our_genre = our_mapping.iloc[0]['final_genre']

            # Map Amazon categories to our standard categories
            amazon_to_standard = {
                'True Crime': 'True Crime',
                'Comedy': 'Comedy',
                'News': 'News & Politics',
                'Leisure': 'Entertainment',
                'Business': 'Business',
                'Sports': 'Sports',
                'Society & Culture': 'Education',
            }

            expected_genre = amazon_to_standard.get(amazon_genre, amazon_genre)

            if our_genre != expected_genre:
                issues.append({
                    'show': show_name,
                    'amazon_genre': amazon_genre,
                    'our_genre': our_genre,
                    'normalized': normalized
                })
            else:
                matches.append(show_name)
        else:
            issues.append({
                'show': show_name,
                'amazon_genre': amazon_genre,
                'our_genre': 'NOT MAPPED',
                'normalized': normalized
            })

    print(f"Amazon shows in our mapping: {len(matches)}/{len(amazon_clean)}")
    print(f"Issues found: {len(issues)}\n")

    if issues:
        print("Genre mismatches or missing mappings:")
        for issue in issues:
            print(f"  {issue['show']}")
            print(f"    Amazon: {issue['amazon_genre']} | Our mapping: {issue['our_genre']}")
            print(f"    Normalized: {issue['normalized']}")
            print()

    return issues


def check_youtube_countries():
    """Check YouTube FeatureCountry against our country mapping."""
    print("\n=== VALIDATING YOUTUBE COUNTRIES ===\n")

    youtube = pd.read_csv('data/youtube.csv')
    youtube['normalized'] = youtube['playlist_name'].apply(normalize_name)

    # Load our country mapping
    country_map = pd.read_csv('comprehensive_country_mapping.csv')

    issues = []
    matches = []

    for _, row in youtube.iterrows():
        show_name = row['playlist_name']
        yt_country = row['FeatureCountry']
        normalized = row['normalized']

        # Find in our mapping
        our_mapping = country_map[country_map['normalized_name'] == normalized]

        if len(our_mapping) > 0:
            our_country = our_mapping.iloc[0]['country']

            # Check if YouTube country matches our mapping
            if pd.notna(yt_country):
                if our_country != yt_country:
                    issues.append({
                        'show': show_name,
                        'youtube_country': yt_country,
                        'our_country': our_country,
                        'normalized': normalized
                    })
                else:
                    matches.append(show_name)
        else:
            if pd.notna(yt_country):
                issues.append({
                    'show': show_name,
                    'youtube_country': yt_country,
                    'our_country': 'NOT MAPPED',
                    'normalized': normalized
                })

    print(f"YouTube shows with matching country: {len(matches)}")
    print(f"Issues found: {len(issues)}\n")

    if issues:
        print("Country mismatches or missing mappings:")
        for issue in issues:
            print(f"  {issue['show']}")
            print(f"    YouTube: {issue['youtube_country']} | Our mapping: {issue['our_country']}")
            print(f"    Normalized: {issue['normalized']}")
            print()

    return issues


def get_all_shows_for_validation():
    """Get all unique shows that need genre/country validation."""
    print("\n=== ALL SHOWS REQUIRING VALIDATION ===\n")

    # Load all platforms
    spotify = pd.read_csv('data/spotify.csv', skiprows=7)
    spotify.columns = ['show_name', 'plays', 'category']
    spotify['normalized'] = spotify['show_name'].apply(normalize_name)

    youtube = pd.read_csv('data/youtube.csv')
    youtube['normalized'] = youtube['playlist_name'].apply(normalize_name)
    youtube = youtube[(youtube['FeatureCountry'] == 'US') | youtube['FeatureCountry'].isna()]

    amazon = pd.read_csv('data/amazon.csv', skiprows=2, low_memory=False)
    amazon = amazon.dropna(subset=['Show Title'])
    amazon['normalized'] = amazon['Show Title'].apply(normalize_name)

    apple = pd.read_csv('data/apple.csv')
    apple['normalized'] = apple['Podcast'].apply(normalize_name)

    iheart = pd.read_csv('data/iheart_platform_nominations.csv', skiprows=2)
    iheart.columns = ['rank', 'show_name', 'listeners', 'streams', 'completion', 'followers']
    iheart = iheart.dropna(subset=['show_name'])
    iheart['normalized'] = iheart['show_name'].apply(normalize_name)

    # Load mappings
    genre_map = pd.read_csv('union_genre_mapping.csv')
    country_map = pd.read_csv('comprehensive_country_mapping.csv')

    # Get all unique normalized names
    all_normalized = set()
    all_normalized.update(spotify['normalized'].tolist())
    all_normalized.update(youtube['normalized'].tolist())
    all_normalized.update(amazon['normalized'].tolist())
    all_normalized.update(apple['normalized'].tolist())
    all_normalized.update(iheart['normalized'].tolist())

    # Check coverage
    genre_covered = set(genre_map['normalized_name'].tolist())
    country_covered = set(country_map['normalized_name'].tolist())

    missing_genre = all_normalized - genre_covered
    missing_country = all_normalized - country_covered

    print(f"Total unique shows: {len(all_normalized)}")
    print(f"Genre coverage: {len(genre_covered)}/{len(all_normalized)}")
    print(f"Country coverage: {len(country_covered)}/{len(all_normalized)}")

    if missing_genre:
        print(f"\nMissing genre mappings ({len(missing_genre)} shows):")
        for name in sorted(missing_genre):
            # Find original name
            orig = None
            for df, col in [(spotify, 'show_name'), (youtube, 'playlist_name'),
                           (amazon, 'Show Title'), (apple, 'Podcast'), (iheart, 'show_name')]:
                match = df[df['normalized'] == name]
                if len(match) > 0:
                    if col == 'Show Title':
                        orig = match.iloc[0]['Show Title']
                    elif col == 'playlist_name':
                        orig = match.iloc[0]['playlist_name']
                    else:
                        orig = match.iloc[0][col]
                    break
            print(f"  {name} (original: {orig})")

    if missing_country:
        print(f"\nMissing country mappings ({len(missing_country)} shows):")
        for name in sorted(missing_country):
            # Find original name and YouTube country if available
            orig = None
            yt_country = None
            for df, col in [(spotify, 'show_name'), (youtube, 'playlist_name'),
                           (amazon, 'Show Title'), (apple, 'Podcast'), (iheart, 'show_name')]:
                match = df[df['normalized'] == name]
                if len(match) > 0:
                    if col == 'Show Title':
                        orig = match.iloc[0]['Show Title']
                    elif col == 'playlist_name':
                        orig = match.iloc[0]['playlist_name']
                        if 'FeatureCountry' in match.columns:
                            yt_country = match.iloc[0]['FeatureCountry']
                    else:
                        orig = match.iloc[0][col]
                    break
            yt_info = f" [YouTube: {yt_country}]" if yt_country and pd.notna(yt_country) else ""
            print(f"  {name} (original: {orig}){yt_info}")

    return missing_genre, missing_country


if __name__ == "__main__":
    # Run validations
    amazon_issues = check_amazon_genres()
    youtube_issues = check_youtube_countries()
    missing_genre, missing_country = get_all_shows_for_validation()

    print("\n=== SUMMARY ===")
    print(f"Amazon genre issues: {len(amazon_issues)}")
    print(f"YouTube country issues: {len(youtube_issues)}")
    print(f"Missing genre mappings: {len(missing_genre)}")
    print(f"Missing country mappings: {len(missing_country)}")

    if amazon_issues or youtube_issues or missing_genre or missing_country:
        print("\n⚠️  Issues found - mappings need updates")
    else:
        print("\n✓ All validations passed!")
