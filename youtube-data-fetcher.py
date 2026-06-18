import os
import re
import logging
import time
import hashlib
from dotenv import load_dotenv
from typing import Optional, List, Dict, Tuple
from learning_db import (init_db,upsert_video,upsert_playlist,
                         cli_add_video,cli_add_playlist,cli_list_videos_by_topic,
                         cli_list_playlists_by_topic,cli_add_topic)
load_dotenv()

try:
    from googleapiclient.discovery import build
    from googleapiclient import errors as google_errors
except ImportError:
    raise ImportError("Please install google-api-python-client: pip install google-api-python-client")


ENV = os.environ.get("ENV", "development").lower()
LOGLEVEL = logging.DEBUG if ENV == "development" else logging.WARNING

logging.basicConfig(
    level=LOGLEVEL,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="youtube-fetcher.log",
    filemode="a"
)

CACHE: Dict[str, Tuple[List[Dict], float]] = {}
CACHE_TTL = 30 * 60  # 30 minutes
CACHE_MAX_SIZE = 200

def _cache_key(query: str, type_: str = "video", maxResults: int = 10) -> str:
    return hashlib.md5(f"{query}|{type_.lower()}|{maxResults}".encode()).hexdigest()


def cache_get(key: str) -> Optional[List[Dict]]:
    if key not in CACHE:
        return None
    results, ts = CACHE[key]
    if time.time() - ts > CACHE_TTL:
        CACHE.pop(key, None)
        return None
    return results


def get_timestamp(k:str) -> float:
    return CACHE[k][1]


def cache_put(key: str, results: List[Dict]) -> None:
    if len(CACHE) >= CACHE_MAX_SIZE:
        oldest = min(CACHE.keys(), key=get_timestamp)
        CACHE.pop(oldest, None)
    CACHE[key] = (results, time.time())

def youtube_build(api_key: str):
    return build("youtube", "v3", developerKey=api_key)

def search_videos(youtube, query: str, maxResults: int = 10, type_: str = "video") -> List[Dict]:

    key = _cache_key(query, type_, maxResults)
    cached = cache_get(key)
    if cached is not None:
        logging.info(f"Cache hit for query: {query}")
        return cached

    results = []
    page_token: Optional[str] = None
    attempts = 0
    max_attempts = 5
    base_wait = 2.0

    while len(results) < maxResults and (page_token is not None or attempts == 0):
        attempts += 1
        try:
            logging.debug(f"Requesting search: query={query}, page_token={page_token}, attempt={attempts}")
            req = youtube.search().list(
                part="snippet",
                q=query,
                type=type_,
                maxResults=min(maxResults - len(results), 50),
                pageToken=page_token or ""
            )
            resp = req.execute()

            items = resp.get("items", [])
            if not items:
                logging.warning(f"No items returned for query: {query}")
                break

            for item in items:
                snippet = item["snippet"]
                item_id = item["id"]
                title = snippet["title"]
                channel = snippet["channelTitle"]

                if type_ == "video":
                    video_id = item_id["videoId"]
                    url = f"https://www.youtube.com/watch?v={video_id}"
                    results.append({"title": title, "channel": channel, "videoId": video_id, "url": url})
                elif type_ == "playlist":
                    playlist_id = item_id["playlistId"]
                    url = f"https://www.youtube.com/playlist?list={playlist_id}"
                    results.append({"title": title, "channel": channel, "playlistId": playlist_id, "url": url})
                elif type_=="channel":
                    channel_id = item_id["channelId"]
                    url = f"https://www.youtube.com/channel/{channel_id}"
                    results.append({"title": title, "channel": channel, "channelId": channel_id, "url": url})

            page_token = resp.get("nextPageToken") or None
            if page_token is None:
                break

        except google_errors.HttpError as e:
            status = getattr(e, "status_code", None)
            msg = str(e)
            logging.warning(f"HttpError: status={status}, msg={msg}")

            if status == 403:
                logging.error("Quota exceeded (403). Stopping search.")
                break
            elif status in (429, 500, 502, 503, 504):
                wait_time = base_wait * (2 ** (attempts - 1))
                logging.info(f"Transient error {status}, retrying after {wait_time}s")
                time.sleep(wait_time)
                continue
            else:
                break
        except Exception as e:
            logging.exception(f"Unexpected error during search: {e}")
            break

    cache_put(key, results)
    logging.info(f"Search returned {len(results)} results for query: {query}")
    return results

