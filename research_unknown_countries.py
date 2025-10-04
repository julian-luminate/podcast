#!/usr/bin/env python3
"""
Research country information for all shows with 'Unknown' country classification
Using Tavily search and Wikipedia to identify podcast origins
"""

import pandas as pd
import time
import json

def load_unknown_country_shows():
    """Load all shows with Unknown country classification."""

    print("LOADING SHOWS WITH UNKNOWN COUNTRY")
    print("=" * 40)

    # Load current rankings
    df = pd.read_csv('final_5platform_podcast_rankings.csv')

    # Filter to Unknown country shows
    unknown_shows = df[df['country'] == 'Unknown'].copy()

    # Clean show names (remove 'nan' entries)
    unknown_shows = unknown_shows[unknown_shows['show_name'].notna()]
    unknown_shows = unknown_shows[unknown_shows['show_name'] != 'nan']

    print(f"Found {len(unknown_shows)} shows with Unknown country")
    return unknown_shows['show_name'].tolist()

def research_podcast_country_batch(shows_batch, batch_num):
    """Research country information for a batch of shows using web search."""

    print(f"\nRESEARCHING BATCH {batch_num} ({len(shows_batch)} shows)")
    print("=" * 50)

    country_results = {}

    for i, show in enumerate(shows_batch):
        print(f"  {i+1:2d}/{len(shows_batch)} Researching: {show}")

        try:
            # Search for podcast information
            from mcp__tavily__search import mcp__tavily__search

            # Create search query
            search_query = f'"{show}" podcast host country origin where created'

            search_results = mcp__tavily__search({
                "query": search_query,
                "options": {
                    "maxResults": 3,
                    "includeAnswer": True,
                    "searchDepth": "basic"
                }
            })

            # Extract country information from search results
            country = extract_country_from_search(search_results, show)

            if country:
                country_results[show] = country
                print(f"     ✓ Found: {country}")
            else:
                print(f"     ⚠ No clear country found")
                country_results[show] = "Unknown"

            # Rate limiting
            time.sleep(0.5)

        except Exception as e:
            print(f"     ✗ Error searching {show}: {e}")
            country_results[show] = "Unknown"

    return country_results

def extract_country_from_search(search_results, show_name):
    """Extract country information from Tavily search results."""

    # Common country indicators
    country_keywords = {
        "united states": "US", "usa": "US", "america": "US", "american": "US",
        "united kingdom": "GB", "uk": "GB", "britain": "GB", "british": "GB", "england": "GB",
        "canada": "CA", "canadian": "CA",
        "australia": "AU", "australian": "AU",
        "germany": "DE", "german": "DE",
        "france": "FR", "french": "FR",
        "spain": "ES", "spanish": "ES",
        "italy": "IT", "italian": "IT",
        "japan": "JP", "japanese": "JP",
        "south korea": "KR", "korea": "KR", "korean": "KR",
        "india": "IN", "indian": "IN",
        "china": "CN", "chinese": "CN",
        "russia": "RU", "russian": "RU",
        "brazil": "BR", "brazilian": "BR",
        "mexico": "MX", "mexican": "MX",
        "argentina": "AR", "argentine": "AR",
        "colombia": "CO", "colombian": "CO",
        "chile": "CL", "chilean": "CL",
        "peru": "PE", "peruvian": "PE",
        "netherlands": "NL", "dutch": "NL",
        "sweden": "SE", "swedish": "SE",
        "norway": "NO", "norwegian": "NO",
        "denmark": "DK", "danish": "DK",
        "finland": "FI", "finnish": "FI",
        "poland": "PL", "polish": "PL",
        "ukraine": "UA", "ukrainian": "UA",
        "indonesia": "ID", "indonesian": "ID",
        "thailand": "TH", "thai": "TH",
        "singapore": "SG",
        "malaysia": "MY", "malaysian": "MY",
        "philippines": "PH", "filipino": "PH",
        "vietnam": "VN", "vietnamese": "VN",
        "turkey": "TR", "turkish": "TR",
        "israel": "IL", "israeli": "IL",
        "egypt": "EG", "egyptian": "EG",
        "south africa": "ZA", "african": "ZA",
        "new zealand": "NZ", "zealand": "NZ",
        "ireland": "IE", "irish": "IE",
        "portugal": "PT", "portuguese": "PT",
        "belgium": "BE", "belgian": "BE",
        "austria": "AT", "austrian": "AT",
        "switzerland": "CH", "swiss": "CH",
        "czech": "CZ", "slovakia": "SK", "hungary": "HU",
        "romania": "RO", "bulgaria": "BG", "croatia": "HR",
        "greece": "GR", "greek": "GR"
    }

    # Search in results content
    all_text = ""

    if isinstance(search_results, dict) and 'results' in search_results:
        for result in search_results['results']:
            if 'content' in result:
                all_text += result['content'].lower() + " "
            if 'title' in result:
                all_text += result['title'].lower() + " "

    # Look for country indicators
    for country_term, country_code in country_keywords.items():
        if country_term in all_text:
            return country_code

    # Special cases for well-known shows
    special_cases = {
        "conan obrien": "US",
        "howard stern": "US",
        "joe rogan": "US",
        "marc maron": "US",
        "bill maher": "US",
        "snl": "US",
        "saturday night live": "US",
        "late night": "US",
        "tonight show": "US",
        "daily show": "US",
        "npr": "US",
        "pbs": "US",
        "cbc": "CA",
        "bbc": "GB",
        "abc": "US",
        "nbc": "US",
        "cbs": "US",
        "fox": "US",
        "cnn": "US",
        "espn": "US"
    }

    show_lower = show_name.lower()
    for indicator, country in special_cases.items():
        if indicator in show_lower:
            return country

    return None

