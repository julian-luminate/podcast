# Data Documentation

## Overview

This document describes all data files, their structures, and how they are used in the cross-platform podcast ranking system.

## Primary Data Files

### data/spotify.csv
**Source:** Spotify US creators data
**Records:** 36 shows
**Time Period:** YTD 2025 through 9/22/2025
**Confidentiality:** CONFIDENTIAL

**Structure:**
```
Header: 7 rows to skip
Columns:
  - show_name: String
  - spotify_plays: String (with commas, e.g., "536,243,172")
  - category: String (genre information)

Processing:
  - Skip first 7 rows
  - Remove commas from plays column
  - Convert plays to float
  - Drop rows with missing data
```

**Characteristics:**
- US-focused content creators
- Shows with 6+ episodes YTD
- Episodes 30+ minutes duration
- Play counts through 9/22/2025

---

### data/youtube.csv
**Source:** YouTube playlist data
**Records:** 101 playlists (filtered to US shows)
**Time Period:** 2025 YTD
**Geography:** Global (filtered to US in processing)

**Structure:**
```
Columns:
  - playlist_name: String (renamed to show_name)
  - watchtime_hrs: Float
  - views: Float (primary metric used)
  - num_2025_videos: Integer
  - FeatureCountry: String (US filter applied)

Processing:
  - Rename playlist_name to show_name
  - Filter to US shows: (FeatureCountry == "US") | isna()
  - Use views as primary engagement metric
```

**Characteristics:**
- Video podcast content
- Multi-country coverage (filtered to US)
- Views metric represents video engagement

---

### data/amazon.csv
**Source:** Audible/Amazon Music
**Records:** ~32 actual shows (741k+ rows with padding)
**Time Period:** January-October 2025
**Geography:** US market

**Structure:**
```
Header: 2 rows to skip
Columns:
  - Show Title: String (renamed to show_name)
  - Total Plays: Float
  - Customers: Float
  - Average Completion Rate: Float

Processing:
  - Skip first 2 rows
  - Drop rows with missing Show Title (removes padding)
  - Rename Show Title to show_name
```

**Characteristics:**
- Massive dataset with significant padding (~741k rows for ~32 shows)
- Requires aggressive cleaning via dropna()
- Jan-Oct 2025 timeframe

---

### data/apple.csv
**Source:** Apple Podcasts
**Records:** 30 shows
**Time Period:** 2025 YTD
**Geography:** US market

**Structure:**
```
Columns:
  - Rank: Integer
  - Podcast: String (renamed to show_name)
  - Plays (>30s): Float (qualified plays)
  - URL: String (Apple Podcasts URL)

Processing:
  - Rename Podcast to show_name
  - Rename Plays (>30s) to apple_plays
  - Drop rows with missing show_name
```

**Characteristics:**
- Top 30 US podcasts
- Plays counted only if >30 seconds (qualified engagement)
- New addition to dataset (5th platform)

---

### data/iheart_platform_nominations.csv
**Source:** iHeart Radio platform
**Records:** 27 shows
**Time Period:** YTD 2025
**Geography:** US market

**Structure:**
```
Header: 2 rows to skip
Columns:
  - rank: Integer
  - show_name: String
  - iheart_listeners: String (with commas)
  - iheart_streams: String (with commas, primary metric)
  - iheart_completion: String (percentage with %)
  - iheart_followers: String (with commas)

Processing:
  - Skip first 2 rows
  - Remove commas and spaces from numeric columns
  - Convert streams, listeners, followers to float
  - Remove % symbol from completion, divide by 100
  - Drop rows with missing show_name
```

**Characteristics:**
- Platform-specific streaming data
- Includes completion rates and follower counts
- Streams used as primary engagement metric

---

## Supplementary Data Files

### alt_data/iheartpodcast_nominations.csv
**Source:** iHeart publisher cross-platform aggregates
**Records:** 25 shows
**Geography:** Cross-platform data

**Structure:**
```
Header: 2 rows to skip
Columns:
  - # of Shows: Float
  - TITLE: String
  - HOST(S): String
  - AVERAGE MONTLY DOWNLOADS: Float
  - TOTAL UNIQUE LISTENERS: Float
  - TOTAL LIFETIME DOWNLOADS: Float
  - SUBSCRIBER/FOLLOWER COUNT: Float

Processing:
  - Skip first 2 rows
  - Drop rows with missing TITLE
```

**Usage:** Reference data only, not used in main ranking system
**Overlap:** 8 shows match with platform-specific iHeart data

