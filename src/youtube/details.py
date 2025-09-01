import requests
import json
from typing import List, Dict

def get_video_details_from_youtube(api_key: str, video_ids: List[str]) -> List[Dict]:
    if not video_ids:
        return []

    details_url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        'key': api_key,
        'id': ','.join(video_ids),
        'part': 'snippet,statistics,contentDetails'
    }

    try:
        response = requests.get(details_url, params=params)
        data = response.json()

        videos = []
        for item in data.get('items', []):
            video = parse_youtube_video_response(item)
            if is_relevant_video(video):
                videos.append(video)

        return videos

    except Exception as e:
        print(f"Error getting video details: {e}")
        return []

def parse_youtube_video_response(item: Dict) -> Dict:
    snippet = item['snippet']
    statistics = item['statistics']

    return {
        'id': item['id'],
        'title': snippet['title'],
        'description': snippet['description'],
        'view_count': int(statistics.get('viewCount', 0)),
        'like_count': int(statistics.get('likeCount', 0)),
        'comment_count': int(statistics.get('commentCount', 0)),
        'duration': item['contentDetails']['duration'],
        'published_at': snippet['publishedAt'],
        'channel_name': snippet['channelTitle'],
        'thumbnail_url': snippet['thumbnails']['high']['url'],
        'tags': json.dumps(snippet.get('tags', [])),
        'category_id': int(snippet.get('categoryId', 0)),
        'url': f"https://www.youtube.com/watch?v={item['id']}"
    }

def is_relevant_video(video: Dict) -> bool:
    """Filter videos based on general quality criteria, not content type."""
    # Basic quality filters - no content-specific bias
    if video['view_count'] < 10000:  # Lowered threshold for broader content
        return False

    # Filter out very short videos (likely not substantial content)
    duration = video.get('duration', '')
    if 'PT' in duration:
        # Parse ISO 8601 duration format (PT1M30S = 1 minute 30 seconds)
        import re
        minutes = re.findall(r'(\d+)M', duration)
        seconds = re.findall(r'(\d+)S', duration)
        total_seconds = (int(minutes[0]) * 60 if minutes else 0) + (int(seconds[0]) if seconds else 0)
        if total_seconds < 60:  # Skip videos under 1 minute
            return False

    return True