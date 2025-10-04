# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a comprehensive podcast analytics and research experiment within Luminate's data science organization. The project focuses on advanced cross-platform podcast performance analysis using data from **5 major platforms**: Spotify, YouTube, Amazon, Apple Podcasts, and iHeart Radio for competitive intelligence, market research, and competitive analysis.

**Status:** ✅ **COMPLETE** - Full 5-platform ranking system with US-normalized consumption data and comprehensive classification (369 shows ranked).

## Architecture

### Data Structure
```
data/                              # Primary datasets (ALL 5 PLATFORMS)
├── spotify.csv                    # US creators, 100 shows, YTD 2025 plays (CONFIDENTIAL)
├── youtube.csv                    # Global playlists, 100 shows, views + country data
├── amazon.csv                     # Audible/Amazon Music, 100 shows (cleaned from padding)
├── apple.csv                      # Apple Podcasts, 30 shows, plays >30s
└── iheart_platform_nominations.csv # iHeart Radio, 150 shows, streaming data

# Generated mapping files (COMPREHENSIVE - ALL COMPLETE)
├── comprehensive_country_mapping_complete.csv # 348 shows with country classifications
├── final_genre_mapping_complete_all.csv # 373 shows with genre classifications
└── final_5platform_podcast_rankings.csv # ✅ FINAL RANKINGS (369 shows)

# Complete analysis system files
├── complete_5platform_ranking_system.py # ✅ Main 5-platform ranking system (FIXED DUPLICATES)
├── comprehensive_country_classification.py # ✅ Manual comprehensive country research
├── research_unknown_countries.py # ✅ Automated Tavily/Wikipedia research
└── public_chart_comparison_analysis.md # ✅ Validation against Edison Research/Apple Charts
```

### Key Data Characteristics
- **Spotify**: US-focused, 100 shows, YTD 2025 plays (CONFIDENTIAL)
- **YouTube**: Global scope, 100 shows, US-normalized at 7.5% (15% with additional 50% discount)
- **Amazon**: Global scope, 100 shows, US-normalized at 65% (cleaned from extensive padding)
- **Apple**: Top 30 US podcasts, plays >30s, 2025 data (100% US data)
- **iHeart**: US platform-specific listening data, 150 shows (100% US data)
- **Total Unique Shows**: 369 across all platforms (369 successfully ranked, duplicates fixed)

## Development Guidelines

### Data Analysis Approach
- Use pandas for CSV processing - all data is in CSV format
- Implement data cleaning for Amazon CSV (contains extensive padding/empty rows)
- Handle confidential Spotify data appropriately
- Consider geographic scope differences (US-only vs global) when comparing platforms
- Normalize metrics across different platform measurement systems

### Important Considerations
- **Confidentiality**: Spotify data marked as confidential - handle accordingly
- **Data Quality**: Amazon CSV requires significant cleaning due to row padding
- **Platform Differences**: Each platform uses different metrics and time periods
- **Temporal Scope**: Data primarily covers 2025 YTD through October

### Advanced 5-Platform Ranking System ✅ COMPLETE
The system implements a sophisticated **four-component weighted scoring algorithm** across **ALL 5 MAJOR PLATFORMS** with US-normalized consumption data:

**Scoring Components (Updated Weights):**
1. **Total Consumption Score (65%)** - US-normalized cross-platform audience metrics
2. **Platform Reach Score (20%)** - Best single platform performance relative to others
3. **Platform Count Score (5%)** - Multi-platform presence bonus (up to 5 platforms)
4. **Within-Genre Popularity Score (10%)** - Consumption-based genre ranking

**Geographic Normalization:**
- **YouTube**: 7.5% factor (15% base × 50% additional discount = US market estimate)
- **Amazon**: 65% factor (global → US estimate)
- **Spotify, Apple, iHeart**: 100% (already US-only data)

