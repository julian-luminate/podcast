# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a podcast analytics and research experiment within Luminate's data science organization. The project focuses on cross-platform podcast performance analysis using data from Spotify, YouTube, Amazon, Apple Podcasts, and iHeart Radio for competitive intelligence and market research.

## Architecture

### Data Structure
```
data/                              # Primary datasets
├── spotify.csv                    # US creators, 36 shows, YTD 2025 plays (CONFIDENTIAL)
├── youtube.csv                    # Global playlists, 101 shows, watch time metrics
├── amazon.csv                     # Audible/Amazon Music, ~32 shows (padded to 741k rows)
├── apple.csv                      # Apple Podcasts, 30 shows, plays >30s
└── iheart_platform_nominations.csv # Platform-specific listening data

alt_data/                          # Supplementary datasets
├── iheartpodcast_nominations.csv  # Publisher cross-platform aggregates
└── us_audiance.csv                # US monthly audience by platform (reference)

# Generated mapping files
├── union_genre_mapping.csv        # 147 shows with unified genre classifications
├── comprehensive_country_mapping.csv # 167 shows with country origins
└── podcast_cross_platform_rankings.csv # Final rankings output
```

### Key Data Characteristics
- **Spotify**: US-focused, 6+ episodes YTD, 30min+ duration, plays through 9/22/2025
- **YouTube**: Global scope, playlist-level metrics, filtered to US shows for analysis
- **Amazon**: Massive dataset with significant padding - only ~32 actual shows in 741k+ rows
- **Apple**: Top 30 US podcasts by plays (>30 seconds), 2025 data
- **iHeart**: Both platform-specific and cross-platform publisher data

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

### Cross-Platform Analysis
The dataset enables comparison of:
- Spotify Plays vs YouTube Views vs Amazon Plays vs Apple Plays vs iHeart Streams
- Geographic distribution (YouTube's multi-country vs US-focused platforms)
- Completion rates and engagement metrics across platforms
- Show performance for Golden Globes or similar award contexts
- Cross-platform show matching with improved normalization

### Show Name Matching
The system uses enhanced normalization to match shows across platforms:
- Removes common suffixes: "Podcast", "Show", "The Podcast", "The Show"
- Removes host qualifiers: "with [host name]", "w/ [host name]"
- Standardizes punctuation and spacing
- Results in 14 additional cross-platform matches compared to basic normalization
- 28 total shows successfully matched across 2+ platforms
- 15 shows matched across 3+ platforms

### Genre and Country Classification
- **Genre Mapping**: 147 shows classified into standard genres (News & Politics, True Crime, Comedy, Sports, Education, Entertainment, Interview & Talk, Business)
- **Country Mapping**: 167 shows with country of origin identified
- **Research Sources**: Tavily web search and Wikipedia used to research show metadata
- **Mapping Files**: `union_genre_mapping.csv` and `comprehensive_country_mapping.csv`

### Development Stack
**Dependencies:**
- pandas (2.3.2+)
- numpy (2.0.0+)

**Key Scripts:**
- `podcast_ranking_system.py` - Main ranking algorithm (5 platforms)
- `improve_show_matching.py` - Show name normalization analysis
- Various genre/country research scripts (Tavily/Wikipedia integration)

**Reproducibility:**
```bash
# Install dependencies
pip3 install pandas numpy

# Run complete analysis
python3 podcast_ranking_system.py

# Output: podcast_cross_platform_rankings.csv (108 shows ranked)
```