def fetch_video_metrics(youtube,video_ids : list) -> dict:
    if not video_ids:
        return {}
    
    metrics = {}

    for i in range(0,len(video_ids,50)):
        batch = video_ids[i:i+50]
        id_str = ",".join(batch)

        try:
            req = youtube.videos().list(
                part="statistics,contentDeatails",
                id = id_str
            )
            resp = req.execute()

            for item in resp.get("items",[]):
                video_id = item["id"]
                stats = item["statistics"]
                content = item["contentDetails"]

                metrics[video_id]={
                    "views":int(stats.get("viewCount",0)),
                    "likes":int(stats.get("likeCount",0)),
                    "comments":int(stats.get("commentCount",0)),
                    "duration_seconds": parse_duration(content.get("duration", "PT0S")) 
                }
        
        except google_errors.HttpError as e:
            status = getattr(e,"status_code",None)
            if status == 403:
                print("Quota exceeded(403). Stopping metrics fetch")
                break
            else:
                print(f"API error , status = {stats}\nmsg={str(e)}")
                continue
    return metrics


def handle_search(youtube, type_: str, default_max: int = 10):
    query = input("Enter search query: ").strip()
    try:
        max_results = int(input(f"Max results (default {default_max}): ").strip() or str(default_max))
        max_results = max(1, min(max_results, 100))

    except ValueError:
        max_results = default_max

    topics_input = input("Topics (comma-separated): ").strip()
    topics = [t.strip() for t in topics_input.split(",") if t.strip()]
    for t in topics:
        cli_add_topic(t)
        
    results = search_videos(youtube, query, maxResults=max_results, type_=type_)
    return results, topics
   
def console_ui(API_key: str):
    youtube = youtube_build(API_key)
    logging.info("YouTube service client created.")
    init_db()
    while True:
        print("\n=== YouTube Fetcher Console UI ===")
        print("1 - Search videos")
        print("2 - Search playlists")
        print("3 - List videos by topic")
        print("4 - List playlists by topic")
        print("5 - Exit")
        
        try:
            choice = int(input("Enter choice: ").strip())

        except ValueError:
            print("Invalid input. Try again.")
            continue

        if choice == 5:
            print("Exiting...")
            break

        if choice == 1:
            results,topics = handle_search(youtube,type_="video")
            if results:
                print("\nSaving to database...")
                saved_videos =[]
                for r in results:
                    video = upsert_video(
                        youtube_id=r["videoId"],
                        title=r["title"],
                        channel=r["channel"],
                        url=r["url"],
                        topics=topics,
                        is_verified=False
                    )
                    saved_videos(video)
                    print(f"[Saved] Video: {video.id} | {video.title}")
                
                print("\nFetching metrics (views, likes, duration)...")
                video_ids = [v.youtube_id for v in saved_videos[:10]]

                metrics = fetch_video_metrics(youtube,video_ids)

                print("Updating database with metrics")

                for video in saved_videos[:10]:
                    if video.youtube_id in metrics:
                        m = metrics[video.youtube_id]
                        video.views = m["views"]
                        video.likes = m["likes"]
                        video.comments = m["comments"]
                        video.duration_seconds = m["duration_seconds"]
                        sess = get_session()
                        sess.commit()
                        sess.close()
                
                print(f"\n=== Results ({len(results)}) ===")
                for i, r in enumerate(results, start=1):
                    print(f"{i}. [{r['title']}] — {r['channel']}")
                    print(f"   -> {r['url']}")
        
        elif choice == 2:
            results,topics = handle_search(youtube,type_="playlist")
            if results:
                print("\nSaving to database...")
                for r in results:
                    upsert_playlist(
                        youtube_id=r["playlistId"],
                        title=r["title"],
                        channel=r["channel"],
                        url=r["url"],
                        topics=topics,
                        is_verified=False
                    )
                
                print(f"\n=== Results ({len(results)}) ===")
                for i, r in enumerate(results, start=1):
                    print(f"{i}. [{r['title']}] — {r['channel']}")
                    print(f"   -> {r['url']}")
        
        elif choice == 3:
            topic = input("Enter topic name: ").strip()
            cli_list_videos_by_topic(topic)
        
        elif choice == 4:
            topic = input("Enter topic name: ").strip()
            cli_list_playlists_by_topic(topic)
        
        else:
            print("Invalid choice. Try again.")


def main():
    API_key = os.getenv("API_KEY")
    if not API_key:
        print("ERROR: YT_API_KEY environment variable not set. Set it in .env or export YT_API_KEY=...")
        logging.error("YT_API_KEY not set")
        return

    console_ui(API_key)

if __name__ == "__main__":
    main()