**Data Quality Fixes:**
- ✅ **Duplicate Resolution**: Fixed "Morbid" appearing twice (#8 and #10) by implementing proper groupby aggregation
- ✅ **Platform Deduplication**: All platforms now aggregate by normalized show name to handle duplicates
- ✅ **Cross-Platform Matching**: Enhanced show name normalization for accurate matching

**Analysis Capabilities:**
- **Complete cross-platform comparison**: Spotify Plays vs YouTube Views vs Amazon Plays vs Apple Plays vs iHeart Streams
- **Geographic distribution analysis** (22 countries represented)
- **Multi-platform show performance correlation** (up to 5 platforms per show)
- **Genre-specific performance benchmarking** (10 standardized genres)
- **Golden Globes/award eligibility filtering** by country
- **Advanced show name normalization** for accurate cross-platform matching

### Show Name Matching & Normalization
The system uses enhanced normalization for accurate cross-platform matching:
- Removes common suffixes: "Podcast", "Show", "The Podcast", "The Show"
- Removes host qualifiers: "with [host name]", "w/ [host name]"
- Standardizes punctuation and spacing using regex
- **Results**: 370 shows successfully ranked across 369 unique shows identified

### Genre and Country Classification ✅ COMPLETE
**Genre Classification:**
- **Standard Categories**: 10 refined genres (News & Politics, True Crime, Comedy, Sports, Education, Entertainment, Interview & Talk, Business, Society & Culture, Other)
- **Coverage**: 373 shows classified (94.1% completeness)
- **Sources**: Manual research > Platform metadata > Tavily AI research > Wikipedia research
- **Mapping File**: `final_genre_mapping_complete_all.csv`

**Country Classification:**
- **Global Coverage**: 348 shows with comprehensive country mapping (94.1% completeness)
- **Geographic Distribution**: 23 countries (US: 214 shows, DE: 19, JP: 9, GB: 8, others)
- **Research Methods**:
  - Manual comprehensive research (214 shows)
  - Platform metadata analysis
  - Tavily AI search integration
  - Wikipedia research fallback
- **Mapping File**: `comprehensive_country_mapping_complete.csv`

### Development Stack
**Dependencies:**
- pandas (2.3.2+)
- numpy (2.0.0+)
- Tavily API (for AI-powered research)
- Wikipedia API (for show metadata research)

**Key Scripts:**
- `complete_5platform_ranking_system.py` - ✅ **MAIN 5-PLATFORM SYSTEM** with advanced scoring
- `fix_missing_classifications.py` - ✅ Comprehensive classification updates
- `research_missing_data_tavily.py` - ✅ Tavily AI-powered research integration
- `updated_podcast_ranking_system.py` - ✅ Updated 4-platform system (legacy)

**Reproducibility:**
```bash
# Install dependencies
pip3 install pandas numpy

# Run complete 5-platform analysis
python3 complete_5platform_ranking_system.py

# Output: final_5platform_podcast_rankings.csv (370 shows ranked)
```

## Final Output ✅ COMPLETE

### `final_5platform_podcast_rankings.csv`
**Comprehensive CSV with 369 US-normalized podcasts across ALL 5 PLATFORMS**

**Top Rankings (US-Normalized):**
- **#1**: The Joe Rogan Experience (99.0 score, US, 666M consumption, 4 platforms)
- **#2**: The Daily (50.9 score, US, 174M consumption, 4 platforms)
- **#3**: 48 Hours (47.9 score, US, 136M consumption, 5 platforms)
- **#4**: Crime Junkie (44.1 score, US, 177M consumption, 4 platforms)
- **#6**: Morbid (40.8 score, US, 125M consumption, 4 platforms) ✅ DUPLICATE FIXED

**Global Representation:** 23 countries (US: 214 shows, DE: 19, JP: 9, GB: 8, others)
**Multi-Platform Coverage:** 2 shows on all 5 platforms, 15 shows on 4+ platforms, 62 multi-platform shows total
**Classification Completeness:** 94.1% (22 Unknown countries, 2 Other genres remaining)

**CSV Columns:**
```
rank, show_name, composite_score, genre, country,
consumption_score, platform_reach_score, platform_count_score, genre_rank_score,
total_consumption, platforms_present,
spotify_plays, youtube_views, youtube_views_us, amazon_plays, amazon_plays_us, apple_plays, iheart_streams
```

**Validation ✅ COMPLETE:**
- **Public Chart Comparison**: `public_chart_comparison_analysis.md`
- **Edison Research Correlation**: 0.73 Spearman coefficient (strong positive correlation)
- **Cross-Platform Validation**: Joe Rogan #1 across all methodologies

**Use Cases:**
- 📊 **Cross-platform competitive intelligence** (all 5 major platforms with US normalization)
- 🌍 **Global podcast market research** (23 countries, 369 shows, 94.1% classified)
- 📈 **Multi-platform performance benchmarking** (geographic adjustment factors applied)
- 🎯 **Platform-specific strategy development** (individual platform vs aggregated performance)
- ✅ **Data quality assurance** (duplicates resolved, normalization applied)

**Status**: **Production-ready ranking system with validated methodology and comprehensive coverage!** 🚀