---

### alt_data/us_audiance.csv
**Source:** Industry audience estimates
**Records:** 5 platforms
**Geography:** US market

**Structure:**
```
Columns:
  - Platform: String
  - Share of U.S. Monthly Podcast Listeners: String (percentage range)
  - Estimated U.S. Audience (Monthly Listeners): String (range in millions)

Data:
  - YouTube: 33-39% (52.1-61.6M listeners)
  - Apple: 34% (~53.7M listeners)
  - Spotify: 21-27% (33.2-42.7M listeners)
  - Amazon Music: 4% (~6.3M listeners)
  - iHeartRadio: 3% (~4.7M listeners)
```

**Usage:** Reference data only, not currently used in calculations
**Potential Use:** Could be used for platform weighting or market share analysis

---

## Generated Mapping Files

### union_genre_mapping.csv
**Purpose:** Unified genre classification for all shows
**Records:** 147 shows classified
**Generation:** Created via Tavily web search research

**Structure:**
```
Columns:
  - normalized_name: String (normalized show name for matching)
  - final_genre: String (standardized genre category)
  - platform_genre: String (original platform genre)
  - research_genre: String (internet research result)
  - tavily_genre: String (Tavily API research result)
  - source_summary: String (provenance of classification)

Standard Genres:
  - News & Politics
  - True Crime
  - Comedy
  - Sports
  - Education
  - Entertainment
  - Interview & Talk
  - Business
```

**Coverage:** 100% (0 shows with "Other" genre)

**Generation Process:**
1. Extract all unique show names across platforms
2. Apply normalization to create lookup keys
3. Research shows using Tavily API
4. Map to one of 8 standard genre categories
5. Store with source attribution

---

### comprehensive_country_mapping.csv
**Purpose:** Country of origin for all shows
**Records:** 167 shows mapped
**Generation:** Created via Tavily/Wikipedia research

**Structure:**
```
Columns:
  - normalized_name: String (normalized show name for matching)
  - country: String (ISO 2-letter country code)
  - source: String (research source and notes)

Country Distribution:
  - US: 93 shows (86%)
  - GB: 3 shows
  - DE: 8 shows (German language shows)
  - ES: 3 shows (Spanish language shows)
  - JP: 1 show (Japanese radio show)
```

**Coverage:** 100% (0 shows with "Unknown" country)

**Generation Process:**
1. Extract shows needing country identification
2. Research using Tavily API and Wikipedia
3. Identify based on: host nationality, production location, primary audience
4. Store with research notes

---

## Output Files

### podcast_cross_platform_rankings.csv
**Purpose:** Final unified rankings across all platforms
**Records:** 108 unique shows
**Generation:** Output of podcast_ranking_system.py

**Structure:**
```
Columns:
  - rank: Integer (1-108)
  - show_name: String (normalized name)
  - composite_score: Float (0-100+ scale)
  - genre: String (from union_genre_mapping)
  - country: String (from comprehensive_country_mapping)

  - consumption_score: Float (0-100, 50% weight)
  - platform_reach_score: Float (0-100, 20% weight)
  - platform_count_score: Float (0-100, 20% weight)
  - genre_rank_score: Float (0-100, 10% weight)

  - total_consumption: Float (sum of all platform metrics)
  - platforms_count: Integer (1-5)

  - spotify_score: Float (0-100 within Spotify)
  - youtube_score: Float (0-100 within YouTube)
  - amazon_score: Float (0-100 within Amazon)
  - apple_score: Float (0-100 within Apple)
  - iheart_score: Float (0-100 within iHeart)

  - spotify_plays: Float (raw metric)
  - youtube_views: Float (raw metric)
  - amazon_plays: Float (raw metric)
  - apple_plays: Float (raw metric)
  - iheart_streams: Float (raw metric)
```

**Statistics:**
- 108 unique shows total
- 5 shows on 4+ platforms
- 15 shows on 3+ platforms
- 28 shows on 2+ platforms
- 80 shows on 1 platform only

---

### show_name_matching_analysis.csv
**Purpose:** Analysis of show name normalization effectiveness
**Generation:** Output of improve_show_matching.py

**Structure:**
```
Columns:
  - new_normalized: String (normalized name with enhanced algorithm)
  - all_variants: String (pipe-separated list of original names)
  - platforms: String (comma-separated list of platforms)
  - old_normalized: String (normalized name with basic algorithm)
  - platform_count: Integer (number of platforms)

Usage:
  - Verify cross-platform matching
  - Identify shows that benefit from improved normalization
  - Review name variants for quality assurance
```

