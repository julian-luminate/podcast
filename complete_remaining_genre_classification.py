#!/usr/bin/env python3
"""
Complete classification for all remaining 150 shows with 'Other' genre
Based on show names, common podcast patterns, and research
"""

import pandas as pd

def create_complete_remaining_genre_classifications():
    """Create comprehensive genre classifications for all 150 remaining Other shows."""

    print("CREATING COMPLETE REMAINING GENRE CLASSIFICATIONS")
    print("=" * 60)

    # Complete genre classifications for all 150 remaining shows
    remaining_genre_classifications = {
        # Sports & Entertainment
        "the dan le batard": "Sports",  # Dan Le Batard Show - ESPN sports talk
        "the herd": "Sports",  # Colin Cowherd sports talk show
        "the dan patrick": "Sports",  # Dan Patrick Show sports radio
        "fantasy footballers fantasy football": "Sports",  # Fantasy football podcast
        "nfl daily": "Sports",  # NFL focused content
        "the ryen russillo": "Sports",  # Bill Simmons network sports content

        # News & Politics
        "the ezra klein": "News & Politics",  # New York Times political podcast
        "the matt walsh": "News & Politics",  # Daily Wire political commentary
        "morning wire": "News & Politics",  # Daily Wire morning news
        "the charlie kirk": "News & Politics",  # Turning Point USA conservative politics
        "the victor davis hanson": "News & Politics",  # Political commentary and history
        "the stephen a smith": "News & Politics",  # ESPN personality political commentary
        "this is gavin newsom": "News & Politics",  # California Governor political content

        # Interview & Talk Shows
        "the joe budden": "Interview & Talk",  # Hip-hop culture and celebrity interviews
        "the bobby bones": "Interview & Talk",  # Country music radio show host
        "elvis duran and the morning on demand": "Interview & Talk",  # Morning radio show
        "the steve harvey morning": "Interview & Talk",  # Steve Harvey morning radio show
        "club shay shay": "Interview & Talk",  # Shannon Sharpe interview show
        "the dr john delony": "Interview & Talk",  # Mental health and advice show
        "the meateater": "Interview & Talk",  # Hunting and outdoor lifestyle interviews

        # True Crime
        "murder in america": "True Crime",  # True crime podcast series
        "true crime": "True Crime",  # Generic true crime content
        "crime conspiracy cults and murder": "True Crime",  # True crime investigations
        "just creepy scary stories": "True Crime",  # Horror and crime stories
        "cold case files miami": "True Crime",  # Cold case investigations
        "murder on the towpath": "True Crime",  # Specific true crime case
        "devil in the desert": "True Crime",  # True crime investigation
        "murder on songbird road": "True Crime",  # True crime case study
        "american homicide": "True Crime",  # American true crime cases
        "murder true crime stories": "True Crime",  # True crime storytelling
        "the idaho massacre": "True Crime",  # Specific true crime case
        "the greatest true crime stories ever told": "True Crime",  # True crime anthology
        "what happened to talina zar": "True Crime",  # Missing person case
        "bone valley": "True Crime",  # True crime investigation
        "up and vanished": "True Crime",  # Missing persons true crime
        "happy face": "True Crime",  # Serial killer case study
        "monster btk": "True Crime",  # BTK serial killer case
        "counterclock": "True Crime",  # True crime investigations
        "crook county": "True Crime",  # Criminal justice true crime
        "intentionally disturbing": "True Crime",  # Dark true crime content
        "crime stories": "True Crime",  # General true crime stories

        # Comedy
        "the tim dillon": "Comedy",  # Stand-up comedian podcast
        "anything goes": "Comedy",  # Emma Chamberlain comedy/lifestyle
        "dungeons and daddies": "Comedy",  # Comedy D&D podcast
        "my brother my brother and me": "Comedy",  # McElroy Brothers comedy advice
        "the broski report": "Comedy",  # Brittany Broski comedy content
        "and thats why we drink": "Comedy",  # Comedy true crime/paranormal
        "office ladies": "Comedy",  # The Office TV show comedy discussion
        "the bald and the beautiful": "Comedy",  # Trixie and Katya drag comedy
        "are you garbage comedy": "Comedy",  # Comedy podcast about being trashy
        "the yard": "Comedy",  # Comedy gaming podcast
        "stavvys world": "Comedy",  # Stavros Halkias comedy podcast
        "therapuss": "Comedy",  # Jake Shane comedy podcast
        "emergency intercom": "Comedy",  # Drew Phillips and Enya Umanzor comedy
        "danny jones": "Comedy",  # Comedy content creator
        "jesser": "Comedy",  # Comedy gaming content

        # Business & Finance
        "morning brew daily": "Business",  # Morning Brew business news
        "allin with chamath jason sacks friedberg": "Business",  # All-In business/tech podcast
        "how to money": "Business",  # Personal finance advice
        "bible in a year": "Society & Culture",  # Religious content
        "unashamed": "Society & Culture",  # Christian lifestyle podcast

        # Entertainment & Pop Culture
        "rotten mango video": "Entertainment",  # Stephanie Soo entertainment content
        "so true": "Entertainment",  # Pop culture commentary
        "the big picture": "Entertainment",  # The Ringer movie podcast
        "pop culture happy hour": "Entertainment",  # NPR pop culture discussion
        "variety confidential": "Entertainment",  # Entertainment industry news
        "the official yellowstone": "Entertainment",  # Yellowstone TV show content
        "pod meets world": "Entertainment",  # Boy Meets World rewatch podcast
        "our american stories": "Entertainment",  # American storytelling
        "all the smoke": "Entertainment",  # Basketball culture and entertainment
        "wisecrack": "Entertainment",  # Philosophy and pop culture analysis

        # Education & Information
        "stuff they dont want you to know": "Education",  # Conspiracy and mystery education
        "stuff you missed in history class": "Education",  # History education
        "ridiculous history": "Education",  # Humorous history content
        "the happiness lab": "Education",  # Psychology and wellness education
        "math magic stories from the frontiers of marketing": "Education",  # Marketing education

        # Technology & Lifestyle
        "andrew schulzs flagrant": "Comedy",  # Andrew Schulz comedy podcast
        "the bulwark": "News & Politics",  # Never Trump conservative commentary
        "timcast irl": "News & Politics",  # Tim Pool political commentary

        # Health & Wellness
        "what now": "Interview & Talk",  # Trevor Noah interview show
        "betrayal weekly": "Society & Culture",  # Relationship and betrayal stories
        "dumb blonde": "Interview & Talk",  # Bunnie XO interview podcast
        "not gonna lie": "Interview & Talk",  # Kylie Kelce lifestyle podcast

        # International/Foreign Language
        "jabab chay bangla জবব চয় বল": "News & Politics",  # Bangladeshi political content
        "比特王新聞": "News & Politics",  # Chinese news content
        "文昭談古論今": "News & Politics",  # Chinese political commentary
        "文昭思緒飛揚podcast": "News & Politics",  # Chinese political discussion

        # Sports Radio/Talk
        "the ben maller": "Sports",  # Sports radio talk show
        "2 pros and a cup of joe": "Sports",  # Sports morning show
        "fox sports radio": "Sports",  # Fox Sports radio content

        # Lifestyle & Advice
        "so supernatural": "Entertainment",  # Supernatural and paranormal content
        "serialously": "True Crime",  # Annie Elise true crime content
        "dark history": "Education",  # Bailey Sarian historical education
        "lore": "Entertainment",  # Folklore and dark stories
        "dateline originals": "True Crime",  # Dateline NBC true crime
        "dateline missing in america": "True Crime",  # Missing persons cases
        "mrballenõs medical mysteries": "True Crime",  # Medical mystery true crime

        # Miscellaneous Talk Shows
        "fly on the wall": "Comedy",  # David Spade and Dana Carvey comedy
        "start here": "News & Politics",  # ABC News morning briefing
        "the way i heard it": "Entertainment",  # Mike Rowe storytelling
        "the best of coast to coast am": "Entertainment",  # Paranormal talk radio
        "drink champs": "Interview & Talk",  # Hip-hop interview show
        "real time": "Entertainment",  # Entertainment and culture discussion
        "therapy gecko": "Interview & Talk",  # Comedy advice show

        # Specialized Content
        "not another dd": "Comedy",  # Comedy podcast
        "chainsfr on spotify": "Entertainment",  # Music and entertainment
        "the lol": "Comedy",  # Comedy content
        "dark downeast": "True Crime",  # Maine true crime stories
        "two ts in a pod": "Interview & Talk",  # Tamra Judge and Teddi Mellencamp
        "ok storytime": "Entertainment",  # Storytelling content
        "true crime tonight": "True Crime",  # Nightly true crime content
        "disgraceland": "Entertainment",  # Music history and crime
        "amy robach tj holmes present": "News & Politics",  # News personalities
        "post run high": "Sports",  # Running and fitness content
        "the odd couple": "Sports",  # Sports talk show
        "it could happen here": "News & Politics",  # Political crisis discussion
        "run that prank": "Comedy",  # Prank comedy content
        "three": "Entertainment",  # General entertainment content
        "dear chelsea": "Comedy",  # Chelsea Handler comedy advice
        "my friend daisy": "Comedy",  # Comedy friendship content
        "strawberry letter": "Interview & Talk",  # Steve Harvey relationship advice
        "conan oõbrien needs a friend": "Comedy",  # Conan O'Brien comedy interview
        "bobbycast": "Interview & Talk",  # Bobby Bones interview content
        "bookmarked by reeses book club": "Education",  # Book discussion and literature
        "the nikki glaser": "Comedy",  # Nikki Glaser comedy podcast
        "health discovered": "Education",  # Health and wellness education
        "ruthies table 4": "Society & Culture",  # Food and culture content
        "40s and free agents": "Interview & Talk",  # Dating and relationship advice
        "hoax": "Education",  # Investigation of hoaxes and misinformation
        "travel": "Education",  # Travel education and advice
        "situationships": "Interview & Talk",  # Relationship advice and dating
        "building abundant success": "Business",  # Business and success advice
        "the season": "Sports",  # Sports seasonal content
        "espn sportscenter update": "Sports",  # ESPN sports news updates
        "black wealth renaissance": "Business",  # Business and wealth building
        "totally 80s": "Entertainment",  # 1980s pop culture and entertainment
        "what are we even doing": "Comedy",  # Comedy lifestyle content
        "klove news": "Society & Culture",  # Christian news and culture
        "i didnõt know maybe you didnõt either": "Education",  # Educational trivia content
        "murder in the moonlight": "True Crime",  # True crime investigation
        "i do part 2": "Interview & Talk",  # Relationship and wedding content
        "united states of kennedy": "News & Politics",  # Kennedy family political content
        "fudd around and find out": "Comedy",  # Comedy firearms content
        "snafu": "News & Politics",  # Military and political commentary
        "scamanda": "True Crime",  # Specific scam investigation
        "boysober": "Interview & Talk",  # Dating and relationship advice
        "sex": "Interview & Talk",  # Sex education and advice
        "the girlfriends jailhouse lawyer season 3": "True Crime",  # Legal true crime
        "the telepathy tapes": "Entertainment",  # Paranormal investigation
        "law order criminal justice systemê season 1 season 2": "True Crime",  # Legal crime content
    }

    print(f"✓ Complete genre classifications prepared for {len(remaining_genre_classifications)} shows")
    return remaining_genre_classifications

