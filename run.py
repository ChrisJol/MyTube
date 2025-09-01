#!/usr/bin/env python3
"""
MyTube - YouTube Video Recommendation System
Main entry point for both CLI and web interfaces
"""
import argparse
import sys
import os
import subprocess
import time
from pathlib import Path

def check_database_exists():
    return Path("video_inspiration.db").exists()

def check_has_videos():
    if not check_database_exists():
        return False
    
    import sqlite3
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

def run_web(port=5000, debug=False, auto_open=True):
    """Run the web dashboard"""
    from app import create_app
    
    print("🚀 Video Inspiration Dashboard")
    print("=" * 40)
    
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
    from search_more_videos import main as search_main
    search_main()

def main():
    parser = argparse.ArgumentParser(
        description="MyTube - YouTube Video Recommendation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                    # Run web dashboard (default)
  python run.py cli                # Run CLI interface
  python run.py web --port 8000    # Run web on custom port
  python run.py search             # Search for more videos
        """
    )
    
    parser.add_argument(
        'mode', 
        nargs='?', 
        default='web',
        choices=['web', 'cli', 'search'],
        help='Run mode (default: web)'
    )
    
    parser.add_argument(
        '--port', 
        type=int, 
        default=5000,
        help='Port for web server (default: 5000)'
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
    
    if args.mode == 'cli':
        run_cli()
    elif args.mode == 'search':
        run_search()
    elif args.mode == 'web':
        run_web(
            port=args.port, 
            debug=args.debug, 
            auto_open=not args.no_browser
        )

if __name__ == "__main__":
    main()
