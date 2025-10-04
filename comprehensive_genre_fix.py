#!/usr/bin/env python3
"""
Comprehensive fix for all remaining 'Other' genre shows based on Tavily research
"""

import pandas as pd

def create_comprehensive_other_genre_fixes():
    """Create comprehensive genre fixes for all remaining 'Other' shows based on research."""

    print("CREATING COMPREHENSIVE 'OTHER' GENRE FIXES")
    print("=" * 55)

    # Comprehensive genre updates for all remaining 'Other' shows
    comprehensive_genre_fixes = {
        # Business & Entrepreneurship
        "the diary of a ceo": "Business",
        "ceo dan cinderella": "Business",
        "figuring out": "Business",  # Raj Shamani business/entrepreneurship podcast

        # News & Politics
        "rita panahi": "News & Politics",
        "brian tyler cohen": "News & Politics",
        "the luke beasley": "News & Politics",
        "권순표의 뉴스 하이킥 2025": "News & Politics",
        "political analysis": "News & Politics",
        "hoy en negocios televisión": "News & Politics",
        "banglavision world news banglavision": "News & Politics",
        "ihip news": "News & Politics",
        "the devory darkins": "News & Politics",
        "teenmaar varthalu by v6": "News & Politics",
        "politik wirtschaft": "News & Politics",  # German politics and economics
        "farron balanced": "News & Politics",  # Farron Cousins progressive political commentary
        "подкасти 24 каналу": "News & Politics",  # Ukrainian news podcasts
        "подкасти на 24 каналі": "News & Politics",  # Ukrainian news podcasts
        "подкасты мировая политика сша китай россия украина": "News & Politics",

        # True Crime & Legal
        "lawcrime sidebar": "True Crime",

        # Education & Science
        "the why files operation": "Education",

        # Entertainment & Media
        "víctor y alba en vivo": "Entertainment",
        "close the door": "Entertainment",  # Deddy Corbuzier Indonesian entertainment
        "podhub": "Entertainment",  # Indonesian podcast platform content
        "dr insanity podcasts": "Entertainment",
        "curhat bang denny sumargo": "Entertainment",
        "las alucines": "Comedy",  # Mexican comedy content
        "full surahs": "Society & Culture",  # Islamic religious content
        "a closer look late night": "Comedy",  # Late night comedy
        "유선배 복지 콘텐츠 핑계고": "Society & Culture",  # Korean social content
        "언알바": "Society & Culture",  # Korean social commentary
        "malam mencekam": "Entertainment",  # Indonesian horror/scary stories
        "dan wootton outspoken": "News & Politics",  # British political commentary
        "sport shorts": "Sports",  # Australian sports content
        "bulwark takes": "News & Politics",  # Political commentary
        "legal af": "News & Politics",  # Legal political commentary
        "کلیپ کوتاه استند آپ کمدیهای مکس امینی": "Comedy",  # Stand-up comedy clips
        "the adam mockler": "News & Politics",  # Political commentary
        "nbc nightly news": "News & Politics",
        "свежие интервью": "Interview & Talk",  # Turkish interviews
        "the ramsey highlights": "Business",  # Dave Ramsey financial content
        "hablando huevadas": "Comedy",  # Peruvian comedy podcast
        "микола давидюк": "News & Politics",  # Ukrainian political content
        "timcast news stories": "News & Politics",  # Tim Pool news commentary
        "rof daily updates": "News & Politics",
        "caso cerrado pleitos familiares con escándalo": "Entertainment",  # Spanish family drama show
        "강펀치 매주 월 금_오전 10시 20분": "News & Politics",  # Korean news program
        "monólogos": "Comedy",  # Mexican comedy monologues
        "beto ribeiro crime comportamento e mistério": "True Crime",  # Brazilian true crime
        "the philip defranco every montueswedthursfriday": "News & Politics",
        "전수미의 뉴스인사이다 이승원의 뉴인사 프라임 am650": "News & Politics",  # Korean news program
        "王局拍案": "News & Politics",  # Chinese political commentary
        "jabab chay bangla জবব চয় বল": "News & Politics",  # Bangladeshi political content
        "비트王新聞": "News & Politics",  # Chinese news content
        "sky news all stars": "News & Politics",  # Australian news commentary
        "chunk": "News & Politics",  # Political news content
        "1 on trending for finance": "Business",  # Financial content
        "nadie dice nada": "Comedy",  # Argentinian comedy podcast
        "penitencia con saskia niño de rivera": "Interview & Talk",  # Mexican interview show
        "the intersection": "News & Politics",
        "global news geopolitical developments": "News & Politics",
        "big bulletin": "News & Politics",  # Indian news content
        "la cotorrisa anecdotarios": "Comedy",  # Mexican comedy podcast
        "intens investigasi": "News & Politics",  # Indonesian investigative journalism
        "india explained": "News & Politics",  # Indian news and politics explanation
        "memoria del balón": "Sports",  # Colombian sports content about football
        "direito estatal": "Education",  # Legal education content
        "과학을 보다": "Education",  # Korean science education
        "bulwark super feed": "News & Politics",
        "the wild project 1vs1 cada jueves": "Interview & Talk",  # Spanish interview show
        "уроки истории": "Education",  # Russian history education
        "jack cocchiarella": "Comedy",  # Comedy content
        "bhoot dot com": "Entertainment",  # Bangladeshi horror/ghost stories
        "rolandmartinunfiltered": "News & Politics",  # Roland Martin political commentary
        "cumicam indepth": "News & Politics",  # Indonesian news analysis
        "all videos": "Entertainment",  # General entertainment content
        "백운기의 정치1번지": "News & Politics",  # Korean political program
        "문昭談古論今": "News & Politics",  # Chinese political commentary
        "la cotorrisa episodios": "Comedy",  # Mexican comedy episodes
        "the wronged hour": "News & Politics",  # Indian social justice content
        "acharya shri kaushik ji maharaj कथ वचक": "Society & Culture",  # Indian religious/cultural content
        "韓國留學生tv": "Society & Culture",  # Korean student life content
        "the young turks": "News & Politics",  # Progressive political commentary
        "문昭思緒飛揚podcast": "News & Politics",  # Chinese political commentary
        "聽重點新聞三立新聞台": "News & Politics",  # Taiwanese news program
        "la cotorrisa": "Comedy",  # Mexican comedy podcast base show
        "the bill simmons": "Sports",  # The Ringer sports commentary
    }

    print(f"✓ Genre fixes prepared for {len(comprehensive_genre_fixes)} shows")
    return comprehensive_genre_fixes

