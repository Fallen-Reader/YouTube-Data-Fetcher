# YouTube Data Fetcher

A beginner-friendly Python project that uses the YouTube Data API v3 to search for videos by keyword and display basic details such as title, channel name, publish date, and video link.

This project is part of my learning journey and will later grow into a larger data collection and visualization project.

## Overview

The goal of this project is to fetch YouTube video data in a structured way, similar to how web scraping collects sources from the web.  
Instead of scraping page HTML, this project uses the official YouTube Data API to get clean JSON data.

The project currently focuses on:
- searching videos by keyword,
- extracting basic video information,
- generating clickable YouTube links,
- and preparing data for future saving and analysis.

## Features

- Search YouTube videos by keyword.
- Fetch basic details for each video.
- Display title, channel name, published date, and video URL.
- Return results in a structured format for future pandas/SQLite use.
- Easy to extend with playlists, channels, saving, and visualization.

## Technologies Used

- Python
- Requests
- pandas
- logging
- YouTube Data API v3
- SQLalchemy
- Cache Managment

## How It Works

1. The user enters a search keyword.
2. The script sends a request to the YouTube Data API search endpoint.
3. The API returns matching video results in JSON format.
4. The script extracts useful details from each result.
5. The results are printed or returned as a list/dictionary for later use.

## Data Retrieved

For each video, the project can fetch:
- title
- channel name
- published date
- description
- video ID
- direct YouTube URL

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/Fallen-Reader/YouTube-Data-Fetcher.git
```

### 2. Install dependencies

```bash
pip install requests pandas python-dotenv
```

### 3. Create a `.env` file

Create a file named `.env` in the project root:

```env
API_KEY=your_youtube_api_key_here
```

### 4. Add `.env` to `.gitignore`

```gitignore
nano .gitignore
.env
```

### 5. Run the script

```bash
python youtube-data-fetcher.py
```

## Example Output

```text
=== YouTube Fetcher Console UI ===
1 - Search videos
2 - Search playlists
3 - List videos by topic
4 - List playlists by topic
5 - Exit
Enter choice: 1
Enter search query: probability for quants
Max results (default 10): 5
Topics (comma-separated): maths,education
[OK] Topic already exists: 7 | maths
[OK] Topic already exists: 3 | education
Fetching metrics (views, likes, duration)...

Saving to database...

=== Results (5) ===
1. [How to Get Good at Probability &amp; Statistics (for Quants &amp; Finance Careers) 📚👩🏼‍💻] — Ioana Roman

Video: How to Get Good at Probability &amp; Statistics (for Quants &amp; Finance Careers) 📚👩🏼‍💻
Score: ███████░░░ (0.717)
Views: 42713
Likes: 1983
Duration: 1035s
   -> https://www.youtube.com/watch?v=zcnHYRxHSpU
2. [Probability - Shortcuts &amp; Tricks for 2026 Placement Tests, Job Interviews &amp; Exams] — CareerRide

Video: Probability - Shortcuts &amp; Tricks for 2026 Placement Tests, Job Interviews &amp; Exams
Score: ██████░░░░ (0.663)
Views: 1966936
Likes: 30813
Duration: 4058s
   -> https://www.youtube.com/watch?v=ximxxERGSUc
3. [Odd Tosses Probability | Citadel Quant Interview Problem] — quantprof 

Video: Odd Tosses Probability | Citadel Quant Interview Problem
Score: ██████░░░░ (0.606)
Views: 7700
Likes: 208
Duration: 177s
   -> https://www.youtube.com/watch?v=RdGdqNe8A8U
4. [Math for Quantatative Finance] — The Math Sorcerer

Video: Math for Quantatative Finance
Score: ███████░░░ (0.707)
Views: 119796
Likes: 4231
Duration: 337s
   -> https://www.youtube.com/watch?v=8U0ksSGEHtc
5. [Jane Street Interview Question] — quantprof 

Video: Jane Street Interview Question
Score: ██████░░░░ (0.605)
Views: 354902
Likes: 6224
Duration: 22s
   -> https://www.youtube.com/watch?v=sfFI28tM8Ds

```

## Project Idea

This project is designed to be expanded later into a larger tool that can:
- save search results into SQLite,
- export data to CSV,
- search playlists and channels,
- and create charts from saved data.

## Future Improvements

Planned next steps:
- Add channel search. 
- Add duplicate handling.
- Build visuals based on search history.
- Quality metrics. ✅
- Add filters for date, channel, or keyword.

## Notes

- Use environment variables for secret values.
- The YouTube Data API has usage limits, so results should be fetched carefully.

## License

This project is for learning and personal practice.
