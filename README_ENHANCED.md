# FRIDAY AI Assistant — Enhanced Edition

> An advanced AI assistant for Windows 11 inspired by Jarvis from Iron Man. Runs as a background service with voice control, system integration, and Jarvis-like features.

## 🌟 Features

### Core AI
- **Gemini Integration** - Powered by Google's Gemini AI model
- **Voice Commands** - Natural language voice input with text-to-speech
- **Personality Modes** - Professional, Casual, or Sarcastic personalities
- **Conversation Memory** - SQLite-based persistent conversation history

### Background Service
- **System Tray Icon** - Quick access from system tray
- **Global Hotkey** - Press `Ctrl+Alt+F` from anywhere to activate voice command
- **Auto-start** - Automatically runs on Windows boot
- **Background Web Server** - Accessible via http://localhost:5000 even in background

### Jarvis-Like Features
- **System Monitoring** - Real-time CPU, RAM, disk, temperature monitoring
- **Weather Integration** - Fetch weather for any city using OpenWeather API
- **Calendar Management** - Add, view, and manage events and reminders
- **Advanced Notes** - Take notes with tags and full-text search
- **Application Control** - Open/close applications via voice
- **Automations** - Create custom automations and triggers
- **Device Status** - View connected devices, running applications

### Web Interface
- **Holographic UI** - Modern, responsive web interface
- **Real-time Updates** - WebSocket-based live updates
- **Voice Command Display** - See voice input/output in real-time
- **System Dashboard** - Comprehensive system information
- **Settings Panel** - Configure personality, API keys, automations

## 🚀 Quick Start

### 1. Install Dependencies
```bash
python install.py
```
Choose option 1 for full installation or run steps individually.

### 2. Configure API Keys
You'll need:
- **Google Gemini API Key** (required)
  - Get it from: https://aistudio.google.com/app/apikey
- **OpenWeather API Key** (optional, for weather)
  - Get it from: https://openweathermap.org/api

### 3. Run as Background Service
```bash
python background_service.py
```

This will:
- Start system tray icon
- Register global hotkey (Ctrl+Alt+F)
- Launch web server
- Start listening for commands

### 4. Access Web UI
Open browser: http://localhost:5000

## 📁 Project Structure

```
project-friday/
├── main.py                 # Original main entry point
├── background_service.py   # ⭐ Background service with tray icon
├── enhanced_brain.py       # ⭐ Enhanced AI with feature integration
├── install.py             # ⭐ One-click installer
├── setup_windows.py       # ⭐ Windows setup (auto-start, shortcuts)
├── requirements.txt       # Updated dependencies
├── assistant/
│   ├── brain.py           # Original AI brain (Gemini)
│   ├── enhanced_brain.py  # ⭐ New enhanced brain
│   ├── features.py        # ⭐ System monitoring, weather, calendar, etc.
│   ├── voice.py           # Voice input/output
│   ├── actions.py         # System actions
│   ├── config.py          # Configuration management
│   └── db.py              # SQLite memory storage
├── web/
│   ├── app.py             # Flask web server
│   ├── templates/
│   │   └── index.html     # Web UI
│   └── static/
│       ├── script.js      # Frontend logic
│       └── style.css      # Styling
├── data/
│   ├── notes.json         # Saved notes
│   ├── calendar_events.json
│   └── automations.json
└── plugins/
    └── hello_plugin.py    # Example plugin
```

## 🎯 Usage Examples

### Voice Commands
```
"What's the weather?" → Fetches current weather
"System status" → Shows CPU, RAM, temperature
"Add event tomorrow at 3pm" → Creates calendar event
"Take a note about..." → Saves a note
"Open Chrome" → Launches Chrome browser
"What are my upcoming events?" → Shows calendar
```

### Keyboard Shortcut
```
Press Ctrl+Alt+F → Activates voice listening
```

### Web Interface
- Dashboard: System metrics in real-time
- Voice Tab: Send voice commands
- Calendar: Manage events
- Notes: Create and search notes
- Settings: Configure personality and automations

## ⚙️ Configuration

### API Keys
Edit `.env` file in project root:
```
GEMINI_API_KEY=your_key_here
OPENWEATHER_API_KEY=your_key_here
```

### Personality
Switch via voice:
- "Switch to professional mode"
- "Switch to casual mode"
- "Switch to sarcastic mode"

### Auto-start Setup
Run setup after installation:
```bash
python setup_windows.py
```
Then select "Full Setup" to:
- Enable auto-start on boot
- Create desktop shortcut
- Register global hotkey

## 📦 New Dependencies Added

```
pystray>=0.19.5              # System tray icon
keyboard>=0.13.5             # Global hotkey support
pywin32>=305                 # Windows integration
```

## 🔧 Advanced Features

### Create Automations
```python
# In enhanced_brain.py or via API
brain.create_automation(
    name="Morning Briefing",
    trigger="08:00 AM",
    actions=[
        {"type": "voice", "text": "Good morning! Here's your briefing."},
        {"type": "weather"},
        {"type": "calendar", "hours": 24}
    ]
)
```

### Add Calendar Events
```python
brain.add_calendar_event(
    title="Team Meeting",
    datetime_str="2026-04-21T14:30:00",
    description="Weekly sync with team"
)
```

### Add Notes
```python
brain.add_note(
    title="Project Ideas",
    content="AI assistant features...",
    tags=["ideas", "project-friday"]
)
```

### System Monitoring
```python
status = system_monitor.get_system_status()
# Returns: cpu%, ram, disk, temperature, running processes
```

## 🛠️ Troubleshooting

### Hotkey not working
- Make sure you're running as Administrator
- Check if another app is using Ctrl+Alt+F
- Try a different hotkey by modifying `background_service.py`

### No audio input
- Check microphone is connected and enabled
- Install pyaudio: `pip install pyaudio`
- On Windows, you may need to install SAPI5

### API errors
- Verify API keys are correctly set in `.env`
- Check internet connection
- Ensure Gemini API key has sufficient quota

### System tray icon not showing
- Run as Administrator
- Windows 11 may hide tray icons by default
- Right-click taskbar clock → Taskbar settings → System tray to unhide

## 📋 Upcoming Features

- [ ] Email integration (Gmail API)
- [ ] Slack/Teams integration
- [ ] Smart home control (Philips Hue, etc.)
- [ ] Database queries via natural language
- [ ] Custom voice models
- [ ] Plugin marketplace
- [ ] Cross-platform support (Mac, Linux)
- [ ] Advanced NLP for better command understanding

## 🎓 Learning Resources

- **Gemini API**: https://ai.google.dev/
- **Flask SocketIO**: https://python-socketio.readthedocs.io/
- **PyAutoGUI**: https://pyautogui.readthedocs.io/

## 📝 Notes

- All data is stored locally (no cloud sync by default)
- Conversation history stored in SQLite
- System tray integration requires Windows 10+
- Global hotkey requires admin privileges on Windows 11

## 🤝 Contributing

To add new features:
1. Add feature class to `assistant/features.py`
2. Register in `enhanced_brain.py`
3. Add web UI component for that feature
4. Update documentation

## ⚖️ License

MIT License - Feel free to use and modify!

---

**Made with ❤️ - FRIDAY AI Assistant**

Press `Ctrl+Alt+F` to activate!
