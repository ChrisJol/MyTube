# MyTube - Video Inspiration Finder 🎯

An intelligent YouTube video recommendation system that learns your preferences to suggest videos you'll love. Built with **Vue 3 + Flask API architecture**, machine learning, and featuring a modern reactive web dashboard.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![Vue](https://img.shields.io/badge/vue-v3.4+-green.svg)
![Node](https://img.shields.io/badge/node-v18+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)

## 🌟 Features

### 🎯 AI-Powered Recommendations

- 🔍 **Smart YouTube Search**: Automatically finds trending videos using configurable search queries
- 🤖 **Machine Learning**: RandomForest model learns your preferences from ratings
- 📊 **Confidence Scores**: See how confident the AI is about each recommendation
- 🎯 **Real-time Learning**: Model updates instantly as you rate more videos

### 🚀 Modern Architecture

- ⚡ **Vue 3 SPA**: Reactive frontend with component architecture
- 🔌 **Flask API**: Pure REST API backend with no template coupling
- 🛠️ **Modern Tooling**: Vite build system with hot reload
- 📱 **Responsive Design**: Works perfectly on desktop and mobile

### 🔒 Privacy & Control

- 🏠 **Local-First**: All data stored locally in SQLite - no external tracking
- ⚙️ **Configurable**: Customize search queries and ML parameters
- 🔧 **Flexible Deployment**: Single app or separate frontend/backend

## 🚀 Quick Start

### Prerequisites

- **Python 3.7+** and **Node.js 18+**
- **YouTube Data API v3 Key** (free from [Google Cloud Console](https://console.cloud.google.com/))

### Installation

```bash
git clone https://github.com/yourusername/mytube.git
cd mytube

# 1. Install Python dependencies
python app.py install

# 2. Install frontend dependencies
cd frontend && npm install && cd ..

# 3. Start the application
python app.py
```

The app will automatically:

1. Build the Vue 3 frontend if needed
2. Search for and load initial videos
3. Open your browser to the dashboard

## 🛠️ Development Modes

### **Production Mode** (Default)

```bash
python app.py
# → Serves built Vue SPA + Flask API
# → Single command, production-ready
```

### **Frontend Development** (Hot Reload)

```bash
cd frontend && npm run dev
# → http://localhost:3000 with instant updates
# → Auto-proxies API calls to Flask backend
# → Start Flask separately: python app.py --port 8000
```

### **Vue Development Mode**

```bash
python app.py dev
# → Vue development server with hot reload
# → Start Flask API separately: python app.py --port 8000

python app.py run --dev
# → Alternative way to start Vue dev server
```

## 🏗️ Architecture

### Modern Vue 3 + Flask API

```
MyTube/
├── frontend/                    # 🎯 Vue 3 Single Page Application
│   ├── src/
│   │   ├── App.vue             # Main Vue application
│   │   ├── main.js             # Vue app entry point
│   │   ├── components/         # Vue Single File Components
│   │   │   ├── AppHeader.vue   # Navigation header
│   │   │   ├── StatusBar.vue   # AI status display
│   │   │   ├── VideoGrid.vue   # Video container
│   │   │   ├── VideoCard.vue   # Individual video cards
│   │   │   └── ErrorDisplay.vue # Error handling
│   │   ├── api/                # API communication layer
│   │   ├── utils/              # Helper functions
│   │   └── css/                # Organized component styles
│   ├── dist/                   # Built assets (Flask serves these)
│   ├── package.json
│   └── vite.config.js          # Vite configuration
├── src/                        # 🔌 Pure Flask API Backend
│   ├── web/
│   │   ├── __init__.py         # Flask app factory
│   │   ├── config.py           # Flexible configuration
│   │   ├── routes/             # SPA serving routes
│   │   └── api/                # REST API endpoints
│   ├── ml/                     # Machine learning pipeline
│   ├── services/               # Business logic
│   └── database/               # Data operations
├── app.py                      # Main entry point
├── dev.py                      # Flexible development server
└── .env                        # Configuration
```

### Key Benefits

- **🔥 Hot Reload**: Vue development server with instant updates
- **🎯 Component Architecture**: Reusable, maintainable Vue components
- **🔌 API-First**: Backend is pure API, frontend consumes it
- **⚡ No Template Coupling**: Frontend and backend completely independent
- **🚀 Flexible Deployment**: Can deploy together or separately

## ⚙️ Configuration

1. **Get YouTube API Key**:

   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Create a project or select existing one
   - Enable YouTube Data API v3
   - Create credentials (API key)

2. **Set up environment**:

   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env and add your API key
   YOUTUBE_API_KEY=your_actual_api_key_here
   ```

3. **Customize your search queries**:
   - Edit `config/search_queries.json` to add search terms relevant to your interests
   - Example: `"python machine learning"`, `"react tutorial"`, etc.

## 🎨 Dashboard Features

### Vue 3 Reactive Interface

- **🎯 Smart Views**: Rate Videos vs MyTube (curated favorites)
- **⚡ Real-time Updates**: Reactive UI updates without page refreshes
- **🤖 AI Status Bar**: Live model training progress and confidence metrics
- **📱 Responsive Grid**: YouTube-like video cards that work on any device

### Advanced Features

- **🔥 Hot Reload Development**: Instant updates during development
- **🎨 Component Architecture**: Modular, reusable Vue components
- **🔔 Smart Notifications**: Toast notifications for user feedback
- **❌ Graceful Error Handling**: Different error states with helpful messages
- **🔄 Auto-refresh**: Keeps recommendations fresh automatically

## 🧠 How the AI Works

### Feature Engineering

The system extracts 11 key features from each video:

- **Content Features**: Title length, description length, keyword presence
- **Engagement Metrics**: View count, like ratio, engagement score
- **Semantic Analysis**: Title sentiment, tutorial/beginner/AI keyword detection
- **Behavioral Patterns**: Time constraints, challenge keywords

### Machine Learning Pipeline

1. **Data Collection**: YouTube API provides video metadata
2. **Feature Extraction**: Convert raw video data into numerical features
3. **User Feedback**: Collect like/dislike ratings with optional notes
4. **Model Training**: RandomForest classifier with 100 trees
5. **Prediction**: Generate confidence scores for new videos

### Learning Process

- **Cold Start**: Shows random videos until you have 10+ ratings
- **Warm Start**: AI model activates and provides personalized recommendations
- **Continuous Learning**: Model retrains after each new rating

## 🖥️ Available Commands

### Main Commands

```bash
# First-time setup (Python + Node.js dependencies)
python app.py install

# Start complete application (default)
python app.py
# → Builds Vue frontend if needed
# → Starts Flask API server
# → Opens browser automatically

# Search for additional videos (optional)
python app.py search

# Custom Flask options
python app.py --port 3000 --debug --no-browser
```

### Development Commands

```bash
# Vue development (hot reload)
python app.py dev                  # Vue dev server only
python app.py run --dev           # Alternative Vue dev mode

# Production with build options
python app.py run --build         # Force rebuild frontend
python app.py run --port 9000     # Custom port

# Frontend development (direct)
cd frontend
npm run dev        # Vue dev server with hot reload
npm run build      # Build for production
npm run preview    # Preview production build
npm run lint       # Check code quality
```

## 🚀 Deployment Options

### **Option 1: Monolithic (Current)**

```bash
python app.py
# → Single command serves both Vue SPA and Flask API
# → Perfect for local development and simple deployment
```

### **Option 2: Separate Deployment (Future)**

```bash
# Frontend: Deploy to CDN/Static hosting (Vercel, Netlify)
cd frontend && npm run build
# → Deploy dist/ folder to static hosting

# Backend: Deploy to API server (Railway, Heroku)
# → Deploy Flask API independently
# → Update frontend API URLs
```

### **Option 3: Containerized**

```dockerfile
# Dockerfile example for complete app
FROM node:18 AS frontend
COPY frontend/ /app/frontend/
RUN cd /app/frontend && npm install && npm run build

FROM python:3.9
COPY . /app/
COPY --from=frontend /app/frontend/dist /app/frontend/dist
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
```

## 🔧 Customization

### Search Queries

Edit the search queries in `config/search_queries.json`:

```json
{
  "search_queries": [
    "python machine learning tutorial",
    "javascript react project",
    "web development 2024",
    "coding interview prep",
    "system design tutorial",
    "database optimization"
  ]
}
```

The system intelligently uses different queries for different purposes:

- **Initial search**: Uses the first few queries when the app starts
- **More videos**: Uses remaining queries when you need more videos to rate
- **Smart rotation**: Automatically avoids repeating the same searches

### ML Model Parameters

Modify model settings in `src/ml/model_training.py`:

```python
model = RandomForestClassifier(
    n_estimators=100,        # Number of trees
    max_depth=10,           # Tree depth
    min_samples_split=5,    # Minimum samples for split
    random_state=42
)
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** and test thoroughly
4. **Commit your changes**: `git commit -m 'Add amazing feature'`
5. **Push to the branch**: `git push origin feature/amazing-feature`
6. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/mytube.git
cd mytube

# Backend setup
python app.py install

# Frontend setup
cd frontend
npm install
cd ..

# Start development environment
python3 dev.py --mode dev
# → Starts both Vue dev server (hot reload) and Flask API
```

### Vue 3 Component Development

```vue
<!-- Example: Creating a new component -->
<template>
  <div class="my-component">
    <h2>{{ title }}</h2>
    <button @click="handleClick">{{ buttonText }}</button>
  </div>
</template>

<script>
import { ref } from "vue";

export default {
  name: "MyComponent",
  props: ["title"],
  emits: ["custom-event"],
  setup(props, { emit }) {
    const buttonText = ref("Click me");

    const handleClick = () => {
      emit("custom-event", { message: "Hello from component!" });
    };

    return { buttonText, handleClick };
  },
};
</script>
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Vue 3** for the reactive frontend framework
- **Vite** for the lightning-fast build system
- **Flask** for the clean API backend
- **YouTube Data API v3** for video data
- **scikit-learn** for machine learning capabilities
- **SQLite** for local data storage

## 📚 Learn More

This project demonstrates several key concepts:

### **Frontend Development**

- **Vue 3 Composition API**: Modern reactive programming
- **Component Architecture**: Reusable, maintainable UI components
- **Modern Build Tools**: Vite with hot reload and optimization
- **SPA Development**: Single Page Application patterns

### **Backend Development**

- **API Design**: RESTful Flask API architecture
- **Machine Learning**: Feature engineering and model training
- **Database Design**: SQLite schema and operations

### **Full-Stack Integration**

- **API Integration**: Frontend-backend communication
- **Development Workflow**: Hot reload, build processes, deployment
- **Modern Architecture**: Separation of concerns, scalable structure

Perfect for learning about **modern full-stack development** with ML-powered features!

## 🐛 Troubleshooting

### Common Issues

**Frontend Build Issues**:

```bash
# Frontend not building
cd frontend && npm install && npm run build

# Vue dev server not starting
cd frontend && npm run dev
# → Check if port 3000 is available
```

**Backend Issues**:

```bash
# Virtual environment issues
python app.py install  # Recreates venv and installs dependencies

# API key issues
# → Ensure YouTube API key is valid in .env file
# → Check quota remaining in Google Cloud Console
```

**Development Server Issues**:

```bash
# Vue dev server not starting
python app.py dev  # Start Vue development server

# Port conflicts
python app.py --port 9000  # Use different port
```

**Database Issues**:

```bash
# Reset database
rm video_inspiration.db
python app.py  # Will recreate and populate database
```

### Architecture Questions

**"Why do I need Node.js for a Python app?"**

- Frontend is now a Vue 3 SPA that needs to be built
- Node.js is only needed for frontend development and building
- Production deployment can serve pre-built assets

**"Can I deploy frontend and backend separately?"**

- Yes! Frontend builds to static files that can be deployed anywhere
- Backend is a pure API that can run independently
- See deployment options section above

### Need Help?

- 📧 Open an issue on GitHub
- 💬 Check existing issues for solutions
- 🔍 Review the troubleshooting section above
- 📖 Check the Vue 3 and Flask documentation

---

⭐ **Found this helpful? Give it a star!** ⭐

Built with ❤️ for the coding community