def research_with_wikipedia_fallback(shows_with_unknown):
    """Research remaining unknown shows with Wikipedia search."""

    print(f"\nWIKIPEDIA FALLBACK RESEARCH")
    print("=" * 30)

    country_results = {}

    for i, show in enumerate(shows_with_unknown):
        print(f"  {i+1}/{len(shows_with_unknown)} Wikipedia: {show}")

        try:
            from mcp__Wikipedia__search import mcp__Wikipedia__search

            # Search Wikipedia
            wiki_results = mcp__Wikipedia__search({
                "query": f"{show} podcast"
            })

            if wiki_results and len(wiki_results) > 0:
                # Read the first relevant article
                from mcp__Wikipedia__readArticle import mcp__Wikipedia__readArticle

                article = mcp__Wikipedia__readArticle({
                    "pageId": wiki_results[0]["pageId"]
                })

                # Extract country from article
                country = extract_country_from_text(article["content"], show)

                if country:
                    country_results[show] = country
                    print(f"     ✓ Wikipedia found: {country}")
                else:
                    country_results[show] = "Unknown"
                    print(f"     ⚠ No country in Wikipedia")
            else:
                country_results[show] = "Unknown"
                print(f"     ⚠ Not found on Wikipedia")

            time.sleep(0.3)

        except Exception as e:
            print(f"     ✗ Wikipedia error: {e}")
            country_results[show] = "Unknown"

    return country_results

def extract_country_from_text(text, show_name):
    """Extract country from Wikipedia article text."""

    country_keywords = {
        "united states": "US", "american": "US", "u.s.": "US",
        "united kingdom": "GB", "british": "GB", "uk": "GB", "england": "GB",
        "canada": "CA", "canadian": "CA",
        "australia": "AU", "australian": "AU",
        "germany": "DE", "german": "DE",
        "france": "FR", "french": "FR",
        "japan": "JP", "japanese": "JP",
        "south korea": "KR", "korean": "KR",
        "india": "IN", "indian": "IN",
        "china": "CN", "chinese": "CN"
    }

    text_lower = text.lower()

    for country_term, country_code in country_keywords.items():
        if country_term in text_lower:
            return country_code

    return None

def save_country_research_results(all_results):
    """Save research results and update mapping files."""

    print(f"\nSAVING COUNTRY RESEARCH RESULTS")
    print("=" * 35)

    # Load existing country mapping if it exists
    try:
        existing_mapping = pd.read_csv("final_country_mapping.csv")
        existing_dict = dict(zip(existing_mapping["normalized_name"], existing_mapping["country"]))
        print(f"Loaded existing mapping: {len(existing_dict)} shows")
    except FileNotFoundError:
        existing_dict = {}
        print("Creating new country mapping")

    # Update with research results
    updated_count = 0
    for show, country in all_results.items():
        if country != "Unknown" and show not in existing_dict:
            existing_dict[show] = country
            updated_count += 1

    # Create updated mapping dataframe
    mapping_data = []
    for show, country in existing_dict.items():
        mapping_data.append({
            "normalized_name": show,
            "country": country,
            "source": "Web research" if show in all_results else "Previous mapping"
        })

    updated_mapping_df = pd.DataFrame(mapping_data)
    updated_mapping_df.to_csv("final_country_mapping_updated.csv", index=False)

    print(f"✓ Updated country mapping: {len(updated_mapping_df)} shows")
    print(f"✓ New countries found: {updated_count}")

    # Show country distribution
    country_dist = updated_mapping_df["country"].value_counts()
    print(f"\nCountry distribution:")
    for country, count in country_dist.head(10).items():
        print(f"  {country}: {count} shows")

    return updated_mapping_df

def main():
    """Main function to research all unknown countries."""

    # Load shows with unknown countries
    unknown_shows = load_unknown_country_shows()

    if not unknown_shows:
        print("No shows with Unknown country found!")
        return

    print(f"Starting research for {len(unknown_shows)} shows...")

    # Process in batches to avoid rate limits
    batch_size = 20
    all_results = {}

    for i in range(0, len(unknown_shows), batch_size):
        batch = unknown_shows[i:i+batch_size]
        batch_num = (i // batch_size) + 1

        batch_results = research_podcast_country_batch(batch, batch_num)
        all_results.update(batch_results)

        print(f"Batch {batch_num} complete: {len([r for r in batch_results.values() if r != 'Unknown'])} countries found")

        # Save intermediate results
        if len(all_results) % 40 == 0:
            save_country_research_results(all_results)

    # Final save
    final_mapping = save_country_research_results(all_results)

    print(f"\n🎯 COUNTRY RESEARCH COMPLETE!")
    print(f"   📋 Researched: {len(unknown_shows)} shows")
    print(f"   🌍 Countries found: {len([r for r in all_results.values() if r != 'Unknown'])}")
    print(f"   📄 Updated mapping: final_country_mapping_updated.csv")
    print(f"   🚀 Ready to update ranking system!")

if __name__ == "__main__":
    main()