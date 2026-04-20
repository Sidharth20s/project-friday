# FRIDAY AI Assistant - Version 2.0

> **F**ast **R**esponsive **I**ntelligent **D**igital **A**ssistant for **Y**ou  
> *Your Personal AI Companion - Now with Desktop GUI & 60+ Commands*

---

## 🎉 What's New in Version 2.0

### ✨ Major Features
- 🖥️ **Professional Desktop GUI** - Native Windows 11 application
- 🌐 **28 REST API Endpoints** - Programmatic access to all features
- 🔊 **60+ Voice Commands** - Expanded command library
- 📊 **Enhanced Voice Engine** - Better wake word detection
- 🎵 **Media Control** - Play, pause, skip music
- 💾 **Memory System** - Remember facts and information
- ⚙️ **Workflow Automation** - Record and playback macros
- 🧠 **Smart Features** - Calculator, translator, news, jokes

---

## 📥 Installation

### Quick Start (5 minutes)
```bash
# 1. Navigate to project
cd project-friday

# 2. Install dependencies
pip install -r requirements.txt
pip install PyQt6 PyQt6-WebEngine

# 3. Get API key
# Go to: https://aistudio.google.com/app/apikey
# Paste key when prompted

# 4. Run FRIDAY
python main.py
```

### What Happens
1. Desktop GUI window opens (1000x700)
2. Web server starts on port 5051
3. System tray icon appears
4. Ready for voice commands

---

## 🎤 How to Use

### Method 1: Voice Commands (Easiest)
```
Press: Ctrl+Alt+F (from anywhere on your PC)
Say your command
FRIDAY responds with voice + text
```

### Method 2: Web Interface
```
Open: http://localhost:5051
Use chat box for voice or text
View calendar, notes, settings
```

### Method 3: Desktop GUI
```
Click system tray icon
Click "Show FRIDAY"
Embedded web UI opens
```

### Method 4: REST API
```bash
curl http://localhost:5051/api/weather?city=London
curl http://localhost:5051/api/system/status
curl http://localhost:5051/api/health
```

---

## 🗣️ 60+ Voice Commands

### Web & Search (5 commands)
```
"Search YouTube for Jarvis"
"Find news about AI"
"Translate hello to Spanish"
"What's the definition of quantum?"
"Google Python tutorials"
```

### File Management (5 commands)
```
"Create a file named notes.txt"
"Read the file notes.txt"
"Delete the file notes.txt"
"Organize my downloads"
"Find file project-friday"
```

### System Control (10 commands)
```
"Lock my computer"
"Check battery status"
"Shutdown in 10 minutes"
"Restart the computer"
"Close Chrome"
"Mute audio"
"Volume up"
"Take a screenshot"
"System status"
"Get CPU info"
```

### Memory & Notes (6 commands)
```
"Remember that I have a meeting at 3pm"
"Forget about the meeting"
"What do you remember about me?"
"Take a note: Important deadline"
"Show my notes"
"Search my notes for budget"
```

### Calendar (4 commands)
```
"What's on my calendar?"
"Show upcoming events for today"
"Create event tomorrow at 2pm: Team meeting"
"Add reminder for Friday"
```

### Productivity (5 commands)
```
"Set a timer for 10 minutes"
"Set an alarm for 7am"
"Open calendar"
"Create an event"
"What time is it?"
```

### Information (10 commands)
```
"What's the weather?"
"Get the 5-day forecast"
"Calculate 25 * 4"
"Tell me a joke"
"Share an interesting fact"
"Convert 100 miles to kilometers"
"Who is Albert Einstein?"
"What's today's date?"
"Get battery percentage"
"Show running apps"
```

### Media Control (5 commands)
```
"Play music"
"Pause the music"
"Skip to next track"
"What song is playing?"
"Recommend a movie"
```

### System & Automation (10+ commands)
```
"Create workflow"
"Record macro"
"Stop recording"
"Play macro"
"Get system status"
"Show connected devices"
"Open Firefox"
"Open Notepad"
```

---

## 📊 API Endpoints

### Health Check
```
GET /api/health
→ Returns system status and version
```

### System Information
```
GET /api/system/status
→ CPU, RAM, disk, temperature

GET /api/system/processes
→ List of running applications
```

### Weather
```
GET /api/weather?city=London
→ Current weather data

GET /api/weather/forecast?city=London
→ Weather forecast
```

