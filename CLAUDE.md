# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a podcast analytics and research experiment within Luminate's data science organization. The project focuses on cross-platform podcast performance analysis using data from Spotify, YouTube, Amazon, and iHeart Radio for competitive intelligence and market research.

## Architecture

### Data Structure
```
data/                              # Primary datasets
├── spotify.csv                    # US creators, 36 shows, YTD 2025 plays (CONFIDENTIAL)
├── youtube.csv                    # Global playlists, 101 shows, watch time metrics
├── amazon.csv                     # Audible/Amazon Music, ~32 shows (padded to 741k rows)
└── iheart_platform_nominations.csv # Platform-specific listening data

alt_data/                          # Supplementary datasets
└── iheartpodcast_nominations.csv  # Publisher cross-platform aggregates
```

### Key Data Characteristics
- **Spotify**: US-focused, 6+ episodes YTD, 30min+ duration, plays through 9/22/2025
- **YouTube**: Global scope, playlist-level metrics, multi-country coverage
- **Amazon**: Massive dataset with significant padding - only ~32 actual shows in 741k+ rows
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
- Spotify Plays vs YouTube Watch Time vs Amazon Total Plays
- Geographic distribution (YouTube's multi-country vs US-focused platforms)
- Completion rates and engagement metrics across platforms
- Show performance for Golden Globes or similar award contexts

### No Traditional Development Stack
This is a pure data analysis project with no existing:
- Package managers (package.json, requirements.txt)
- Build/test/lint scripts
- Source code files
- Testing frameworks

Any analysis scripts or visualization tools will need to be created from scratch using appropriate data science libraries (pandas, matplotlib, seaborn, etc.).