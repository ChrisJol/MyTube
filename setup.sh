#!/usr/bin/env bash
set -euo pipefail

echo "🔧 MyTube - Initial Setup"
echo "========================="

# 1) Find a Python 3 interpreter
if command -v python3 >/dev/null 2>&1; then
  PYTHON="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
  PYTHON="$(command -v python)"
else
  echo "❌ No Python found. Install Python 3 and re-run."
  echo "   macOS: brew install python@3.12"
  echo "   Ubuntu: sudo apt install python3 python3-venv"
  exit 1
fi
echo "🐍 Using: $PYTHON"

# 2) Create venv if needed
if [ ! -d "venv" ]; then
  echo "📦 Creating virtual environment..."
  "$PYTHON" -m venv venv
else
  echo "📦 Virtual environment already exists"
fi

# 3) Find venv Python
if [ -x "venv/bin/python" ]; then
  VENV_PY="venv/bin/python"
elif [ -x "venv/bin/python3" ]; then
  VENV_PY="venv/bin/python3"
else
  echo "❌ Virtual environment creation failed"
  exit 1
fi

# 4) Install dependencies
echo "📚 Installing dependencies..."
"$VENV_PY" -m pip install --upgrade pip
"$VENV_PY" -m pip install requests pandas scikit-learn numpy python-dotenv flask flask-cors

# 5) Check for .env file
if [ ! -f ".env" ]; then
  echo "⚠️  No .env file found!"
  echo "Please create a .env file with your YouTube API key:"
  echo "   YOUTUBE_API_KEY=your_api_key_here"
  echo ""
  echo "Get your API key at: https://console.developers.google.com/"
  echo ""
fi

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the application:"
echo "   ./start.sh          # Start web dashboard"
echo "   python run.py cli   # Start CLI mode"
echo "   python run.py --help # See all options"