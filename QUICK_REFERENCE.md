# FRIDAY v2.0 - Quick Reference Guide

## 🎤 Voice Commands Quick List

### Search & Web (5)
| Command | Example | Result |
|---------|---------|--------|
| YouTube | "Play on YouTube..." | Open YouTube search |
| News | "Get news about AI" | Show news headlines |
| Translate | "Translate hello to Spanish" | Translation result |
| Define | "What's the meaning of..." | Word definition |
| Search | "Google Python tutorials" | Web search |

### Files (5)
| Command | Example | Result |
|---------|---------|--------|
| Create | "Create file notes.txt" | File created |
| Read | "Read file notes.txt" | File content displayed |
| Delete | "Delete file notes.txt" | File deleted |
| Organize | "Organize my downloads" | Downloads organized |
| Find | "Find file project" | File search results |

### System (10)
| Command | Example | Result |
|---------|---------|--------|
| Lock | "Lock my computer" | Screen locked |
| Battery | "Check battery" | Battery % shown |
| Shutdown | "Shutdown in 5 mins" | PC shuts down |
| Restart | "Restart" | PC restarts |
| Close App | "Close Chrome" | App closes |
| Volume | "Volume up" / "Mute" | Volume adjusted |
| Screenshot | "Take a screenshot" | Screenshot taken |
| CPU/RAM | "System status" | System info shown |
| Battery | "Battery status" | Battery info |
| Apps | "Show running apps" | List of apps |

### Memory (3)
| Command | Example | Result |
|---------|---------|--------|
| Remember | "Remember meeting at 3pm" | Fact stored |
| Forget | "Forget about meeting" | Fact removed |
| List | "What do you know?" | Stored facts listed |

### Calendar (4)
| Command | Example | Result |
|---------|---------|--------|
| View Events | "What's on my calendar?" | Events displayed |
| Upcoming | "Show upcoming events" | Next 24h events |
| Add Event | "Create event tomorrow at 2pm" | Event created |
| Reminder | "Set reminder for Friday" | Reminder set |

### Productivity (5)
| Command | Example | Result |
|---------|---------|--------|
| Timer | "Set timer for 10 mins" | Timer starts |
| Alarm | "Set alarm for 7am" | Alarm set |
| Calendar | "Open calendar" | Calendar shown |
| Add Event | "Create an event" | Event dialog |
| Notes | "Take a note: ..." | Note saved |

### Information (10)
| Command | Example | Result |
|---------|---------|--------|
| Weather | "What's the weather?" | Weather data |
| Forecast | "Get forecast" | 5-day forecast |
| Calculate | "Calculate 25 * 4" | = 100 |
| Joke | "Tell me a joke" | Joke told |
| Fact | "Share a fact" | Fact shared |
| Convert | "Convert 100 miles to km" | Conversion result |
| Wikipedia | "Who is Albert Einstein?" | Bio displayed |
| Time | "What time is it?" | Time shown |
| Date | "What's today's date?" | Date shown |
| Device | "Show connected devices" | Devices listed |

### Media (5)
| Command | Example | Result |
|---------|---------|--------|
| Play | "Play music" | Music starts |
| Pause | "Pause the music" | Music paused |
| Next | "Skip to next track" | Next song plays |
| Identify | "What song is playing?" | Song name shown |
| Movies | "Recommend a movie" | Movie suggested |

### Automation (4)
| Command | Example | Result |
|---------|---------|--------|
| Workflow | "Create workflow" | Workflow dialog |
| Record | "Record macro" | Recording starts |
| Stop | "Stop recording" | Recording stops |
| Play | "Play macro" | Macro executes |

### Apps & Programs (10)
| Command | Example | Result |
|---------|---------|--------|
| Chrome | "Open Chrome" | Chrome opens |
| Firefox | "Open Firefox" | Firefox opens |
| Edge | "Open Edge" | Edge opens |
| Notepad | "Open Notepad" | Notepad opens |
| Calculator | "Open Calculator" | Calculator opens |
| Paint | "Open Paint" | Paint opens |
| Word | "Open Word" | Word opens |
| Excel | "Open Excel" | Excel opens |
| PowerPoint | "Open PowerPoint" | PowerPoint opens |
| Discord | "Open Discord" | Discord opens |

