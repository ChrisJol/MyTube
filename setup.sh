#!/usr/bin/env bash
set -euo pipefail

echo "🔧 Setting up Video Inspiration Finder..."

# 1) Find a Python 3 interpreter
if command -v python3 >/dev/null 2>&1; then
  PYTHON="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  PYTHON="$(command -v python)"
else
  echo "❌ No Python found. Install Python 3 (e.g., 'brew install python@3.12') and re-run."
  exit 1
fi
echo "🐍 Using: $PYTHON"

# 2) Create venv if needed
if [ ! -d "venv" ]; then
  echo "📦 Creating virtual environment..."
  "$PYTHON" -m venv venv
fi

# 3) Resolve the venv's python explicitly (don't depend on activation)
if [ -x "venv/bin/python" ]; then
  VENV_PY="venv/bin/python"
elif [ -x "venv/bin/python3" ]; then
  VENV_PY="venv/bin/python3"
else
  echo "❌ venv exists but no python executable found in venv/bin."
  ls -l venv/bin || true
  exit 1
fi
echo "🐍 venv interpreter: $VENV_PY"

# (Optional) Activate if you still want it, but not required
# source venv/bin/activate

# 4) Install deps using the venv interpreter explicitly
echo "📚 Installing dependencies..."
"$VENV_PY" -m pip install --upgrade pip
"$VENV_PY" -m pip install requests pandas scikit-learn numpy python-dotenv flask flask-cors

echo "✅ Setup complete!"

# ---- helper funcs unchanged (sqlite3 checks) ----
check_videos() {
  if [ -f "video_inspiration.db" ]; then
    sqlite3 video_inspiration.db "SELECT COUNT(*) FROM videos;" 2>/dev/null || echo "0"
  else
    echo "0"
  fi
}

check_unrated_videos() {
  if [ -f "video_inspiration.db" ]; then
    sqlite3 video_inspiration.db "SELECT COUNT(*) FROM videos v LEFT JOIN preferences p ON v.id = p.video_id WHERE p.video_id IS NULL;" 2>/dev/null || echo "0"
  else
    echo "0"
  fi
}

# ---- main menu (use $VENV_PY instead of 'python') ----
video_count="$(check_videos)"
unrated_count="$(check_unrated_videos)"

echo ""
echo "📊 Current Status:"
echo "   Total videos: $video_count"
echo "   Unrated videos: $unrated_count"
echo ""

echo "Choose what you want to do:"
echo "1. 🌐 Launch Dashboard (recommended)"
echo "2. 📱 Interactive CLI Rating Session"  
echo "3. 🔍 Search for More Videos"
echo "4. 🛠️ Full Setup (Search + Rate + Dashboard)"
echo ""
read -p "Enter choice (1-4): " choice

case "$choice" in
  1)
    echo ""
    echo "🌐 Launching Dashboard..."
    if [ "$unrated_count" -eq "0" ] && [ "$video_count" -gt "0" ]; then
      echo "⚠️  All videos are rated. Searching for more videos first..."
      "$VENV_PY" search_more_videos.py
    elif [ "$video_count" -eq "0" ]; then
      echo "⚠️  No videos found. Searching for videos first..."
      "$VENV_PY" main.py --search-only 2>/dev/null || "$VENV_PY" search_more_videos.py
    fi
    echo ""
    echo "📱 Dashboard will be available at: http://localhost:5001"
    echo "🛑 Press Ctrl+C to stop the server"
    echo "----------------------------------------"
    "$VENV_PY" dashboard_api.py
    ;;
  2)
    echo ""
    echo "📱 Starting Interactive Rating Session..."
    "$VENV_PY" main.py
    ;;
  3)
    echo ""
    echo "🔍 Searching for more videos..."
    "$VENV_PY" search_more_videos.py
    echo ""
    echo "✅ Search complete! You can now:"
    echo "   • Run './setup.sh' again and choose option 1 for Dashboard"
    echo "   • Run '$VENV_PY dashboard_api.py' directly"
    ;;
  4)
    echo ""
    echo "🛠️  Running Full Setup..."
    echo "🔍 Step 1: Searching for videos..."
    "$VENV_PY" main.py --search-only 2>/dev/null || "$VENV_PY" search_more_videos.py
    echo ""
    echo "📱 Step 2: Starting rating session..."
    echo "💡 Tip: Rate at least 10 videos to activate AI recommendations"
    echo "   (You can press 'q' anytime to skip to dashboard)"
    "$VENV_PY" main.py
    ;;
  *)
    echo "❌ Invalid choice. Please run './setup.sh' again."
    exit 1
    ;;
esac
