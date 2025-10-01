# Cross-Platform Podcast Ranking Methodology

## Overview

This methodology creates a unified ranking system across five major podcast platforms: Spotify, YouTube, Amazon (Audible/Amazon Music), Apple Podcasts, and iHeart Radio. The system uses a four-component weighted scoring approach that balances total consumption, platform-specific performance, multi-platform presence, and within-genre popularity. Designed to identify the top podcasts for competitive intelligence and market research based on comprehensive audience reach and engagement metrics.

## Data Sources

- **Spotify**: US market, YTD 2025 plays (36 shows)
- **YouTube**: US market playlists, views (filtered from global dataset, 101 shows)
- **Amazon**: US market, Jan-Oct 2025 total plays (32 shows, padded to 741k rows)
- **Apple**: US market, plays >30s (30 shows)
- **iHeart**: US platform data, YTD streams (27 shows)

**Total Dataset:** 108 unique shows after cross-platform matching and deduplication

## Common Metrics Identified

**Primary engagement metric per platform:**
- Spotify: Total plays
- YouTube: Views (video engagement metric)
- Amazon: Total plays
- Apple: Plays >30s (qualified engagement)
- iHeart: Total streams

## Data Collection and Preparation

### 1. Data Loading and Cleaning
```python
# Platform-specific data loading
- Spotify: CSV with 7-row header skip, columns: [show_name, plays, category]
- YouTube: CSV with playlist_name → show_name, filtered to US shows only
- Amazon: CSV with 2-row header skip, heavy row padding (~741k rows for ~32 shows)
- Apple: CSV with columns: [Rank, Podcast, Plays (>30s), URL]
- iHeart: CSV with 2-row header skip, columns include listeners, streams, completion, followers
```

### 2. Show Name Normalization for Cross-Platform Matching

**Enhanced Normalization Algorithm:**
```python
def normalize_show_names(show_name):
    # Convert to lowercase
    normalized = show_name.strip().lower()

    # Remove common suffixes (order matters - longest first)
    suffixes = [
        r'\s+the\s+podcast$',
        r'\s+podcast$',
        r'\s+the\s+show$',
        r'\s+show$',
        r'\s+with\s+[host names]$',  # e.g., "with Dax Shepard"
        r'\s+w\s+[host]$',            # e.g., "w Theo Von"
        r'\s+w/\s+[host]$',           # e.g., "w/ Theo Von"
    ]

    for suffix in suffixes:
        normalized = re.sub(suffix, '', normalized)

    # Remove punctuation, normalize spaces
    normalized = re.sub(r'[^\w\s]', '', normalized)
    normalized = re.sub(r'\s+', ' ', normalized).strip()

    return normalized
```

**Matching Results:**
- 28 shows matched across 2+ platforms
- 15 shows matched across 3+ platforms
- 5 shows matched across 4+ platforms
- 14 additional matches compared to basic normalization

**Examples of Improved Matching:**
- "Armchair Expert with Dax Shepard" + "Armchair Expert" → `armchair expert`
- "This Past Weekend w/ Theo Von" → `this past weekend`
- "The Ben Shapiro Show" + "The Ben Shapiro Podcast" → `the ben shapiro`
- "My Favorite Murder with Karen Kilgariff and Georgia Hardstark" → `my favorite murder`

### 3. Genre Classification

**Standard Genre Categories:**
- News & Politics
- True Crime
- Comedy
- Sports
- Education
- Entertainment
- Interview & Talk
- Business

**Classification Process:**
1. Extract unique show names across all platforms
2. Use Tavily web search to research show genre and metadata
3. Map to standardized genre categories
4. Store in `union_genre_mapping.csv` (147 shows classified)

**Coverage:** 100% of shows classified (0 "Other" genres remaining)

### 4. Country of Origin Mapping

**Classification Process:**
1. Extract show names requiring country identification
2. Use Tavily/Wikipedia to research show origin
3. Identify host nationality, production location, primary audience
4. Store in `comprehensive_country_mapping.csv` (167 shows mapped)

**Coverage:** 100% of shows mapped (0 "Unknown" countries remaining)

**Country Distribution:**
- US: 93 shows (majority)
- GB: 3 shows
- DE: 8 shows
- ES: 3 shows
- JP: 1 show

### 5. Four-Component Weighted Scoring System
Rankings are calculated using a weighted sum of four key components that reflect different aspects of podcast success:

**Component Weights:**
- **Total Consumption (50%)**: Sum of all engagement metrics across platforms
- **Platform Reach (30%)**: Average performance within each platform where show appears
- **Platform Count (10%)**: Number of platforms where show has presence
- **Within-Genre Popularity (10%)**: Ranking within the show's specific genre category