---

## 🌐 REST API Quick Reference

### Base URL
```
http://localhost:5051
```

### Health Check
```bash
GET /api/health
curl http://localhost:5051/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-04-20T15:30:00",
  "version": "2.0.0"
}
```

---

## 📊 System Endpoints

### Get System Status
```bash
GET /api/system/status
curl http://localhost:5051/api/system/status
```

**Response:**
```json
{
  "cpu_percent": 25.5,
  "memory": {
    "percent": 60,
    "used_gb": 12.5,
    "total_gb": 16
  },
  "disk": {
    "percent": 45,
    "used_gb": 450,
    "total_gb": 1000,
    "free_gb": 550
  },
  "temperature": 65
}
```

### Get Running Apps
```bash
GET /api/system/processes
curl http://localhost:5051/api/system/processes
```

**Response:**
```json
{
  "applications": [
    "chrome.exe",
    "code.exe",
    "notepad.exe",
    "python.exe"
  ]
}
```

---

## 🌤️ Weather Endpoints

### Get Weather
```bash
GET /api/weather?city=London
curl "http://localhost:5051/api/weather?city=London"
```

**Response:**
```json
{
  "city": "London",
  "temp": 15,
  "feels_like": 13,
  "description": "Cloudy",
  "humidity": 75,
  "wind_speed": 12,
  "pressure": 1013,
  "sunrise": "06:30",
  "sunset": "20:45"
}
```

### Get Forecast
```bash
GET /api/weather/forecast?city=London
```

---

## 📅 Calendar Endpoints

### Get All Events
```bash
GET /api/calendar/events
curl http://localhost:5051/api/calendar/events
```

### Get Upcoming Events
```bash
GET /api/calendar/upcoming?hours=24
curl http://localhost:5051/api/calendar/upcoming?hours=24
```

### Create Event
```bash
POST /api/calendar/event
curl -X POST http://localhost:5051/api/calendar/event \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Team Meeting",
    "date_time": "2026-04-21T14:00:00",
    "description": "Weekly sync",
    "priority": "normal"
  }'
```

### Delete Event
```bash
DELETE /api/calendar/event/1
curl -X DELETE http://localhost:5051/api/calendar/event/1
```

---

## 📝 Notes Endpoints

### Get All Notes
```bash
GET /api/notes
curl http://localhost:5051/api/notes
```

### Search Notes
```bash
GET /api/notes/search?q=important
curl http://localhost:5051/api/notes/search?q=important
```

### Search by Tag
```bash
GET /api/notes/tag?tag=work
curl http://localhost:5051/api/notes/tag?tag=work
```

### Create Note
```bash
POST /api/notes
curl -X POST http://localhost:5051/api/notes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Project Ideas",
    "content": "AI assistant enhancements",
    "tags": ["ideas", "project"]
  }'
```

---

## 🤖 Automation Endpoints

### Get All Automations
```bash
GET /api/automations
curl http://localhost:5051/api/automations
```

### Create Automation
```bash
POST /api/automations
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

### Toggle Automation
```bash
PUT /api/automations/1/toggle
curl -X PUT http://localhost:5051/api/automations/1/toggle
```

---

## 🚀 App Control Endpoints

### Open Application
```bash
POST /api/app/open
curl -X POST http://localhost:5051/api/app/open \
  -H "Content-Type: application/json" \
  -d '{"app_name": "chrome"}'
```

### Close Application
```bash
POST /api/app/close
curl -X POST http://localhost:5051/api/app/close \
  -H "Content-Type: application/json" \
  -d '{"app_name": "chrome"}'
```

---

## 🖥️ GUI Features

### Launching
```bash
python main.py
```

### System Tray
- Right-click icon → "Show FRIDAY"
- Right-click icon → "Quit"

### Window
- Minimize button → Hides to tray
- Close button → Hides to tray
- Restore from tray → Right-click icon

### Web UI
- Access at http://localhost:5051
- All features available
- Real-time updates

---

## 🎯 Common Use Cases

### Set Up Morning Routine
```bash
# 1. Create calendar event
curl -X POST http://localhost:5051/api/calendar/event \
  -d '{"title":"Morning Meeting","date_time":"2026-04-21T09:00:00"}'

