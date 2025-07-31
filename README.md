# 🎬 YouTube Video Downloader

A full-stack YouTube video downloader with a clean, modern interface. Paste any YouTube URL to get video details and download options in multiple formats.

## ✨ Features

- 🎥 **Video Preview**: See video title, duration, and thumbnail before downloading
- 📹 **Multiple Formats**: Download videos in various MP4 qualities  
- ⚡ **Fast Processing**: Built with Django REST API and yt-dlp
- 📱 **Responsive Design**: Clean UI with Tailwind CSS v4
- � **Auto Cleanup**: Downloaded files are automatically removed after 24 hours
- 🛡️ **Error Handling**: Robust error handling for invalid URLs and network issues

## 🛠 Tech Stack

**Frontend:**
- React 19 with Vite
- Tailwind CSS v4
- React Router DOM

**Backend:**
- Django 5.1.6 with Django REST Framework
- yt-dlp for video extraction
- CORS headers for cross-origin requests
- SQLite database

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/elxecutor/elxtract.git
cd elxtract/backend
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Python dependencies**
```bash
pip install django djangorestframework django-cors-headers yt-dlp python-dotenv
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Start the Django server**
```bash
python manage.py runserver
```

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd ../frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start development server**
```bash
npm run dev
```

### Quick Start with VS Code Tasks

If using VS Code, you can use the predefined tasks:
- `Ctrl+Shift+P` → "Tasks: Run Task" → "Run Django Backend"
- `Ctrl+Shift+P` → "Tasks: Run Task" → "Run Vite Frontend"

## 🚀 Usage

1. **Start both servers** (backend on :8000, frontend on :5173)
2. **Open your browser** to `http://localhost:5173`
3. **Paste a YouTube URL** in the input field
4. **Click "Get Format"** to see video details and available download options
5. **Choose your preferred format** and click "Download"

### Example URLs to test:
```
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://youtu.be/jNQXAC9IVRw
```

## 📁 Project Structure

```
elxtract/
├── backend/                 # Django REST API
│   ├── backend/            # Django project settings
│   ├── core/               # Main app with video processing
│   │   ├── models.py       # Database models
│   │   ├── views.py        # API endpoints
│   │   └── urls.py         # URL routing
│   ├── media/downloads/    # Temporary download storage
│   └── manage.py           # Django management script
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # React components
│   │   └── main.jsx        # Application entry point
│   ├── public/            # Static assets
│   └── package.json       # Frontend dependencies
└── README.md              # This file
```

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/formats/` | Get video details and available formats |
| POST | `/api/download/` | Download video in specified format |
| POST | `/api/cleanup/` | Manual cleanup of old files |

### API Usage Examples

**Get video formats:**
```bash
curl -X POST http://localhost:8000/api/formats/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

**Download video:**
```bash
curl -X POST http://localhost:8000/api/download/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "format_id": "18"}'
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the backend directory:
```env
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
AUTO_CLEANUP_ENABLED=True
CLEANUP_DOWNLOADS_AFTER_HOURS=24
```

### Frontend Configuration

The frontend is configured to work with the backend on `localhost:8000`. If you need to change this, update the API calls in `src/components/Body.jsx`.

## 🔍 Troubleshooting

### Common Issues

**Backend not starting:**
- Ensure Python virtual environment is activated
- Install missing dependencies: `pip install django djangorestframework django-cors-headers yt-dlp python-dotenv`
- Run migrations: `python manage.py migrate`

**Frontend not loading:**
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check if port 5173 is available

**CORS errors:**
- Ensure django-cors-headers is installed and configured
- Check that frontend URL is allowed in Django settings

**Download failures:**
- Video might be private, restricted, or removed
- Try updating yt-dlp: `pip install --upgrade yt-dlp`
- Check internet connection and firewall settings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m "Add feature"`
5. Push to the branch: `git push origin feature-name`
6. Open a Pull Request

## 📋 To-Do

- [ ] Add audio-only download (MP3/M4A)
- [ ] Implement download progress tracking
- [ ] Add batch download functionality
- [ ] Create Docker containerization
- [ ] Add user authentication
- [ ] Implement download history
- [ ] Add dark mode toggle

## ⚠️ Legal Notice

This tool is for educational and personal use only. Please respect YouTube's Terms of Service and copyright laws. Users are responsible for ensuring they have the right to download content.

## � Bug Reports

Found a bug? Please create an issue with:
- Steps to reproduce
- Expected vs actual behavior
- Browser and OS information
- Error messages (if any)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.



