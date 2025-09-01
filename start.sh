#!/usr/bin/env bash
set -euo pipefail

echo "� MyTube - YouTube Video Recommendation System"
echo "================================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
  echo "❌ Virtual environment not found!"
  echo "Please run the initial setup first:"
  echo "   python3 -m venv venv"
  echo "   source venv/bin/activate"
  echo "   pip install requests pandas scikit-learn numpy python-dotenv flask flask-cors"
  exit 1
fi

# Find the venv Python interpreter
if [ -x "venv/bin/python" ]; then
  VENV_PY="venv/bin/python"
elif [ -x "venv/bin/python3" ]; then
  VENV_PY="venv/bin/python3"
else
  echo "❌ Virtual environment exists but Python interpreter not found."
  exit 1
fi

echo ""
echo "🌐 Starting dashboard server..."
echo "📱 Dashboard will open automatically in your browser"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Start the dashboard server (run.py handles auto-browser opening)
"$VENV_PY" run.py web --port 8000
