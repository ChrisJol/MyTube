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
    print("   python app.py run       # Start web dashboard")
    print("   python app.py cli       # Start CLI mode")
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

def run_cli():
    """Run the CLI interface"""
    from main import main
    main()

def run_web(port=8000, debug=False, auto_open=True):
    """Run the web dashboard"""
    from src.web import create_app
    
    print("🚀 MyTube - Web Dashboard")
    print("=========================")
    
    # Check if database and videos exist
    if not check_has_videos():
        print("⚠️  No videos found in database!")
        print("\nOptions:")
        print("1. Run CLI first to search and rate videos")
        print("2. Continue with empty dashboard (demo mode)")
        
        choice = input("\nEnter choice (1/2): ").strip()
        
        if choice == "1":
            print("\n🔍 Running CLI application first...")
            try:
                run_cli()
            except KeyboardInterrupt:
                print("\n👋 Switching to dashboard...")
                time.sleep(1)
            except Exception as e:
                print(f"Error running CLI: {e}")
                return
    
    # Start dashboard
    print(f"\n🌐 Starting dashboard server on port {port}...")
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

def run_search():
    """Run additional video search"""
    import os
    from dotenv import load_dotenv
    from src.database.manager import setup_database_tables
    from src.database.video_operations import save_videos_to_database, save_video_features_to_database
    from src.youtube.search import search_youtube_videos_by_query
    from src.youtube.details import get_video_details_from_youtube
    from src.youtube.utils import remove_duplicate_videos
    from src.ml.feature_extraction import extract_all_features_from_video
    from src.config.search_config import get_search_queries
    import random
    
    load_dotenv()
    
    api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        print("Error: YOUTUBE_API_KEY not found in environment variables")
        return

    db_path = "video_inspiration.db"
    setup_database_tables(db_path)

    print("🔍 Searching for more videos...")

    all_queries = get_search_queries()
    if len(all_queries) > 5:
        search_queries = all_queries[5:]
    else:
        search_queries = all_queries.copy()
        random.shuffle(search_queries)

    print(f"Using {len(search_queries)} search queries for discovery...")

    all_videos = []
    for query in search_queries:
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
  cli                         # Start CLI interface
  search                      # Search for more videos

Examples:
  python app.py install       # First-time setup
  python app.py run           # Start web dashboard
  python app.py run --port 3000 --debug  # Custom options
  python app.py cli           # CLI interface
  python app.py search        # Search for videos
        """
    )
    
    parser.add_argument(
        'command', 
        nargs='?', 
        default='run',
        choices=['install', 'run', 'cli', 'search'],
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
    elif args.command == 'cli':
        run_cli()
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