# 2. Create automation
curl -X POST http://localhost:5051/api/automations \
  -d '{"name":"Morning","trigger":"07:00 AM",...}'

# 3. Use voice command
"Hey Friday, what's on my schedule?"
```

### Productivity Session
```bash
# Via voice
"Set a timer for 25 minutes"
"Take a note: Project deadline Friday"
"Show my calendar"
"Open VS Code"

# Or via API
curl -X POST http://localhost:5051/api/notes \
  -d '{"title":"Deadline","tags":["project"]}'
```

### Monitor System
```bash
# Via API
curl http://localhost:5051/api/system/status

# Via voice
"System status"
"What's my CPU usage?"
"Check battery"
```

---

## 🔄 Request/Response Format

### Standard Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Operation completed",
  "timestamp": "2026-04-20T15:30:00Z"
}
```

### Standard Error Response
```json
{
  "success": false,
  "error": "Error description",
  "message": "Failed to complete operation",
  "code": 400
}
```

---

## ⚙️ Configuration Quick Reference

### .env Settings
```env
# Required
GEMINI_API_KEY=your_key_here

# Optional
OPENWEATHER_API_KEY=your_key_here
WEB_PORT=5051
DEFAULT_CITY=New Delhi
VOICE_SPEED=175
VOICE_VOLUME=1.0
```

---

## 📱 Platform Support

| Feature | Windows | Mac | Linux |
|---------|---------|-----|-------|
| Voice | ✅ | ✅ | ✅ |
| GUI | ✅ | ⚠️ | ⚠️ |
| Tray | ✅ | ✅ | ✅ |
| API | ✅ | ✅ | ✅ |
| System Commands | ✅ | ⚠️ | ⚠️ |

*✅ = Fully supported | ⚠️ = Partial support*

---

## 🚀 Performance Tips

1. **Voice Commands**
   - Speak clearly
   - Use natural language
   - Say "Hey Friday" first

2. **API Performance**
   - Use specific queries
   - Limit result sets
   - Cache results locally

3. **System Performance**
   - Close unused apps
   - Ensure 4GB+ RAM
   - Use SSD storage

4. **Network**
   - Use wired connection for stability
   - Ensure good WiFi signal
   - Check internet speed

---

## 🐛 Debugging

### Check Logs
```bash
cat logs/friday_service.log
```

### Test API Health
```bash
curl http://localhost:5051/api/health
```

### Check Dependencies
```bash
pip list | grep -E "PyQt6|pystray|gemini"
```

### Verify Services
```bash
# Check if port 5051 is listening
netstat -an | findstr :5051

# Check if process running
tasklist | findstr python
```

---

## 📚 Additional Resources

- **Documentation**: See README_V2.md
- **Full Analysis**: See VERSION_2_ANALYSIS.md
- **Changes**: See CHANGELOG.md
- **API Docs**: See web/api.py

---

## 💡 Tips & Tricks

1. **Use Aliases**
   - "Chrome" = "Google Chrome"
   - "Calc" = "Calculator"
   - "VS Code" = "VSCode"

2. **Combine Commands**
   - "Open Chrome and search YouTube for..."
   - "Set a timer and take a note..."

3. **Use Automations**
   - Schedule regular tasks
   - Create morning/evening routines
   - Set reminders

4. **API Automation**
   - Create scripts to control FRIDAY
   - Integrate with other tools
   - Build custom workflows

---

## 🎓 Learning Path

1. **Beginner**: Use voice commands (Ctrl+Alt+F)
2. **Intermediate**: Use web UI (http://localhost:5051)
3. **Advanced**: Use REST API (curl/programming)
4. **Expert**: Create custom automations & plugins

---

## 🆘 Quick Troubleshooting

| Issue | Quick Fix |
|-------|-----------|
| Command not understood | Repeat clearly |
| API returns error | Check logs |
| GUI won't start | `pip install PyQt6` |
| No microphone | Check Windows Sound settings |
| Port conflict | Change WEB_PORT in .env |
| API timeout | Restart service |

---

**FRIDAY v2.0 Quick Reference** | Last Updated: April 20, 2026

*For detailed info, see README_V2.md or VERSION_2_ANALYSIS.md*