### Calendar
```
GET /api/calendar/events
→ All calendar events

GET /api/calendar/upcoming?hours=24
→ Events in next N hours

POST /api/calendar/event
→ Create new event

DELETE /api/calendar/event/<id>
→ Delete event
```

### Notes
```
GET /api/notes
→ All notes

GET /api/notes/search?q=important
→ Search notes

GET /api/notes/tag?tag=work
→ Filter by tag

POST /api/notes
→ Create new note
```

### Automations
```
GET /api/automations
→ All automations

POST /api/automations
→ Create automation

PUT /api/automations/<id>/toggle
→ Enable/disable automation
```

### Applications
```
POST /api/app/open
→ Open application

POST /api/app/close
→ Close application
```

---

## 🖥️ Desktop GUI Features

### Window
- 1000x700 professional interface
- Windows 11 native styling
- Embedded web browser
- Responsive layout

### System Tray
- Right-click menu
- "Show FRIDAY" option
- "Quit" option
- Always-visible icon

### Minimize Behavior
- Close button hides to tray (doesn't exit)
- Right-click tray icon to restore
- Stays running in background

### Integration
- Seamless web UI embedding
- Multi-threaded for responsiveness
- Proper error handling

---

## 📁 Project Structure (v2.0)

```
project-friday/
├── main.py                    # Main entry point
├── gui.py                     # ⭐ NEW: Desktop GUI
├── background_service.py      # Background service
│
├── assistant/
│   ├── brain.py
│   ├── actions.py             # ⭐ 60+ handlers
│   ├── features.py
│   ├── voice.py               # ⭐ Enhanced
│   ├── config.py
│   ├── db.py
│   └── __init__.py
│
├── web/
│   ├── app.py
│   ├── api.py                 # ⭐ NEW: 28 endpoints
│   ├── templates/
│   │   └── index.html
│   └── static/
│       ├── style.css
│       └── script.js
│
├── data/
│   ├── notes.json
│   ├── calendar_events.json
│   └── automations.json
│
├── VERSION_2_ANALYSIS.md      # ⭐ NEW: Analysis
├── CHANGELOG.md               # ⭐ NEW: Changes
└── requirements.txt
```

---

## ⚙️ Configuration

### .env File
```env
# API Keys (Required)
GEMINI_API_KEY=your_key_here
OPENWEATHER_API_KEY=your_key_here

# Server
WEB_PORT=5051
HOST=0.0.0.0

# Voice Settings
VOICE_SPEED=175
VOICE_VOLUME=1.0
WAKE_WORD=hey friday

# Features
DEFAULT_CITY=New Delhi
ENABLE_AUTOMATIONS=true
```

---

## 🚀 Advanced Usage

### Create Calendar Event via API
```bash
curl -X POST http://localhost:5051/api/calendar/event \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Meeting",
    "date_time": "2026-04-21T14:00:00",
    "description": "Weekly sync",
    "priority": "high"
  }'
```

### Add Note via API
```bash
curl -X POST http://localhost:5051/api/notes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Project Ideas",
    "content": "AI assistant enhancements",
    "tags": ["ideas", "project-friday"]
  }'
```

### Search Notes
```bash
curl http://localhost:5051/api/notes/search?q=important
curl http://localhost:5051/api/notes/tag?tag=work
```

### Create Automation
```bash
curl -X POST http://localhost:5051/api/automations \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Morning Briefing",
    "trigger": "08:00 AM",
    "actions": [
      {"type": "voice", "text": "Good morning!"},
      {"type": "weather"},
      {"type": "calendar", "hours": 24}
    ]
  }'
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| GUI won't launch | Install PyQt6: `pip install PyQt6 PyQt6-WebEngine` |
| Port 5051 in use | Change in .env: `WEB_PORT=5052` |
| Microphone not working | Check Windows Settings → Sound → Recording devices |
| API not responding | Verify server is running: `curl http://localhost:5051/api/health` |
| Wake word not detected | Try: "hey friday, what's the weather" |
| No sound output | Check Windows volume + speaker settings |

---

## 📈 Performance

### Resource Usage
- **Memory**: 250-400MB typical
- **CPU**: <5% idle (increases during voice processing)
- **Disk**: ~50MB code + data files
- **Network**: Minimal (only for APIs)

### Optimization Tips
1. Close unused applications
2. Disable unnecessary automations
3. Use wired network for better stability
4. Run with sufficient RAM (4GB+)

---

## 🔒 Privacy & Security

✅ **All data stored locally** - No cloud sync  
✅ **API keys in .env** - Not shared  
✅ **Conversation history** - SQLite local storage  
✅ **No telemetry** - No tracking  
✅ **Safe file operations** - Validated paths  

---

## 📚 Documentation Files

- **README.md** - This file
- **VERSION_2_ANALYSIS.md** - Complete feature analysis
- **CHANGELOG.md** - Detailed change log
- **QUICKSTART.md** - Quick start guide
- **DEVELOPER_GUIDE.md** - For extending FRIDAY

---

## 🎓 Learning Resources

- [Gemini API Docs](https://ai.google.dev/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PyQt6 Guide](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [REST API Best Practices](https://restfulapi.net/)

---

## 🎯 Quick Examples

### Example 1: Morning Briefing
```
User: "Ctrl+Alt+F"
FRIDAY: "Good morning! It's Monday, 7:00 AM"

User: "Weather"
FRIDAY: "It's 45°F and rainy. I've opened your calendar."

User: "What's on my schedule?"
FRIDAY: "You have a team meeting at 9 AM and lunch at 1 PM"
```

### Example 2: Work Session
```
User: "Ctrl+Alt+F"
FRIDAY: "Ready when you are!"

User: "Set a timer for 25 minutes"
FRIDAY: "Pomodoro timer started"

User: "Take a note: Deadline for project Friday"
FRIDAY: "Note saved with tag: work"

User: "Open VS Code"
FRIDAY: "Launching VS Code"
```

### Example 3: API Integration
```bash
#!/bin/bash
# Get system status
STATUS=$(curl -s http://localhost:5051/api/system/status)
echo "Current system: $STATUS"

# Add event
curl -X POST http://localhost:5051/api/calendar/event \
  -d '{"title":"Meeting","date_time":"2026-04-21T14:00:00"}'

# Check weather
WEATHER=$(curl -s "http://localhost:5051/api/weather?city=London")
echo "Weather: $WEATHER"
```

---

## 🌟 Version 2.0 Highlights

| Feature | Details |
|---------|---------|
| **Voice Commands** | 60+ available |
| **REST API** | 28 endpoints |
| **Desktop GUI** | PyQt6 + Tray |
| **File Management** | Create/Read/Delete |
| **Calendar** | Full management |
| **Notes** | With tags & search |
| **Weather** | Real-time data |
| **System Monitor** | CPU/RAM/Disk/Temp |
| **Memory** | Remember facts |
| **Automations** | Custom workflows |
| **Media** | Play/Pause/Skip |
| **Smart Features** | Jokes, facts, translator |

---

## 🚀 Getting Started

### Step 1: Install
```bash
cd project-friday
pip install -r requirements.txt
pip install PyQt6 PyQt6-WebEngine
```

### Step 2: Configure
```bash
python install.py
# Follow prompts for API keys
```

### Step 3: Run
```bash
python main.py
# Desktop GUI launches automatically
```

### Step 4: Try It!
```
Press Ctrl+Alt+F and say a command
Or visit http://localhost:5051
Or use REST API with curl
```

---

## 💬 Example Commands to Try

```
"Hey Friday, open Chrome"
"What's the weather?"
"Set a timer for 10 minutes"
"Take a note: Remember to call John"
"System status"
"Tell me a joke"
"Translate hello to Spanish"
"Create event tomorrow: Meeting"
"Show my calendar"
```

---

## 🎓 Support & Community

For issues or questions:
1. Check [QUICKSTART.md](QUICKSTART.md)
2. Review [CHANGELOG.md](CHANGELOG.md)
3. Check logs: `logs/friday_service.log`
4. Test API: `curl http://localhost:5051/api/health`

---

## 📝 Version History

- **v2.0** (April 2026) - Major enhancement, GUI, 60+ commands, REST API
- **v1.0** (Earlier) - Initial release with basic commands

---

## ✨ What's Next?

**Version 2.1 (Coming Soon)**
- Email integration
- Slack/Teams chatbot
- Enhanced macros
- Smart home devices

---

**FRIDAY v2.0 - Your Personal AI Assistant** 🤖  
*Always listening, always ready to help*

Made with ❤️ - April 2026

---

*Need help? Press Ctrl+Alt+F to activate FRIDAY anytime!*
