from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import json

# Youtube API key
load_dotenv()
youtube_key = os.getenv("YOUTUBE_API")

def fetch_videos(query, video_num):
  try:
    # Fetch videos from Youtube
    youtube = build("youtube", "v3", developerKey=youtube_key)
    request = youtube.search().list(
        part = "snippet",
        q = query,
        type = "video",
        maxResults = video_num
    )
    response = request.execute()

    # Organize videos
    result = []
    for item in response["items"]:
      
      id = item["id"]["videoId"]
      
      video = {
        "title": item["snippet"]["title"],
        "id": id,
        "channel": item["snippet"]["channelTitle"],
        "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
        "publish_time": item["snippet"]["publishedAt"],
        "video_url": f"https://www.youtube.com/watch?v={id}"
      }
      
      result.append(video)
      
    return result
  except Exception as e:
    print("Error fetching video:", e)
    return []

if __name__ == "__main__":
  videos = fetch_videos("Svelte tutorial", 5)
  for vid in videos:
    print(vid)