def apply_complete_genre_classifications():
    """Apply all remaining genre classifications and create final comprehensive mapping."""

    print("\nAPPLYING COMPLETE GENRE CLASSIFICATIONS")
    print("=" * 45)

    # Get all classifications
    remaining_classifications = create_complete_remaining_genre_classifications()

    # Load existing comprehensive mapping
    try:
        existing_mapping = pd.read_csv("final_genre_mapping_comprehensive.csv")
        print(f"Loaded existing comprehensive mapping: {len(existing_mapping)} shows")
    except FileNotFoundError:
        existing_mapping = pd.DataFrame(columns=["normalized_name", "genre", "source"])
        print("Created new comprehensive mapping")

    # Create complete updated mapping
    all_mapping_data = []

    # Add existing mappings (these take priority)
    for _, row in existing_mapping.iterrows():
        all_mapping_data.append({
            "normalized_name": row["normalized_name"],
            "genre": row["genre"],
            "source": row["source"]
        })

    existing_shows = set(existing_mapping["normalized_name"]) if not existing_mapping.empty else set()

    # Add new classifications for remaining shows
    for show, genre in remaining_classifications.items():
        if show not in existing_shows:
            all_mapping_data.append({
                "normalized_name": show,
                "genre": genre,
                "source": f"Complete classification research: {genre} content"
            })
            print(f"  + Added: {show} -> {genre}")

    # Create final comprehensive mapping
    complete_mapping_df = pd.DataFrame(all_mapping_data)
    complete_mapping_df = complete_mapping_df.drop_duplicates(subset=["normalized_name"], keep="first")

    # Save the complete mapping
    complete_mapping_df.to_csv("final_genre_mapping_complete_all.csv", index=False)

    print(f"✓ Complete comprehensive mapping: {len(complete_mapping_df)} shows")

    # Show genre distribution
    genre_dist = complete_mapping_df["genre"].value_counts()
    print(f"\nComplete genre distribution:")
    for genre, count in genre_dist.items():
        print(f"  {genre}: {count} shows")

    return complete_mapping_df

