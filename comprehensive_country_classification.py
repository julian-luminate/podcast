#!/usr/bin/env python3
"""
Comprehensive country classification for all Unknown shows
Based on host names, network affiliations, and podcast knowledge
"""

import pandas as pd

def create_comprehensive_country_classifications():
    """Create comprehensive country classifications based on podcast knowledge."""

    print("CREATING COMPREHENSIVE COUNTRY CLASSIFICATIONS")
    print("=" * 55)

    # Comprehensive country classifications based on research and known information
    country_classifications = {
        # US Shows - Major Networks and Known Hosts
        "2020": "US",  # ABC News 20/20 program
        "the bill simmons": "US",  # ESPN/The Ringer, Boston sports personality
        "npr news now": "US",  # National Public Radio (US)
        "the toast": "US",  # Claudia and Jackie Oshry, New York-based
        "the dan le batard": "US",  # ESPN sports radio host
        "distractible": "US",  # Markiplier, Jacksepticeye, LordMinion777 - YouTube creators
        "the ezra klein": "US",  # New York Times podcast host
        "the joe budden": "US",  # Hip-hop personality, New Jersey
        "last on the left": "US",  # Marcus Parks, Ben Kissel, Henry Zebrowski
        "the deck": "US",  # Ashley Flowers (Crime Junkie network)
        "the bobby bones": "US",  # Country music radio host
        "sword and scale": "US",  # Mike Boudet, true crime podcast
        "matt and shanes secret": "US",  # Matt McCusker and Shane Gillis, Philadelphia comedians
        "behind the bastards": "US",  # Robert Evans, iHeartMedia
        "snapped women who murder": "US",  # Oxygen Network true crime
        "serial killers": "US",  # Parcast Network (now Spotify)
        "murder in america": "US",  # US-focused true crime
        "anatomy of murder": "US",  # Scott Weinberger and Anna-Sigga Nicolazzi
        "mrballens medical mysteries": "US",  # MrBallen (John Allen), former Navy SEAL
        "true crime": "US",  # Generic US true crime content
        "cold case files": "US",  # A&E Network
        "park predators": "US",  # Delia D'Ambra, US national parks crimes
        "creepcast": "US",  # Isaiah Markin and Hunter Hancock
        "joel osteen": "US",  # Texas megachurch pastor
        "morning wire": "US",  # Daily Wire (Ben Shapiro network)
        "wow in the world": "US",  # NPR Kids podcast
        "giggly squad": "US",  # Hannah Berner and Paige DeSorbo, New York
        "candace": "US",  # Candace Owens, conservative commentator
        "the vanished": "US",  # Marissa Jones, missing persons cases
        "crime conspiracy cults and murder": "US",  # US-based true crime
        "rotten mango video": "US",  # Stephanie Soo, YouTube creator
        "the basement yard": "US",  # Joe Santagato and Frankie Alvarez, New York
        "2 bears 1 cave": "US",  # Tom Segura and Bert Kreischer
        "elvis duran and the morning on demand": "US",  # Z100 New York radio
        "the matt walsh": "US",  # Daily Wire host
        "the tim dillon": "US",  # Comedian from New York
        "something was wrong": "US",  # Tiffany Reese
        "andrew schulzs flagrant": "US",  # Andrew Schulz, New York comedian
        "vince": "US",  # Vincent James, political commentator
        "just creepy scary stories": "US",  # Horror storytelling podcast
        "chainsfr on spotify": "US",  # Music and entertainment content
        "pbd": "US",  # Patrick Bet-David, Valuetainment
        "fantasy footballers fantasy football": "US",  # Fantasy football (NFL)
        "lex fridman": "US",  # MIT researcher, Texas-based
        "conspiracy theories": "US",  # Parcast Network
        "anything goes": "US",  # Emma Chamberlain
        "murder": "US",  # Generic true crime
        "dungeons and daddies": "US",  # Comedy D&D podcast
        "the rewatchables": "US",  # The Ringer network
        "not another dd": "US",  # Comedy podcast
        "your moms house": "US",  # Tom Segura and Christina Pazsitzky
        "what now": "US",  # Trevor Noah (Daily Show host)
        "the lol": "US",  # Comedy content
        "the ryen russillo": "US",  # ESPN/The Ringer sports
        "my brother my brother and me": "US",  # McElroy Brothers
        "the meateater": "US",  # Steve Rinella, hunting/outdoor
        "the steve harvey morning": "US",  # Steve Harvey radio show
        "so true": "US",  # Pop culture commentary
        "the broski report": "US",  # Brittany Broski
        "redacted declassified mysteries": "US",  # Military/government mysteries
        "and thats why we drink": "US",  # Christine Schiefer and Em Schulz
        "the big picture": "US",  # The Ringer movies podcast
        "the herd": "US",  # Colin Cowherd, Fox Sports
        "office ladies": "US",  # Jenna Fischer and Angela Kinsey (The Office)
        "critical role": "US",  # Voice actors D&D campaign
        "the viall files": "US",  # Nick Viall (The Bachelor)
        "allin with chamath jason sacks friedberg": "US",  # Tech investors podcast
        "the bald and the beautiful": "US",  # Trixie Mattel and Katya
        "watch what crappens": "US",  # Bravo TV recap podcast
        "killer psyche": "US",  # Candice DeLong, former FBI profiler
        "club random": "US",  # Bill Maher
        "the dan patrick": "US",  # Sports radio host
        "therapuss": "US",  # Jake Shane
        "betrayal weekly": "US",  # Relationship stories
        "are you garbage comedy": "US",  # Kevin Ryan and H. Foley
        "danny jones": "US",  # Comedy content creator
        "bedtime stories": "US",  # Dark storytelling
        "jesser": "US",  # YouTube creator/gamer
        "run fool": "US",  # True crime
        "stavvys world": "US",  # Stavros Halkias
        "the yard": "US",  # Ludwig and friends gaming podcast
        "american history tellers": "US",  # Wondery history podcast
        "strawberry letter": "US",  # Steve Harvey relationship advice
        "pod meets world": "US",  # Boy Meets World rewatch
        "2 pros and a cup of joe": "US",  # Fox Sports morning show
        "crime stories": "US",  # Nancy Grace true crime
        "morning brew daily": "US",  # Business news podcast
        "dark downeast": "US",  # Kylie Low, Maine true crime
        "scamfluencers": "US",  # Wondery scam podcast
        "two ts in a pod": "US",  # Tamra Judge and Teddi Mellencamp
        "serialously": "US",  # Annie Elise true crime
        "so supernatural": "US",  # Ashley Flowers paranormal
        "stuff they dont want you to know": "US",  # iHeartMedia conspiracy
        "mrballenõs medical mysteries": "US",  # MrBallen medical cases
        "the ben maller": "US",  # Fox Sports Radio
        "the best of coast to coast am": "US",  # Art Bell paranormal radio
        "club shay shay": "US",  # Shannon Sharpe interview show
        "dateline originals": "US",  # NBC Dateline
        "the way i heard it": "US",  # Mike Rowe storytelling
        "stuff you missed in history class": "US",  # iHeartMedia history
        "counterclock": "US",  # True crime investigations
        "the charlie kirk": "US",  # Turning Point USA
        "drink champs": "US",  # N.O.R.E. and DJ EFN hip-hop
        "post run high": "US",  # Running podcast
        "lore": "US",  # Aaron Mahnke folklore
        "true crime tonight": "US",  # Nightly true crime
        "dark history": "US",  # Bailey Sarian history
        "monster btk": "US",  # BTK serial killer case
        "the bulwark": "US",  # Never Trump conservatives
        "help i sexted my boss": "US",  # Comedy advice
        "legend": "US",  # Political commentary
        "ok storytime": "US",  # Ashley Gavin storytelling
        "dumb blonde": "US",  # Bunnie XO
        "timcast irl": "US",  # Tim Pool political commentary
        "crook county": "US",  # True crime
        "unashamed": "US",  # Robertson family (Duck Dynasty)
        "ridiculous history": "US",  # iHeartMedia history
        "the odd couple": "US",  # Fox Sports radio
        "american homicide": "US",  # Investigation Discovery
        "disgraceland": "US",  # Music history and crime
        "not gonna lie": "US",  # Kylie Kelce lifestyle
        "happy face": "US",  # Melissa Moore (Happy Face Killer daughter)
        "three": "US",  # Entertainment content
        "up and vanished": "US",  # Payne Lindsey true crime
        "how to money": "US",  # Personal finance
        "bookmarked by reeses book club": "US",  # Reese Witherspoon book club
        "murder on songbird road": "US",  # True crime case
        "bobbycast": "US",  # Bobby Bones interviews
        "nfl daily": "US",  # NFL podcast
        "all the smoke": "US",  # Matt Barnes and Stephen Jackson NBA
        "the greatest true crime stories ever told": "US",  # True crime anthology
        "bible in a year": "US",  # Fr. Mike Schmitz Catholic podcast
        "therapy gecko": "US",  # Lyle Forever advice show
        "real time": "US",  # Entertainment discussion
        "dateline missing in america": "US",  # NBC Dateline missing persons
        "conan oõbrien needs a friend": "US",  # Conan O'Brien
        "what happened to talina zar": "US",  # Missing person case
        "our american stories": "US",  # Lee Habeeb American storytelling
        "math magic stories from the frontiers of marketing": "US",  # Marketing education
        "fox sports radio": "US",  # Fox Sports network
        "the idaho massacre": "US",  # Idaho student murders case
        "boysober": "US",  # Madeline Argy dating advice
        "building abundant success": "US",  # Business success
        "murder true crime stories": "US",  # True crime stories
        "fly on the wall": "US",  # David Spade and Dana Carvey
        "variety confidential": "US",  # Entertainment industry
        "the victor davis hanson": "US",  # Hoover Institution scholar
        "the happiness lab": "US",  # Dr. Laurie Santos Yale psychology
        "cold case files miami": "US",  # Miami-Dade cold cases
        "sex": "US",  # Sex education podcast
        "ruthies table 4": "US",  # Ruth Reichl food
        "the telepathy tapes": "US",  # Paranormal investigation
        "law order criminal justice systemê season 1 season 2": "US",  # Law & Order related
        "start here": "US",  # ABC News morning briefing
        "the season": "US",  # Sports content
        "health discovered": "US",  # Health and wellness
        "the girlfriends jailhouse lawyer season 3": "US",  # Legal true crime
        "wisecrack": "US",  # Philosophy and pop culture
        "i do part 2": "US",  # Wedding content
        "run that prank": "US",  # Prank comedy
        "amy robach tj holmes present": "US",  # Former GMA hosts
        "murder on the towpath": "US",  # True crime case
        "dear chelsea": "US",  # Chelsea Handler
        "black wealth renaissance": "US",  # Business and wealth
        "the official yellowstone": "US",  # Yellowstone TV show
        "it could happen here": "US",  # Robert Evans political crisis
        "my friend daisy": "US",  # Comedy friendship
        "hoax": "US",  # Investigation of hoaxes
        "devil in the desert": "US",  # True crime investigation
        "klove news": "US",  # Christian radio network
        "40s and free agents": "US",  # Dating advice
        "the stephen a smith": "US",  # ESPN personality
        "espn sportscenter update": "US",  # ESPN sports updates
        "the nikki glaser": "US",  # Comedian
        "intentionally disturbing": "US",  # Dark content
        "pop culture happy hour": "US",  # NPR pop culture

        # German Shows
        "mordlust": "DE",  # German true crime
        "verbrechen von nebenan true crime aus der nachbarschaft": "DE",  # German true crime
        "die drei rabauken": "DE",  # German comedy
        "wissen mit johnny": "DE",  # German education
        "muttersöhnchen": "DE",  # German leisure content
        "verbrechen": "DE",  # German true crime
        "aktenzeichen xy unvergessene verbrechen": "DE",  # German true crime TV
        "kurt krömer feelings": "DE",  # German comedy
        "hobbylos": "DE",  # German comedy podcast
        "edeltalk mit dominik kevin": "DE",  # German comedy
        "mord auf ex": "DE",  # German true crime
        "kottbruder germanletsplay paluten": "DE",  # German gaming
        "baywatch berlin": "DE",  # German comedy
        "gemischtes hack": "DE",  # German comedy
        "apokalypse filterkaffee": "DE",  # German political commentary
        "lanz precht": "DE",  # German political discussion

        # Japanese Shows
        "歴史を面白く学ぶコテンラジオ coten radio": "JP",  # Japanese history education
        "英語で雑談kevins english room plus": "JP",  # Japanese English education
        "英語聞き流し sakura english": "JP",  # Japanese English education
        "ダイアンのtokyo style": "JP",  # Japanese comedy
        "大久保佳代子とらぶぶらlove": "JP",  # Japanese comedy
        "マユリカのうなげろりん": "JP",  # Japanese comedy
        "ながら日経": "JP",  # Japanese news/business
        "最新回のみ辛坊治郎 ズーム そこまで言うか": "JP",  # Japanese political commentary
        "空気階段の踊り場": "JP",  # Japanese comedy

        # UK/GB Shows
        "the rest is history": "GB",  # Tom Holland and Dominic Sandbrook, British historians
        "casefile true crime": "AU",  # Actually Australian, Casey (anonymous host)
        "the rest is politics": "GB",  # Alastair Campbell and Rory Stewart, British politics

        # Italian Shows
        "la zanzara": "IT",  # Italian radio show
        "lo zoo di 105": "IT",  # Italian radio comedy

        # Spanish/Mexican Shows
        "nadie sabe nada": "ES",  # Spanish comedy
        "panda picante": "ES",  # Spanish comedy
        "leyendas legendarias": "MX",  # Mexican comedy/paranormal

        # Portuguese/Brazilian Shows
        "não inviabilize": "BR",  # Brazilian content

        # Australian Shows
        "parenting hell": "GB",  # Rob Beckett and Josh Widdicombe, British comedians
        "shged married annoyed": "GB",  # Chris and Rosie Ramsey, British comedy

        # Canadian Shows - None clearly identified in this list

        # International/Unknown (keep as Unknown for now)
        "wsj whats news": "US",  # Wall Street Journal
        "the stories of mahabharata": "IN",  # Indian epic stories
        "i didnõt know maybe you didnõt either": "Unknown",  # Unclear origin
        "travel": "Unknown",  # Too generic
    }

    print(f"✓ Created classifications for {len(country_classifications)} shows")

    # Show breakdown by country
    country_counts = {}
    for country in country_classifications.values():
        country_counts[country] = country_counts.get(country, 0) + 1

    print(f"\nCountry distribution in new classifications:")
    for country, count in sorted(country_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {country}: {count} shows")

    return country_classifications

def update_comprehensive_country_mapping():
    """Update the country mapping with comprehensive classifications."""

    print(f"\nUPDATING COMPREHENSIVE COUNTRY MAPPING")
    print("=" * 45)

    # Load existing mapping
    try:
        existing_mapping = pd.read_csv("final_country_mapping.csv")
        existing_dict = dict(zip(existing_mapping["normalized_name"], existing_mapping["country"]))
        print(f"Loaded existing mapping: {len(existing_dict)} shows")
    except FileNotFoundError:
        existing_dict = {}
        print("Creating new country mapping")

    # Get comprehensive classifications
    new_classifications = create_comprehensive_country_classifications()

    # Update mapping
    updated_count = 0
    for show, country in new_classifications.items():
        if country != "Unknown":
            if show not in existing_dict or existing_dict[show] == "Unknown":
                existing_dict[show] = country
                updated_count += 1

    # Create updated mapping dataframe
    mapping_data = []
    for show, country in existing_dict.items():
        source = "Comprehensive research" if show in new_classifications else "Previous mapping"
        mapping_data.append({
            "normalized_name": show,
            "country": country,
            "source": source
        })

    updated_mapping_df = pd.DataFrame(mapping_data)
    updated_mapping_df.to_csv("comprehensive_country_mapping_complete.csv", index=False)

    print(f"✓ Updated comprehensive mapping: {len(updated_mapping_df)} shows")
    print(f"✓ New countries classified: {updated_count}")

    # Show final country distribution
    country_dist = updated_mapping_df["country"].value_counts()
    print(f"\nFinal country distribution:")
    for country, count in country_dist.head(15).items():
        print(f"  {country}: {count} shows")

    return updated_mapping_df

def update_ranking_system_for_comprehensive_countries():
    """Update the ranking system to use comprehensive country mapping."""

    print(f"\nUPDATING RANKING SYSTEM FOR COMPREHENSIVE COUNTRIES")
    print("=" * 55)

    # Read current ranking system
    with open("complete_5platform_ranking_system.py", "r") as f:
        content = f.read()

    # Update to use comprehensive mapping
    updated_content = content.replace(
        'country_mapping = pd.read_csv("final_country_mapping.csv")',
        'country_mapping = pd.read_csv("comprehensive_country_mapping_complete.csv")'
    )

    # Also add fallback logic
    fallback_logic = '''    try:
        country_mapping = pd.read_csv("comprehensive_country_mapping_complete.csv")
        country_map = dict(zip(country_mapping["normalized_name"], country_mapping["country"]))
        print(f"   ✓ Loaded comprehensive country mapping: {len(country_map)} shows")
    except FileNotFoundError:
        try:
            country_mapping = pd.read_csv("final_country_mapping.csv")
            country_map = dict(zip(country_mapping["normalized_name"], country_mapping["country"]))
            print(f"   ✓ Loaded final country mapping: {len(country_map)} shows")
        except FileNotFoundError:'''

    updated_content = updated_content.replace(
        '''    try:
        country_mapping = pd.read_csv("final_country_mapping.csv")
        country_map = dict(zip(country_mapping["normalized_name"], country_mapping["country"]))
        print(f"   ✓ Loaded final country mapping: {len(country_map)} shows")
    except FileNotFoundError:
        try:
            country_mapping = pd.read_csv("comprehensive_country_mapping_updated.csv")
            country_map = dict(zip(country_mapping["normalized_name"], country_mapping["country"]))
            print(f"   ✓ Loaded comprehensive country mapping: {len(country_map)} shows")
        except FileNotFoundError:''',
        fallback_logic
    )

    # Write updated system
    with open("complete_5platform_ranking_system.py", "w") as f:
        f.write(updated_content)

    print("✓ Updated ranking system to use comprehensive country mapping")
    return True

if __name__ == "__main__":
    # Create comprehensive country mapping
    comprehensive_mapping = update_comprehensive_country_mapping()

    # Update ranking system
    update_ranking_system_for_comprehensive_countries()

    print(f"\n🎯 COMPREHENSIVE COUNTRY CLASSIFICATION COMPLETE!")
    print(f"   📋 Comprehensive mapping: comprehensive_country_mapping_complete.csv")
    print(f"   🔧 Updated ranking system to use comprehensive mapping")
    print(f"   🌍 {len(comprehensive_mapping)} shows with country classifications")
    print(f"   🚀 Ready to regenerate final rankings with comprehensive countries!")