---

## Data Quality Notes

### Platform-Specific Issues

**Amazon:**
- Heavy row padding requires aggressive cleaning
- Only ~32 actual shows in 741k+ rows
- Must use dropna(subset=['Show Title']) to remove padding

**Spotify:**
- CONFIDENTIAL data - handle appropriately
- Play counts include commas requiring string processing
- 7-row header needs skipping

**YouTube:**
- Global data requires US filtering
- Country field has missing values (assumed US)
- Views used instead of watch time hours

**Apple:**
- Relatively clean data
- Top 30 shows only (limited coverage)
- Qualified plays (>30s) may differ from other platform metrics

**iHeart:**
- Numeric fields contain commas and spaces
- Completion rates include % symbol
- Both platform and publisher data available (use platform)

### Missing Data Handling

**Philosophy:** Missing platform data treated as 0 without penalty

**Implementation:**
- Shows not on a platform: 0 for that platform's metrics
- Platform reach calculated only from platforms where show appears
- Platform count accurately reflects actual presence
- No imputation or artificial inflation

### Time Period Discrepancies

- **Spotify:** Through 9/22/2025
- **YouTube:** YTD 2025
- **Amazon:** January-October 2025
- **Apple:** 2025 YTD
- **iHeart:** YTD 2025

**Impact:** Some variance due to different measurement windows, but all roughly comparable (YTD 2025)

---

## Data Processing Pipeline

### Step 1: Load and Clean
```python
def load_and_clean_data():
    # Load 5 platform CSV files with specific cleaning per platform
    # Return: spotify, youtube, amazon, apple, iheart dataframes
```

### Step 2: Normalize Show Names
```python
def normalize_show_names(df):
    # Apply enhanced normalization removing suffixes/prefixes
    # Return: dataframe with normalized show_name column
```

### Step 3: Calculate Platform Scores
```python
def calculate_platform_scores(spotify, youtube, amazon, apple, iheart):
    # For each platform: (show_metric / platform_max) × 100
    # Return: dataframes with platform_score columns added
```

### Step 4: Merge Cross-Platform
```python
def create_unified_ranking(spotify, youtube, amazon, apple, iheart):
    # 1. Get all unique normalized show names
    # 2. Create master dataframe with all shows
    # 3. Left join each platform data
    # 4. Load genre/country mappings
    # 5. Fill missing values with 0
    # 6. Calculate 4 component scores
    # 7. Calculate composite score
    # 8. Sort and rank
    # Return: complete rankings dataframe
```

### Step 5: Output Results
```python
def main():
    # Generate podcast_cross_platform_rankings.csv
    # Display console output with detailed metrics
```

---

## Reproducibility Requirements

### Required Files
```
data/spotify.csv
data/youtube.csv
data/amazon.csv
data/apple.csv
data/iheart_platform_nominations.csv
union_genre_mapping.csv
comprehensive_country_mapping.csv
```

### Dependencies
```
pandas==2.3.2
numpy==2.0.0
```

### Execution
```bash
pip3 install pandas numpy
python3 podcast_ranking_system.py
```

### Expected Output
```
podcast_cross_platform_rankings.csv
  - 108 rows (shows)
  - 21 columns (metrics and scores)
  - Console display of full rankings
```

---

## Data Lineage

```
Raw Platform Data
  ↓
Platform-Specific Cleaning
  ↓
Show Name Normalization (Enhanced)
  ↓
Genre/Country Enrichment (Tavily/Wikipedia)
  ↓
Within-Platform Score Calculation
  ↓
Cross-Platform Merging
  ↓
Four-Component Score Calculation
  ↓
Final Ranking
  ↓
Output CSV + Console Display
```

---

## Validation Checks

### Data Quality
- ✓ All 5 platforms loaded successfully
- ✓ 108 unique shows identified
- ✓ 28 shows matched across 2+ platforms
- ✓ 100% genre coverage (0 "Other")
- ✓ 100% country coverage (0 "Unknown")

### Calculation Integrity
- ✓ All scores normalized 0-100
- ✓ Component weights sum to 100% (50+20+20+10)
- ✓ Missing data handled consistently
- ✓ No negative values in output
- ✓ Rank order matches composite score order

### Cross-Platform Matching
- ✓ 14 additional matches vs basic normalization
- ✓ No duplicate shows after matching
- ✓ Enhanced algorithm applied consistently
- ✓ All platforms use same normalization logic