def update_ranking_system_to_use_complete_mapping():
    """Update the ranking system to use the complete mapping file."""

    print("\nUPDATING RANKING SYSTEM TO USE COMPLETE MAPPING")
    print("=" * 55)

    # Read the current ranking system
    with open("complete_5platform_ranking_system.py", "r") as f:
        content = f.read()

    # Update to prioritize the complete mapping
    updated_content = content.replace(
        'genre_mapping = pd.read_csv("final_genre_mapping_comprehensive.csv")',
        'genre_mapping = pd.read_csv("final_genre_mapping_complete_all.csv")'
    )

    # Write the updated system
    with open("complete_5platform_ranking_system.py", "w") as f:
        f.write(updated_content)

    print("✓ Updated ranking system to use complete mapping file")

    return True

if __name__ == "__main__":
    # Create complete genre classifications
    complete_mapping = apply_complete_genre_classifications()

    # Update ranking system
    update_ranking_system_to_use_complete_mapping()

    print(f"\n🎯 COMPLETE GENRE CLASSIFICATION FINISHED!")
    print(f"   📋 Complete mapping: final_genre_mapping_complete_all.csv")
    print(f"   🔧 Updated ranking system to use complete mapping")
    print(f"   🌟 {len(complete_mapping)} shows with comprehensive genre classifications")
    print(f"   🚀 Ready to regenerate final rankings with complete classifications!")