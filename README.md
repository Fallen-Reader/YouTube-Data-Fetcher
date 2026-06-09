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
enter the name : nigthcore

title : Nightcore - Apollo - (Lyrics)
Url : https://www.youtube.com/watch?v=TpIqDm031gg

title : Nightcore - Teeth (But it hits hard) (Lyrics)
Url : https://www.youtube.com/watch?v=i5KjN0GXumw

title : Nightcore - Older // Sasha Sloan (Lyrics)
Url : https://www.youtube.com/watch?v=mgYR5fp161Y

title : Nightcore - No Friends (Lyrics)
Url : https://www.youtube.com/watch?v=9xG5aPvrS-k

title : Nightcore - House of Memories (Lyrics)
Url : https://www.youtube.com/watch?v=ee8ROcjVpvg
```

## Project Idea

This project is designed to be expanded later into a larger tool that can:
- save search results into SQLite,
- export data to CSV,
- search playlists and channels,
- and create charts from saved data.

## Future Improvements

Planned next steps:
- Add playlist search.
- Add channel search.
- Save results into a database.
- Add duplicate handling.
- Build visuals based on search history.
- Add filters for date, channel, or keyword.

## Notes

- Use environment variables for secret values.
- The YouTube Data API has usage limits, so results should be fetched carefully.

## License

This project is for learning and personal practice.