# MyTube Frontend

Modern vanilla JavaScript frontend with Vite build system for the MyTube video recommendation application.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm (or yarn/pnpm)

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server with hot reload
npm run dev
```

The development server will start on `http://localhost:3000` with:
- ✅ Hot reload for instant updates
- ✅ Proxy to Flask backend on `http://localhost:8000`
- ✅ Modern ES6+ features
- ✅ CSS preprocessing

### Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

Built files will be output to `dist/` directory, which Flask serves automatically.

## 📁 Project Structure

```
frontend/
├── src/
│   ├── js/
│   │   ├── main.js              # Application entry point
│   │   ├── api/
│   │   │   └── videos.js        # API communication layer
│   │   ├── components/
│   │   │   ├── VideoCard.js     # Video card component
│   │   │   ├── StatusBar.js     # Status bar component
│   │   │   ├── ViewSwitcher.js  # View navigation component
│   │   │   └── ErrorHandler.js  # Error display component
│   │   └── utils/
│   │       ├── helpers.js       # Utility functions
│   │       └── notifications.js # Notification system
│   ├── css/
│   │   ├── main.css            # CSS entry point
│   │   ├── base/
│   │   │   ├── variables.css   # CSS custom properties
│   │   │   └── reset.css       # CSS reset/normalize
│   │   └── components/
│   │       ├── header.css      # Header component styles
│   │       ├── status-bar.css  # Status bar styles
│   │       ├── video-card.css  # Video card styles
│   │       └── layout.css      # Layout and grid styles
│   └── index.html              # Development HTML template
├── dist/                       # Built files (auto-generated)
├── package.json
├── vite.config.js             # Vite configuration
└── eslint.config.js           # ESLint configuration
```

## 🛠️ Development Workflow

### 1. Frontend Development
```bash
cd frontend
npm run dev
```
- Frontend runs on `http://localhost:3000`
- Auto-proxies API calls to Flask backend
- Hot reload for instant feedback

### 2. Backend Development
```bash
# In project root
python app.py
```
- Flask backend runs on `http://localhost:8000`
- Serves API endpoints and built frontend assets

### 3. Production Build
```bash
cd frontend
npm run build
```
- Builds optimized assets to `dist/`
- Flask automatically serves these files

## 🎯 Key Features

### Modern Development Experience
- **ES6 Modules**: Clean, organized code structure
- **Hot Reload**: Instant updates during development
- **Component Architecture**: Reusable, maintainable components
- **CSS Variables**: Consistent theming system
- **ESLint**: Code quality and consistency

### Component System
- **VideoCard**: Handles video display and rating interactions
- **StatusBar**: Shows AI model status and learning progress
- **ViewSwitcher**: Manages navigation between views
- **ErrorHandler**: Displays different error states gracefully

### API Integration
- **Async/Await**: Modern promise handling
- **Error Handling**: Comprehensive error management
- **Notifications**: User feedback system

## 🔧 Configuration

### Vite Configuration (`vite.config.js`)
- **Proxy Setup**: Routes `/api/*` to Flask backend
- **Build Output**: Configured for Flask integration
- **CSS Processing**: PostCSS with Autoprefixer

### ESLint Configuration (`eslint.config.js`)
- **Modern JavaScript**: ES2022 features
- **Browser Globals**: Window, document, fetch, etc.
- **Code Quality**: Consistent formatting and best practices

## 🚀 Deployment

The frontend builds to static files that Flask serves directly:

1. **Build**: `npm run build` creates optimized assets
2. **Flask Integration**: Built files are served from `dist/`
3. **Single Command**: `python app.py` runs the complete application

## 🔄 Migration from Inline Code

This frontend replaces the previous inline HTML/CSS/JS with:
- ✅ **400+ lines of CSS** → Organized component files
- ✅ **400+ lines of JavaScript** → ES6 modules with proper structure
- ✅ **Single HTML file** → Clean template with build integration
- ✅ **No build process** → Modern tooling with hot reload

## 📚 Next Steps

### Potential Enhancements
- **TypeScript**: Add type safety
- **Testing**: Unit tests with Vitest
- **PWA**: Progressive Web App features
- **Framework Migration**: Easy path to React/Vue if needed

### Framework Migration Path
The component architecture makes it easy to migrate to a framework later:
- Components are already modular
- API layer is separate
- CSS is organized and reusable
- Build system is framework-agnostic
