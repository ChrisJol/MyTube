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

# ---- Auto-launch dashboard ----
echo ""
echo "🚀 Starting Video Inspiration Dashboard..."

# Check if we have videos, and search for some if we don't
video_count="0"
if [ -f "video_inspiration.db" ]; then
  video_count="$(sqlite3 video_inspiration.db "SELECT COUNT(*) FROM videos;" 2>/dev/null || echo "0")"
fi

if [ "$video_count" -eq "0" ]; then
  echo "� No videos found. Searching for initial videos..."
  "$VENV_PY" search_more_videos.py
  echo ""
fi

echo "🌐 Opening dashboard in your browser..."
echo "📱 Dashboard URL: http://localhost:5001"
echo ""
echo "� How to use:"
echo "   • Rate videos by clicking 👍 or 👎"
echo "   • The AI learns from your ratings and improves recommendations"
echo "   • More videos are automatically fetched as needed"
echo "   • Training happens automatically - no minimum required!"
echo ""
echo "🛑 Press Ctrl+C to stop the server"
echo "----------------------------------------"

# Try to open the dashboard in the default browser
if command -v open >/dev/null 2>&1; then
  # macOS
  (sleep 2 && open "http://localhost:5001") &
elif command -v xdg-open >/dev/null 2>&1; then
  # Linux
  (sleep 2 && xdg-open "http://localhost:5001") &
elif command -v start >/dev/null 2>&1; then
  # Windows
  (sleep 2 && start "http://localhost:5001") &
fi

# Start the dashboard server
"$VENV_PY" dashboard_api.py