**Detailed Calculation:**
```
# Component 1: Total Consumption Score (50% weight)
Total Consumption = Spotify Plays + YouTube Views + Amazon Plays + Apple Plays + iHeart Streams
Consumption Score = (Total Consumption / Maximum Total) × 100

# Component 2: Platform Reach Score (20% weight)
Platform Reach = Average of individual platform scores (0-100 each)
Individual Platform Score = (Show Metric / Platform Maximum) × 100

# Component 3: Platform Count Score (20% weight)
Platform Count Score = (Number of Platforms / Maximum Platforms) × 100
Maximum Platforms = 5 (Spotify, YouTube, Amazon, Apple, iHeart)

# Component 4: Within-Genre Popularity Score (10% weight)
Genre Rank = Show's consumption rank within its unified genre category
Genre Score = (Show Consumption / Max Genre Consumption) × 100

# Final Composite Score
Composite Score = (Consumption × 0.5) + (Platform Reach × 0.2) + (Platform Count × 0.2) + (Genre Popularity × 0.1)
```

**Rationale for This Approach:**
- **Total Reach Priority (50%)**: Maintains absolute audience impact as the dominant factor
- **Platform Excellence (20%)**: Rewards strong performance relative to platform maximums
- **Multi-Platform Strategy (20%)**: Significant credit for successful cross-platform distribution
- **Genre Context (10%)**: Rewards shows that dominate within their content category
- **Comprehensive Assessment**: Four dimensions provide holistic view of podcast success

## Fairness Considerations

### Component Balance
The 50/20/20/10 weight distribution ensures:
- Total consumption drives primary ranking differences (reflects real-world impact)
- Platform reach provides meaningful differentiation (rewards excellence within platforms)
- Multi-platform presence offers significant advantage (credits distribution strategy)
- Genre popularity rewards category leadership (recognizes niche dominance)

### Missing Data Handling
- Missing platform data treated as 0 for all calculations
- Shows not appearing on a platform receive no penalty in other components
- Platform reach score calculated only from platforms where show appears
- No artificial imputation that could inflate or deflate scores

### Geographic Consistency
- All platforms now focus on US market for fair comparison
- YouTube filtered to US-only shows (missing countries assumed US)
- Eliminates geographic bias in cross-platform analysis

### Four-Component Balance
- **Total Reach Priority**: Consumption score (50%) ensures absolute audience size remains the primary driver
- **Platform Excellence Recognition**: Reach score (20%) rewards shows that excel relative to their platforms
- **Multi-Platform Recognition**: Count score (20%) provides significant credit for cross-platform presence
- **Genre Context Assessment**: Genre popularity (10%) rewards category leadership and specialization
- **Prevents Single-Metric Gaming**: No component alone can determine final ranking
- **Comprehensive Evaluation**: Reflects total impact, platform mastery, distribution strategy, and genre dominance

### Show Name Matching Fairness
- **Enhanced Normalization**: Removes suffix variations that could split same show across platforms
- **Consistent Application**: Same normalization applied to all platforms equally
- **14 Additional Matches**: Improved algorithm found 14 shows that were previously split
- **No Manual Overrides**: All matching done algorithmically for reproducibility
- **Transparent Process**: Normalization logic fully documented and testable

## Ranking Output

The system generates comprehensive results including:
1. **Composite Score**: Primary ranking metric (0-100+ scale)
2. **Component Breakdown**: Individual scores for consumption, platform reach, platform count, and genre popularity
3. **Genre Classification**: Unified genre category for each show
4. **Total Consumption**: Sum of all engagement metrics across platforms
5. **Platform Count**: Number of platforms where show appears
6. **Individual Platform Scores**: Transparency into platform-specific performance (0-100 each)
7. **Within-Genre Ranking**: Show's position within its specific genre category
8. **Raw Metrics**: Original engagement numbers for validation and transparency

## Scoring Examples

**Four-Component Breakdown:**

**Example 1: Total Reach Leader**
- Joe Rogan Experience: 536M Spotify + 240M YouTube hours + 15M iHeart = Dominant consumption score (50%)
- Strong platform reach across multiple platforms = High reach score (30%)
- Multi-platform presence (3 platforms) = Good count score (10%)
- #1 in Interview & Talk genre = Maximum genre score (10%)
- Result: Likely overall #1 due to excellence across all four components

**Example 2: Genre Specialist**
- Top True Crime show: Moderate total consumption but dominates genre
- Excellent platform reach within True Crime category
- Single platform presence = Lower count score
- #1 within True Crime = Maximum genre popularity score
- Result: Strong overall score with genre specialization bonus

**Example 3: Multi-Platform Generalist**
- Good performance across 4 platforms = Maximum count score (100%)
- Average platform reach across all platforms
- Moderate total consumption from distributed presence
- Mid-tier within genre = Moderate genre score
- Result: Balanced score reflecting successful cross-platform distribution strategy

