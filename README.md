# FRIDAY — Your Personal AI Assistant

> **F**ast **R**esponsive **I**ntelligent **D**igital **A**ssistant for **Y**ou  
> *Inspired by Tony Stark's FRIDAY from the Iron Man films*

---

## 🚀 Quick Start

### Step 1: Install dependencies
```bash
cd project-friday
pip install -r requirements.txt
```

> **Note on PyAudio (Windows)**: If `pyaudio` fails to install, run:
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

### Step 2: Get your FREE Gemini API Key
1. Go to [https://aistudio.google.com/](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click **"Get API key"** → **"Create API key"**
4. Copy the key

### Step 3: Run FRIDAY
```bash
python main.py
```

On first run, you'll be prompted to paste your Gemini API key. It will be saved automatically.

The browser will open at **http://localhost:5000** with the holographic UI.

---

## 🎤 How to Use

### Voice Commands
Say **"Hey Friday"** followed by your command:
- *"Hey Friday, open Chrome"*
- *"Hey Friday, what's the weather?"*
- *"Hey Friday, take a screenshot"*

### Text Commands
Type in the chat box and press Enter or click Send.

### Quick Command Buttons
Click any button in the left panel for instant actions.

---

## 🧠 Capabilities

| Feature | Example Commands |
|---------|-----------------|
| **AI Conversation** | "Who invented the internet?", "Write me a poem" |
| **Open Apps** | "Open Chrome", "Launch Calculator", "Open VS Code" |
| **Web Search** | "Search for Python tutorials", "Google ISRO" |
| **YouTube** | "Search YouTube for lo-fi music" |
| **Wikipedia** | "Who is Nikola Tesla?", "What is quantum computing?" |
| **Time & Date** | "What time is it?", "What's today's date?" |
| **Weather** | "What's the weather in Mumbai?" |
| **System Stats** | "CPU usage", "Battery status", "RAM info" |
| **Volume** | "Turn up volume", "Mute", "Lower volume" |
| **Screenshot** | "Take a screenshot" |
| **Notes** | "Remember I have a meeting at 3pm", "My notes" |
| **Shutdown** | "Shutdown my PC", "Restart" |
| **Memory** | "Clear memory" |

---

## 📁 Project Structure

```
project-friday/
├── main.py                  # Entry point
├── requirements.txt
├── .env                     # Your API keys (auto-created)
├── .env.example             # Template
├── assistant/
│   ├── brain.py             # Gemini AI integration
│   ├── voice.py             # Speech recognition + TTS
│   ├── actions.py           # Windows system commands
│   └── config.py            # Settings management
├── web/
│   ├── app.py               # Flask + SocketIO server
│   ├── templates/index.html # JARVIS-style UI
│   └── static/
│       ├── style.css
│       └── script.js
└── data/
    ├── memory.json          # Conversation history
    └── notes.json           # Saved notes
```

---

## ⚙️ Optional: Weather API

For live weather, get a free key from [openweathermap.org](https://openweathermap.org/api) and add it to `.env`:
```
WEATHER_API_KEY=your_key_here
DEFAULT_CITY=New Delhi
```

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| PyAudio install fails | Use `pipwin install pyaudio` |
| No microphone detected | Voice input disabled, text input still works |
| Gemini API error | Check your API key in `.env` |
| Port 5000 in use | Add `WEB_PORT=5001` to `.env` |

---

*Built with ❤️ — Powered by Google Gemini*
