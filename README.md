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
git clone https://github.com/Omniscient-Frame/YouTube-Data-Fetcher.git
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
Enter search query: nightcore hardstyle
Max results (default 10): 10       
Topics (comma-separated): nightcore,songs
[OK] Topic already exists: 1 | nightcore
[OK] Topic created: 2 | songs

Saving to database...

=== Results (10) ===
1. [Nightcore - Hardstyle Mix [1 hour] #21] — Fr3shDs4
   -> https://www.youtube.com/watch?v=IsKrbjxJHnE
2. [Nightcore | Canon in D (Jatimatic Hardstyle Bootleg)] — Mine
   -> https://www.youtube.com/watch?v=DUR21pca1oY
3. [Old School Classic Nightcore Mix | Complete 2011 to 2021 Hottest Songs] — AxionX
   -> https://www.youtube.com/watch?v=xfjnN3sXYhk
4. [Ultra Ultra Masculine White Girl Playlist [Hardstyle Mix]] — 5MO
   -> https://www.youtube.com/watch?v=yRvodjtCMJo
5. [Nightcore - How Do You Do] — Nightcore Lab NCL
   -> https://www.youtube.com/watch?v=0GEX_sVwUn4
6. [Russian Nightcore Hardstyle Playlist|Русский Найткор Хардстайл Плейлист] — Nyctereute
   -> https://www.youtube.com/watch?v=xve6mJYT270
7. [Nightcore - Stamp On The Ground (Lyrics)] — Nightcore Zodiac
   -> https://www.youtube.com/watch?v=dwhnsV9yhZw
8. [[NIGHTCORE] WE ARE CHARLIE KIRK (Agartha Hardstyle Remix)] — Dirtman Grassy
   -> https://www.youtube.com/watch?v=tlOdillu4FI
9. [Nightcore - Clarity] — NightcoreReality
   -> https://www.youtube.com/watch?v=9buluPWlkAA
10. [i kissed a girl (hardstyle)] — singedJAM
   -> https://www.youtube.com/watch?v=8sIJNHn1uyc
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
- Quality metrics
- Add filters for date, channel, or keyword.

## Notes

- Use environment variables for secret values.
- The YouTube Data API has usage limits, so results should be fetched carefully.

## License

This project is for learning and personal practice.
