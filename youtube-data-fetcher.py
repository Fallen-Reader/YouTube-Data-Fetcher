import requests
import sqlite3 as sq
import requests
import pandas as pd
import logging
import os
from dotenv import load_dotenv

load_dotenv()

API_key = os.getenv("API_KEY")
base_url = "https://www.googleapis.com/youtube/v3/search?"
#https://www.googleapis.com/youtube/v3/search?part=snippet&q=query&type=video&key=YOUR_API_KEY

def SearchForvideo(name):
    try:
        url = f"{base_url}part=snippet&q={name}&type=video&key={API_key}"
        response = requests.get(url)
        response.raise_for_status()
        info = response.json()
        if not info.get("items"):
            logging.warning(f"No video is found for query : {name}")
            return None
        
        videos = []
        for item in info["items"]:
            snippet = item["snippet"]
            video_id = item["id"]["videoId"]
            videos.append({
                "title": snippet["title"],
                "channel": snippet["channelTitle"],
                "description": snippet["description"],
                "videoId": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}"
            })
        return videos

    except Exception as e:
        logging.warning(f"{e}")


query = str(input("enter the name : "))
result = SearchForvideo(query)

if result:
    for video in result:
        print(f"title : {video["title"]}\nUrl : {video["url"]}\n")


