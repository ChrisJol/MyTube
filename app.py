#!/usr/bin/env python3
"""
MyTube - YouTube Video Recommendation System
Single entry point for all functionality
"""
import argparse
import sys
import os
import subprocess
import time
import sqlite3
from pathlib import Path

def install():
    """Install dependencies and set up the application"""
    print("🔧 MyTube - Installation")
    print("========================")
    
    # Find Python interpreter
    if subprocess.run(["which", "python3"], capture_output=True).returncode == 0:
        python_cmd = "python3"
    elif subprocess.run(["which", "python"], capture_output=True).returncode == 0:
        python_cmd = "python"
    else:
        print("❌ No Python found. Install Python 3 and re-run.")
        print("   macOS: brew install python@3.12")
        print("   Ubuntu: sudo apt install python3 python3-venv")
        return False
    
    print(f"🐍 Using: {python_cmd}")
    
    # Create virtual environment
    if not Path("venv").exists():
        print("📦 Creating virtual environment...")
        subprocess.run([python_cmd, "-m", "venv", "venv"], check=True)
    else:
        print("📦 Virtual environment already exists")
    
    # Find venv Python
    venv_python = "venv/bin/python" if Path("venv/bin/python").exists() else "venv/bin/python3"
    if not Path(venv_python).exists():
        print("❌ Virtual environment creation failed")
        return False
    
    # Install dependencies
    print("📚 Installing dependencies...")
    subprocess.run([venv_python, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([
        venv_python, "-m", "pip", "install", 
        "requests", "pandas", "scikit-learn", "numpy", "python-dotenv", "flask", "flask-cors"
    ], check=True)
    
    # Check for .env file
    if not Path(".env").exists():
        print("⚠️  No .env file found!")
        print("Please create a .env file with your YouTube API key:")
        print("   YOUTUBE_API_KEY=your_api_key_here")
        print("")
        print("Get your API key at: https://console.developers.google.com/")
        print("")
    
    print("✅ Installation complete!")
    print("")
    print("🚀 To start the application:")
    print("   python app.py           # Start web dashboard")
    print("   python app.py search    # Search for more videos")
    return True

def check_has_videos():
    """Check if database has videos"""
    if not Path("video_inspiration.db").exists():
        return False
    
    try:
        conn = sqlite3.connect("video_inspiration.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM videos")
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    except:
        return False

def run_web(port=8000, debug=False, auto_open=True):
    """Run the web dashboard"""
    from src.web import create_app

    print("🚀 MyTube - Web Dashboard")
    print("=========================")

    # Check if database and videos exist
    if not check_has_videos():
        print("📋 No videos found in database. Loading initial videos...")
        try:
            _load_initial_videos()
            # Verify videos were actually loaded
            if check_has_videos():
                print("✅ Initial videos loaded successfully!")
            else:
                print("⚠️  Warning: No videos were loaded (API may have failed)")
                print("Dashboard will start in demo mode.")
        except Exception as e:
            print(f"⚠️  Could not load initial videos: {e}")
            print("   This is likely due to YouTube API quota limits.")
            print("   Dashboard will start in demo mode - you can still explore the interface!")
            print("   API quotas reset daily, so try again tomorrow.")
        print("")

    # Start dashboard
    print(f"🌐 Starting dashboard server on port {port}...")
    print(f"📱 Dashboard will be available at: http://localhost:{port}")
    print("🛑 Press Ctrl+C to stop the server")
    print("-" * 40)

    # Auto-open browser
    if auto_open:
        import threading
        def open_browser():
            time.sleep(2)
            import webbrowser
            webbrowser.open(f"http://localhost:{port}")

        threading.Thread(target=open_browser, daemon=True).start()

    try:
        app = create_app()
        app.run(host='0.0.0.0', port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped!")
    except Exception as e:
        print(f"Error starting dashboard: {e}")

def _load_initial_videos():
    """Load initial videos when starting the web app for the first time"""
    import os
    from dotenv import load_dotenv
    from src.database.manager import setup_database_tables
    from src.database.video_operations import save_videos_to_database, save_video_features_to_database
    from src.services.youtube_service import YouTubeService
    from src.ml.feature_extraction import extract_all_features_from_video
    from src.config.search_config import get_search_queries

    load_dotenv()

    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        raise Exception("YOUTUBE_API_KEY not found in environment variables")

    db_path = "video_inspiration.db"
    setup_database_tables(db_path)

    youtube_service = YouTubeService(api_key)
    all_queries = get_search_queries()

    # Use first 5 queries for initial load
    initial_queries = all_queries[:5]
    print(f"      Searching {len(initial_queries)} topics...")

    all_videos = []
    for query in initial_queries:
        try:
            videos = youtube_service.search_and_get_details(query, 8)  # Fewer videos per query for initial load
            all_videos.extend(videos)
            print(f"      Found {len(videos)} videos for '{query}'")
        except Exception as e:
            print(f"      Warning: Could not search '{query}': {e}")

    unique_videos = YouTubeService.remove_duplicate_videos(all_videos)
    print(f"      Total unique videos: {len(unique_videos)}")

    if unique_videos:
        save_videos_to_database(unique_videos, db_path)
        for video in unique_videos:
            features = extract_all_features_from_video(video)
            save_video_features_to_database(video['id'], features, db_path)
        print(f"      Saved {len(unique_videos)} videos to database")
    else:
        raise Exception("No videos were found (likely due to API quota limits)")

def run_search():
    """Search for videos and add them to the database"""
    import os
    from dotenv import load_dotenv
    from src.database.manager import setup_database_tables
    from src.database.video_operations import save_videos_to_database, save_video_features_to_database
    from src.services.youtube_service import YouTubeService
    from src.ml.feature_extraction import extract_all_features_from_video
    from src.config.search_config import get_search_queries
    import random

    load_dotenv()

    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("❌ Error: YOUTUBE_API_KEY not found in environment variables")
        print("Please create a .env file with your YouTube API key:")
        print("   YOUTUBE_API_KEY=your_api_key_here")
        return

    db_path = "video_inspiration.db"
    setup_database_tables(db_path)

    youtube_service = YouTubeService(api_key)
    all_queries = get_search_queries()

    # Use different queries for search vs initial load
    if len(all_queries) > 5:
        search_queries = all_queries[5:10]  # Use queries 5-10 for search command
    else:
        search_queries = all_queries.copy()
        random.shuffle(search_queries)
        search_queries = search_queries[:5]  # Limit to 5 queries

    print(f"🔍 Searching {len(search_queries)} topics for videos...")

    all_videos = []
    for i, query in enumerate(search_queries, 1):
        print(f"  [{i}/{len(search_queries)}] Searching: {query}")
        try:
            videos = youtube_service.search_and_get_details(query, 10)
            all_videos.extend(videos)
            print(f"      Found {len(videos)} videos")
        except Exception as e:
            print(f"      Error searching '{query}': {e}")

    unique_videos = YouTubeService.remove_duplicate_videos(all_videos)

    if unique_videos:
        print(f"💾 Saving {len(unique_videos)} unique videos to database...")
        save_videos_to_database(unique_videos, db_path)

        print("🧠 Extracting features for ML recommendations...")
        for i, video in enumerate(unique_videos, 1):
            if i % 10 == 0:  # Show progress every 10 videos
                print(f"      Processing features: {i}/{len(unique_videos)}")
            features = extract_all_features_from_video(video)
            save_video_features_to_database(video['id'], features, db_path)

        print(f"✅ Successfully added {len(unique_videos)} videos to the database!")
    else:
        print("❌ No new videos found.")
        print("   This might be due to YouTube API quota limits or network issues.")
        print("   API quotas reset daily. Try again later.")

def ensure_venv():
    """Ensure we're running in the virtual environment"""
    if Path("venv").exists() and not sys.executable.startswith(str(Path("venv").absolute())):
        # We have a venv but we're not using it
        venv_python = "venv/bin/python" if Path("venv/bin/python").exists() else "venv/bin/python3"
        if Path(venv_python).exists():
            # Re-run with venv python
            os.execv(venv_python, [venv_python] + sys.argv)

def main():
    # Auto-switch to venv if available (except for install command)
    if len(sys.argv) == 1 or (len(sys.argv) > 1 and sys.argv[1] != 'install'):
        ensure_venv()

    parser = argparse.ArgumentParser(
        description="MyTube - YouTube Video Recommendation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  install                      # Install dependencies and set up
  run                         # Start web dashboard (default)
  search                      # Search for more videos

Examples:
  python app.py install       # First-time setup
  python app.py run           # Start web dashboard
  python app.py run --port 3000 --debug  # Custom options
  python app.py search        # Search for videos
        """
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        default='run',
        choices=['install', 'run', 'search'],
        help='Command to execute (default: run)'
    )
    
    parser.add_argument(
        '--port', 
        type=int, 
        default=8000,
        help='Port for web server (default: 8000)'
    )
    
    parser.add_argument(
        '--debug', 
        action='store_true',
        help='Run web server in debug mode'
    )
    
    parser.add_argument(
        '--no-browser', 
        action='store_true',
        help='Don\'t auto-open browser for web mode'
    )
    
    args = parser.parse_args()
    
    if args.command == 'install':
        install()
    elif args.command == 'search':
        run_search()
    elif args.command == 'run':
        run_web(
            port=args.port,
            debug=args.debug,
            auto_open=not args.no_browser
        )

if __name__ == "__main__":
    main()
