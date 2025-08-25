#!/usr/bin/env python3
import os
from dotenv import load_dotenv

from src.database.manager import setup_database_tables
from src.database.video_operations import save_videos_to_database, save_video_features_to_database
from src.youtube.search import search_youtube_videos_by_query, get_coding_search_queries
from src.youtube.details import get_video_details_from_youtube
from src.youtube.utils import remove_duplicate_videos
from src.ml.feature_extraction import extract_all_features_from_video

load_dotenv()

def search_more_videos():
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("Error: YOUTUBE_API_KEY not found in environment variables")
        return

    db_path = "video_inspiration.db"
    setup_database_tables(db_path)

    print("🔍 Searching for more coding videos...")

    # Use different/additional search queries to find new videos
    additional_queries = [
        "python projects for beginners viral",
        "full stack web development course",
        "machine learning crash course",
        "javascript frameworks comparison",
        "coding interview preparation",
        "docker tutorial for developers",
        "git and github tutorial",
        "database design tutorial",
        "API development tutorial"
    ]

    all_videos = []

    for query in additional_queries:
        print(f"  Searching: {query}")
        video_ids = search_youtube_videos_by_query(api_key, query, 10)
        videos = get_video_details_from_youtube(api_key, video_ids)
        all_videos.extend(videos)

    unique_videos = remove_duplicate_videos(all_videos)

    if unique_videos:
        save_videos_to_database(unique_videos, db_path)

        for video in unique_videos:
            features = extract_all_features_from_video(video)
            save_video_features_to_database(video['id'], features, db_path)

        print(f"✅ Found and saved {len(unique_videos)} new videos!")
    else:
        print("❌ No new videos found.")

if __name__ == "__main__":
    search_more_videos()