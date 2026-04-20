# FRIDAY AI Assistant — Quick Start Guide

## 🚀 Installation (5 minutes)

### Step 1: Install Python Dependencies
```bash
# Navigate to project folder
cd C:\Users\SIDHARTH\OneDrive\Desktop\project-friday

# Run installer
python install.py
```

Choose option **1** for full installation (includes API key setup and Windows configuration).

### Step 2: Get API Keys

#### Google Gemini API (Required)
1. Go to: https://aistudio.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

#### OpenWeather API (Optional, for weather)
1. Go to: https://openweathermap.org/api
2. Sign up (free account)
3. Go to API keys section
4. Copy your API key

### Step 3: Configure API Keys
During `install.py`, you'll be prompted to paste these keys. Or edit `.env` file:
```
GEMINI_API_KEY=your_gemini_key_here
OPENWEATHER_API_KEY=your_openweather_key_here
```

### Step 4: Start FRIDAY
```bash
python background_service.py
```

You'll see:
- System tray icon appears (right side of taskbar)
- Web server starts
- Global hotkey registered

## 💡 Using FRIDAY

### Method 1: Global Hotkey (Easiest)
```
Press: Ctrl+Alt+F (from anywhere on your computer)
```
Then speak your command!

### Method 2: System Tray Icon
Right-click the system tray icon → "🎙️ Voice Command"

### Method 3: Web Interface
Open browser: http://localhost:5000
- Click microphone button for voice
- Type in chat box for text
- Use tabs for calendar, notes, settings

## 🎤 Example Voice Commands

```
"What's the weather?"
→ Tells you current weather and temperature

"System status"
→ Shows CPU, RAM, and temperature

"Add event tomorrow at 2pm: Team meeting"
→ Adds to calendar

"Take a note: Remember to call John"
→ Saves note

"Open Chrome"
→ Launches Chrome browser

"What are my upcoming events?"
→ Lists next 24 hours events

"Search my notes for budget"
→ Finds notes containing "budget"

"Create automation: Morning briefing"
→ Sets up automatic morning report

"Switch to professional mode"
→ Changes AI personality

"Clear memory"
→ Forgets previous conversation
```

## 📊 Web UI Tabs

### 🏠 Dashboard
- Real-time system stats (CPU, RAM, Disk, Temp)
- Current time and date
- Battery status

### 🎙️ Voice Chat
- Microphone button for voice commands
- Text input for typing
- Conversation history
- Status indicator

### 📅 Calendar
- View all events
- Add new events
- Delete events
- Color-coded by priority

### 📝 Notes
- Create/save notes with tags
- Full-text search
- Tag-based search
- Quick access to recent notes

### ⚙️ Settings
- Change AI personality
- Configure API keys
- Enable/disable features
- View logs

### 🤖 Automations
- Create custom automations
- Set triggers and actions
- Enable/disable automations
- Monitor automation history

## 🖥️ Windows Integration Features

### Auto-Start on Boot
FRIDAY will automatically start when you boot Windows (after setup).

### System Tray Access
- Minimize to tray instead of closing
- Quick access from taskbar
- Right-click for options

### Global Hotkey
- **Ctrl+Alt+F** - Works from ANY window
- Voice command activation
- Doesn't interfere with other apps

### Desktop Shortcut
- Created during setup
- Quick launch FRIDAY
- Pin to Start menu if desired

## 🔧 Advanced Usage

### Accessing the Database
Notes, calendar events, and automations are saved in:
- `data/notes.json`
- `data/calendar_events.json`
- `data/automations.json`

You can manually edit these JSON files or use the web UI.

### Using REST API Directly
The web server exposes REST APIs:

```bash
# Get weather
curl http://localhost:5000/api/weather?city=London

# Get all notes
curl http://localhost:5000/api/notes

# Get system status
curl http://localhost:5000/api/system/status

# Add a note
curl -X POST http://localhost:5000/api/notes \
  -H "Content-Type: application/json" \
  -d '{"title":"Meeting", "content":"...", "tags":["work"]}'
```

### Extending with Plugins
Add custom plugins in `plugins/` folder and import in `main.py`

## ❓ Troubleshooting

### "API key not found" error
- Check `.env` file exists in project root
- Verify GEMINI_API_KEY is set correctly
- Reinstall: `python install.py` → option 3

### Microphone not working
- Check microphone is connected
- Go to Windows Settings → Sound → Check recording devices
- Try installing: `pip install --upgrade pyaudio`

### Hotkey not working
- Run as Administrator (right-click python.exe)
- Check if Ctrl+Alt+F is used by another app
- Try a different hotkey (edit background_service.py line 66)

### System tray icon not showing
- Windows 11 hides tray icons by default
- Right-click taskbar clock → Taskbar settings → System tray
- Unhide FRIDAY

### Web UI shows "Connection Refused"
- Make sure `background_service.py` is still running
- Check port 5000 isn't in use: `netstat -ano | findstr :5000`
- Restart the service

### Voice commands not understood
- Speak clearly and naturally
- Try simpler commands first
- Check microphone volume
- Try the web UI chat box instead

## 📞 Getting Help

1. Check logs: `logs/friday_service.log`
2. Test API directly: `curl http://localhost:5000/api/health`
3. Verify all dependencies: `pip list | findstr friday`

## 🎯 Next Steps

1. ✅ Install and run FRIDAY
2. ✅ Test voice command (Ctrl+Alt+F)
3. ✅ Try different personalities
4. ✅ Create some calendar events
5. ✅ Explore web UI
6. ✅ Create automations
7. ✅ Add it to Windows startup (if you like it!)

## 💾 Backup Important Data

Important files to backup:
```
- data/notes.json
- data/calendar_events.json
- data/automations.json
- .env (contains API keys)
```

---

**Need more help?** See `README_ENHANCED.md` for complete documentation.

**Ready to go?** Press `Ctrl+Alt+F` and start commanding! 🚀