**Component Impact:**
- **Consumption (50%)**: Primary driver of ranking differences
- **Platform Reach (30%)**: Key differentiator for platform excellence
- **Platform Count (10%)**: Modest advantage for multi-platform shows
- **Genre Popularity (10%)**: Rewards category leadership and specialization

## Validation Approach

Rankings can be validated by:
- Comparing top performers against known industry leaders (Joe Rogan, Crime Junkie)
- Analyzing platform-specific vs. composite rankings for consistency
- Reviewing multi-platform shows for expected score premiums
- Cross-referencing with external podcast charts where available
- Ensuring total consumption leaders rank appropriately high
- Verifying multi-platform shows receive appropriate count component benefits

## Methodology Strengths

- **Balanced Approach**: Rewards both total reach and platform-relative achievement
- **Real-World Relevance**: Maintains importance of large audience platforms
- **Cross-Platform Fairness**: Prevents single-platform dominance through normalization
- **Transparency**: All components and calculations clearly documented
- **Scalability**: Can accommodate new platforms or updated audience data

## Limitations

- **Time Period Variations**: Different measurement windows across platforms (YTD vs Jan-Oct)
- **Content Type Differences**: YouTube video podcasts vs. audio-only on other platforms
- **Engagement Depth**: Raw metrics don't capture listen-through rates or engagement quality
- **Audience Overlap**: Same users may consume content across multiple platforms
- **Market Dynamics**: Audience estimates based on industry averages, not real-time data
- **Geographic Scope**: US-only focus may miss global podcast phenomena

## Technical Implementation

### Data Processing Pipeline
1. **Data Loading**: Five CSV files loaded with platform-specific cleaning
   - Spotify: 7-row header skip, string-to-float conversion for plays
   - YouTube: Rename columns, filter to US shows only
   - Amazon: 2-row header skip, dropna to remove padding rows
   - Apple: Standard CSV load, rename columns
   - iHeart: 2-row header skip, clean numeric columns with commas

2. **Show Name Normalization**: Enhanced algorithm for cross-platform matching
   - Remove common suffixes (podcast, show, with host, etc.)
   - Standardize punctuation and spacing
   - Applied consistently to all 5 platforms

3. **Genre/Country Enrichment**: Web research to classify shows
   - Use Tavily API to research show metadata
   - Map to standard genre categories (8 genres)
   - Identify country of origin
   - Store in mapping CSV files for reproducibility

4. **Platform Score Calculation**: Within-platform normalization
   - Each platform: (show_metric / platform_max) × 100
   - Creates 0-100 scale per platform

5. **Composite Score Calculation**: Four-component weighted system
   - Consumption: Sum all platform metrics, normalize to 100
   - Platform Reach: Average of platform scores where show appears
   - Platform Count: (num_platforms / 5) × 100
   - Genre Rank: Normalize within genre based on consumption

6. **Data Merging**: Cross-platform aggregation
   - Normalized names used as join key
   - Left join from all unique shows to each platform
   - Missing data filled with 0 (no penalty for missing platforms)

### Reproducibility Steps

**Complete Process:**
```bash
# 1. Install dependencies
pip3 install pandas numpy

# 2. Place data files in correct locations
data/
├── spotify.csv
├── youtube.csv
├── amazon.csv
├── apple.csv
└── iheart_platform_nominations.csv

# 3. Ensure genre/country mappings exist (or will be generated)
union_genre_mapping.csv
comprehensive_country_mapping.csv

# 4. Run main ranking system
python3 podcast_ranking_system.py

# 5. Output generated
podcast_cross_platform_rankings.csv  # 108 shows with all metrics
```

**Analysis Scripts Available:**
- `podcast_ranking_system.py` - Main ranking algorithm
- `improve_show_matching.py` - Analyze name normalization effectiveness
- Genre/country research scripts - Generate mapping files from web research

### Output Generation
Execute `python3 podcast_ranking_system.py` to generate:
- **CSV Export**: `podcast_cross_platform_rankings.csv` with 108 shows, all metrics
- **Console Display**: Full rankings with detailed component breakdowns
- **Transparency**: All raw metrics and component scores visible for validation

**Output Columns:**
- rank, show_name, composite_score, genre, country
- consumption_score, platform_reach_score, platform_count_score, genre_rank_score
- total_consumption, platforms_count
- spotify_score, youtube_score, amazon_score, apple_score, iheart_score
- spotify_plays, youtube_views, amazon_plays, apple_plays, iheart_streams

### Quality Assurance
- All calculations use consistent 0-100 normalization
- Component weights clearly defined and documented (50/20/20/10)
- Cross-platform matching handles 14 common name variations
- Missing data handled systematically without bias
- 100% genre coverage (0 "Other" categories)
- 100% country coverage (0 "Unknown" countries)
- All 5 platforms integrated with consistent methodology