def update_final_genre_mapping_directly():
    """Update the final genre mapping file directly with comprehensive fixes."""

    print("\nUPDATING FINAL GENRE MAPPING WITH COMPREHENSIVE FIXES")
    print("=" * 60)

    # Get comprehensive fixes
    genre_fixes = create_comprehensive_other_genre_fixes()

    # Load existing genre mapping
    try:
        genre_df = pd.read_csv("final_genre_mapping_updated.csv")
        print(f"Loaded existing genre mapping: {len(genre_df)} shows")
    except FileNotFoundError:
        try:
            genre_df = pd.read_csv("final_genre_mapping.csv")
            print(f"Loaded fallback genre mapping: {len(genre_df)} shows")
        except FileNotFoundError:
            genre_df = pd.DataFrame(columns=["normalized_name", "genre", "source"])
            print("Created new genre mapping")

    # Create comprehensive updated data
    updated_genre_data = []
    existing_shows = set(genre_df["normalized_name"]) if not genre_df.empty else set()

    # Add existing data with updates
    for _, row in genre_df.iterrows():
        show_name = row["normalized_name"]
        if show_name in genre_fixes:
            new_genre = genre_fixes[show_name]
            updated_genre_data.append({
                "normalized_name": show_name,
                "genre": new_genre,
                "source": f"Tavily research comprehensive update: {new_genre} content"
            })
            print(f"  ✓ Updated: {show_name} -> {new_genre}")
        else:
            updated_genre_data.append({
                "normalized_name": show_name,
                "genre": row["genre"],
                "source": row["source"]
            })

    # Add any new shows not in existing mapping
    for show, genre in genre_fixes.items():
        if show not in existing_shows:
            updated_genre_data.append({
                "normalized_name": show,
                "genre": genre,
                "source": f"Tavily research: {genre} content classification"
            })
            print(f"  + Added: {show} -> {genre}")

    # Create final DataFrame
    updated_genre_df = pd.DataFrame(updated_genre_data)
    updated_genre_df = updated_genre_df.drop_duplicates(subset=["normalized_name"], keep="first")

    # Save comprehensive mapping
    updated_genre_df.to_csv("final_genre_mapping_comprehensive.csv", index=False)

    print(f"✓ Comprehensive genre mapping: {len(updated_genre_df)} shows")

    # Show final distribution
    genre_dist = updated_genre_df["genre"].value_counts()
    print(f"\nFinal comprehensive genre distribution:")
    for genre, count in genre_dist.head(15).items():
        print(f"  {genre}: {count} shows")

    return updated_genre_df

if __name__ == "__main__":
    # Create comprehensive genre mapping
    comprehensive_mapping = update_final_genre_mapping_directly()

    print(f"\n🎯 COMPREHENSIVE GENRE CLASSIFICATION COMPLETE!")
    print(f"   Updated mapping: final_genre_mapping_comprehensive.csv")
    print(f"   Ready to apply to complete ranking system!")