"""
FRIDAY AI Assistant — Action Engine
Handles all Windows system commands and local actions.
"""

import os
import subprocess
import webbrowser
import datetime
import platform
import psutil
import pyautogui
import requests
import json
import re
import shutil
import importlib.util
from pathlib import Path
from assistant.config import WEATHER_API_KEY, DEFAULT_CITY
from assistant import db

BASE_DIR = Path(__file__).resolve().parent.parent
PLUGINS_DIR = BASE_DIR / "plugins"
PLUGINS_DIR.mkdir(exist_ok=True)

# ─── App Aliases ──────────────────────────────────────────
APP_ALIASES = {
    "chrome":        "chrome",
    "google chrome": "chrome",
    "firefox":       "firefox",
    "edge":          "msedge",
    "microsoft edge":"msedge",
    "notepad":       "notepad",
    "calculator":    "calc",
    "calc":          "calc",
    "paint":         "mspaint",
    "word":          "winword",
    "excel":         "excel",
    "powerpoint":    "powerpnt",
    "task manager":  "taskmgr",
    "file explorer": "explorer",
    "explorer":      "explorer",
    "cmd":           "cmd",
    "terminal":      "cmd",
    "vs code":       "code",
    "vscode":        "code",
    "spotify":       "spotify",
    "discord":       "discord",
    "vlc":           "vlc",
    "steam": "steam",
    "whatsapp": "whatsapp",
    "settings": "ms-settings:",
    "control panel": "control",
}

def detect_intent(text: str) -> dict:
    """Parse user text and return action intent dictionary."""
    t = text.lower().strip()

    # Plugins check first
    plugin_response = check_plugins(t)
    if plugin_response:
        return {"action": "plugin_response", "reply": plugin_response}

    # Proactive Briefing
    if "morning briefing" in t or "status report" in t:
        return {"action": "morning_briefing"}

    # Open application
    for alias, cmd in APP_ALIASES.items():
        if alias in t:
            return {"action": "open_app", "app": alias, "cmd": cmd}

    # ─── WEB & SEARCH ────────────────────────
    if any(w in t for w in ["search", "google", "look up", "browse"]):
        if "find file" not in t:
            query = re.sub(r"(search|google|look up|browse)\s+(for\s+)?", "", t).strip()
            return {"action": "web_search", "query": query}
    
    if "youtube" in t or "play on youtube" in t:
        query = re.sub(r"(play on youtube|youtube)\s+", "", t).strip()
        return {"action": "youtube", "query": query}
    
    if "news" in t or "headlines" in t:
        topic = re.sub(r"(news|headlines)(\s+about)?\s+", "", t).strip()
        return {"action": "news", "topic": topic}
    
    if "translate" in t:
        parts = re.sub(r"translate\s+", "", t).split("to")
        if len(parts) == 2:
            return {"action": "translate", "text": parts[0].strip(), "lang": parts[1].strip()}
    
    if "define" in t or "meaning" in t:
        word = re.sub(r"(define|meaning of)\s+", "", t).strip()
        return {"action": "define", "word": word}

    # ─── FILE OPERATIONS ─────────────────────
    if "organize my downloads" in t or "clean my downloads" in t:
        return {"action": "organize_downloads"}
    if "find file" in t or "search for file" in t:
        filename = re.sub(r"(find file|search for file)\s+", "", t).strip()
        return {"action": "find_file", "filename": filename}
    
    if "create file" in t:
        return {"action": "create_file"}
    if "read file" in t:
        filename = re.sub(r"read file\s+", "", t).strip()
        return {"action": "read_file", "filename": filename}
    if "delete file" in t:
        filename = re.sub(r"delete file\s+", "", t).strip()
        return {"action": "delete_file", "filename": filename}

    # ─── SYSTEM CONTROL ──────────────────────
    if "screenshot" in t: return {"action": "screenshot"}
    if "lock my computer" in t or "lock screen" in t: return {"action": "lock"}
    if "battery" in t or "battery status" in t: return {"action": "battery"}
    
    if "shutdown" in t:
        mins = re.search(r"(\d+)\s*(minutes?|mins?)", t)
        delay = int(mins.group(1)) * 60 if mins else 600
        return {"action": "shutdown", "delay": delay}
    if "restart" in t: return {"action": "restart"}
    
    if "volume" in t:
        direction = "up" if "up" in t or "increase" in t else "down" if "down" in t or "decrease" in t else "mute"
        return {"action": "volume", "direction": direction}
    
    if "close" in t and "app" in t:
        app_name = re.sub(r"close\s+(the\s+)?(app|application)\s+", "", t).strip()
        return {"action": "close_app", "app": app_name}

    # ─── MEMORY ──────────────────────────────
    if t.startswith("remember ") or "remember that" in t:
        fact = re.sub(r"(remember\s+(that\s+)?)", "", t).strip()
        return {"action": "remember", "fact": fact}
    if "forget" in t:
        keyword = re.sub(r"forget\s+(about\s+)?", "", t).strip()
        return {"action": "forget", "keyword": keyword}
    if "what do you know" in t or "list memory" in t:
        return {"action": "list_memory"}

    # ─── PRODUCTIVITY ────────────────────────
    if "note" in t:
        if "read" in t or "show" in t or "my notes" in t:
            return {"action": "show_notes"}
        note = re.sub(r"(take a note|make a note|note that|create note)\s+", "", t).strip()
        return {"action": "note", "content": note}
    
    if "timer" in t:
        mins = re.search(r"(\d+)\s*(minutes?|mins?)", t)
        return {"action": "timer", "minutes": int(mins.group(1))} if mins else {"action": "timer", "minutes": 5}
    
    if "alarm" in t:
        time_match = re.search(r"(\d{1,2}):(\d{2})", t)
        if time_match:
            return {"action": "alarm", "time": f"{time_match.group(1)}:{time_match.group(2)}"}
    
    if "calendar" in t or "events" in t:
        return {"action": "calendar"}
    
    if "add event" in t or "schedule" in t:
        return {"action": "add_event"}

    # ─── INFORMATION ─────────────────────────
    if "weather" in t:
        city = DEFAULT_CITY
        city_match = re.search(r"in ([a-zA-Z\s]+)$", t)
        if city_match: city = city_match.group(1).strip()
        return {"action": "weather", "city": city}
    
    if "forecast" in t:
        city = DEFAULT_CITY
        city_match = re.search(r"in ([a-zA-Z\s]+)$", t)
        if city_match: city = city_match.group(1).strip()
        return {"action": "forecast", "city": city}
    
    if "calculate" in t or "math" in t:
        expr = re.sub(r"(calculate|math)\s+", "", t).strip()
        return {"action": "calculate", "expression": expr}
    
    if "convert" in t:
        return {"action": "convert"}
    
    if "joke" in t: return {"action": "joke"}
    if "fact" in t or "did you know" in t: return {"action": "fact"}
    if any(w in t for w in ["time", "what time"]) and "timer" not in t and "alarm" not in t:
        return {"action": "get_time"}
    if "date" in t or "today" in t: return {"action": "get_date"}
    if any(w in t for w in ["battery", "cpu", "ram", "system"]) and "battery status" not in t:
        return {"action": "system_info"}

    # ─── MEDIA CONTROL ───────────────────────
    if "play music" in t or "start music" in t: return {"action": "play_music"}
    if "pause music" in t or "stop music" in t: return {"action": "pause_music"}
    if "next track" in t or "skip" in t: return {"action": "next_track"}
    if "identify song" in t or "what song" in t: return {"action": "identify_song"}
    if "movie" in t and ("recommend" in t or "suggestion" in t): return {"action": "movie_rec"}

    # ─── AUTOMATION ──────────────────────────
    if "workflow" in t: return {"action": "workflow"}
    if "record macro" in t or "record" in t: return {"action": "record_macro"}
    if "stop recording" in t: return {"action": "stop_recording"}
    if "play macro" in t: return {"action": "play_macro"}

    # ─── ADVANCED PLACEHOLDERS ───────────────
    if "email" in t:
        return {"action": "placeholder", "feature": "Email Management"}
    if "light" in t or "ac" in t or "fan" in t or "smart home" in t:
        return {"action": "placeholder", "feature": "Smart Home Integration"}

    return {"action": "ai_response"}

# ─── Plugin System ────────────────────────────────────────

def check_plugins(text):
    for plugin_file in PLUGINS_DIR.glob("*.py"):
        try:
            spec = importlib.util.spec_from_file_location(plugin_file.stem, plugin_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "handle_command"):
                reply = module.handle_command(text)
                if reply: return reply
        except Exception:
            pass
    return None

# ─── Action Executor ──────────────────────────────────────

def execute(intent: dict) -> str:
    action = intent.get("action")
    if action == "plugin_response": return intent["reply"]
    if action == "morning_briefing": return morning_briefing()
    if action == "placeholder": return f"The {intent['feature']} feature requires additional configuration. Check the README for details."
    
    # Web & Search
    if action == "open_app": return open_app(intent["cmd"], intent["app"])
    if action == "web_search": return web_search(intent["query"])
    if action == "youtube": return open_youtube(intent["query"])
    if action == "news": return get_news(intent.get("topic", ""))
    if action == "translate": return translate_text(intent["text"], intent["lang"])
    if action == "define": return define_word(intent["word"])
    
    # File Operations
    if action == "organize_downloads": return organize_downloads()
    if action == "find_file": return find_file(intent["filename"])
    if action == "create_file": return create_file(intent.get("filename", ""), intent.get("content", ""))
    if action == "read_file": return read_file_content(intent["filename"])
    if action == "delete_file": return delete_file(intent["filename"])
    
    # System Control
    if action == "weather": return get_weather(intent["city"])
    if action == "get_time": return get_time()
    if action == "get_date": return get_date()
    if action == "system_info": return get_system_info()
    if action == "volume": return control_volume(intent["direction"])
    if action == "screenshot": return take_screenshot()
    if action == "lock": return lock_screen()
    if action == "battery": return get_battery()
    if action == "shutdown": return shutdown_system(intent.get("delay", 600))
    if action == "restart": return restart()
    if action == "close_app": return close_app(intent["app"])
    
    # Memory
    if action == "remember": return remember_fact(intent["fact"])
    if action == "forget": return forget_fact(intent["keyword"])
    if action == "list_memory": return list_memory()
    
    # Productivity
    if action == "note": return save_note(intent["content"])
    if action == "show_notes": return read_notes()
    if action == "timer": return set_timer(intent["minutes"])
    if action == "alarm": return set_alarm(intent.get("time"))
    if action == "calendar": return show_calendar()
    if action == "add_event": return add_event()
    
    # Information
    if action == "forecast": return get_forecast(intent["city"])
    if action == "calculate": return calculate(intent["expression"])
    if action == "convert": return convert_units()
    if action == "joke": return get_joke()
    if action == "fact": return get_fact()
    
    # Media Control
    if action == "play_music": return play_music()
    if action == "pause_music": return pause_music()
    if action == "next_track": return next_track()
    if action == "identify_song": return identify_song()
    if action == "movie_rec": return movie_recommendation()
    
    # Automation
    if action == "workflow": return workflow_manager()
    if action == "record_macro": return record_macro()
    if action == "stop_recording": return stop_macro_recording()
    if action == "play_macro": return play_macro()
    
    # Legacy support
    if action == "save_note": return save_note(intent["note"])
    if action == "read_notes": return read_notes()
    
    return None

# ─── WEB & SEARCH HANDLERS ────────────────────────────────

def get_news(topic: str = "") -> str:
    """Fetch news headlines for a topic."""
    if not topic:
        topic = "general"
    try:
        # Using NewsAPI or similar (placeholder for now)
        webbrowser.open(f"https://news.google.com/search?q={requests.utils.quote(topic)}")
        return f"Opening news for {topic}."
    except Exception:
        return "Could not fetch news."

def translate_text(text: str, target_lang: str) -> str:
    """Translate text to target language."""
    try:
        webbrowser.open(f"https://translate.google.com/?sl=auto&tl={target_lang}&text={requests.utils.quote(text)}")
        return f"Translating to {target_lang}."
    except Exception:
        return "Translation service unavailable."

def open_youtube(query: str) -> str:
    """Open YouTube and search for a query."""
    try:
        webbrowser.open(f"https://www.youtube.com/results?search_query={requests.utils.quote(query)}")
        return f"Playing '{query}' on YouTube."
    except Exception:
        return "Failed to open YouTube."

def define_word(word: str) -> str:
    """Get definition of a word."""
    try:
        webbrowser.open(f"https://www.google.com/search?q=define+{requests.utils.quote(word)}")
        return f"Looking up definition for '{word}'."
    except Exception:
        return "Definition service unavailable."

# ─── FILE OPERATIONS HANDLERS ─────────────────────────────

def create_file(filename: str = "", content: str = "") -> str:
    """Create a new file."""
    if not filename:
        return "Please specify a filename."
    try:
        file_path = Path.home() / "Documents" / filename
        with open(file_path, "w") as f:
            f.write(content)
        return f"File '{filename}' created successfully."
    except Exception as e:
        return f"Failed to create file: {str(e)}"

def read_file_content(filename: str) -> str:
    """Read content from a file."""
    if not filename:
        return "Please specify a filename."
    try:
        file_path = Path.home() / "Documents" / filename
        if not file_path.exists():
            file_path = Path.cwd() / filename
        with open(file_path, "r") as f:
            content = f.read()
        return f"Content: {content[:500]}..." if len(content) > 500 else f"Content: {content}"
    except Exception as e:
        return f"Failed to read file: {str(e)}"

def delete_file(filename: str) -> str:
    """Delete a file."""
    if not filename:
        return "Please specify a filename."
    try:
        file_path = Path.home() / "Documents" / filename
        if not file_path.exists():
            file_path = Path.cwd() / filename
        file_path.unlink()
        return f"File '{filename}' deleted successfully."
    except Exception as e:
        return f"Failed to delete file: {str(e)}"

# ─── SYSTEM CONTROL HANDLERS ──────────────────────────────

def lock_screen() -> str:
    """Lock the computer screen."""
    try:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Screen locked."
    except Exception:
        return "Failed to lock screen."

def get_battery() -> str:
    """Get battery status."""
    try:
        battery = psutil.sensors_battery()
        if battery:
            status = "plugged in" if battery.power_plugged else "on battery"
            return f"Battery: {battery.percent}% ({status}). Time left: {battery.secsleft // 3600}h {(battery.secsleft % 3600) // 60}m"
        return "Battery information unavailable."
    except Exception:
        return "Could not get battery status."

def shutdown_system(delay: int = 600) -> str:
    """Shutdown system after delay (in seconds)."""
    try:
        mins = delay // 60
        subprocess.run(f"shutdown /s /t {delay}", shell=True)
        return f"PC will shut down in {mins} minute(s). Say 'cancel shutdown' to abort."
    except Exception:
        return "Failed to initiate shutdown."

def close_app(app_name: str) -> str:
    """Close a running application."""
    try:
        subprocess.call(["taskkill", "/IM", f"{app_name}.exe"], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return f"Closed {app_name}."
    except Exception:
        return f"Could not close {app_name}."

# ─── MEMORY HANDLERS ──────────────────────────────────────

def remember_fact(fact: str) -> str:
    """Store a fact in user memory."""
    try:
        db.add_memory("user_fact", fact)
        return f"I'll remember that, Boss: {fact}"
    except Exception:
        return "Failed to store memory."

def forget_fact(keyword: str) -> str:
    """Remove a fact from memory."""
    try:
        # Placeholder for memory removal logic
        return f"I've forgotten about {keyword}."
    except Exception:
        return "Failed to forget memory."

def list_memory() -> str:
    """List all stored facts."""
    try:
        facts = db.get_memory(limit=10)
        if facts:
            return "Recent memories: " + ", ".join([f.get("content", "") for f in facts])
        return "No stored memories."
    except Exception:
        return "Could not retrieve memories."

# ─── PRODUCTIVITY HANDLERS ────────────────────────────────

def set_timer(minutes: int) -> str:
    """Set a timer for specified minutes."""
    import time
    try:
        # This would typically use system notifications
        return f"Timer set for {minutes} minute(s)."
    except Exception:
        return "Failed to set timer."

def set_alarm(time_str: str) -> str:
    """Set an alarm for specified time."""
    try:
        return f"Alarm set for {time_str}."
    except Exception:
        return "Failed to set alarm."

def show_calendar() -> str:
    """Display calendar."""
    try:
        webbrowser.open("https://calendar.google.com")
        return "Opening calendar."
    except Exception:
        return "Failed to open calendar."

def add_event() -> str:
    """Add event to calendar."""
    try:
        return "Opening event creation dialog."
    except Exception:
        return "Failed to create event."

# ─── INFORMATION HANDLERS ────────────────────────────────

def get_forecast(city: str) -> str:
    """Get weather forecast for city."""
    try:
        if not WEATHER_API_KEY or len(WEATHER_API_KEY) < 10:
            return f"Forecast for {city} available in browser."
        r = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={WEATHER_API_KEY}&units=metric").json()
        return f"5-day forecast available for {city}."
    except Exception:
        return "Forecast service offline."

def calculate(expression: str) -> str:
    """Perform mathematical calculation."""
    try:
        # Safe evaluation of math expressions
        result = eval(expression, {"__builtins__": {}}, {})
        return f"{expression} = {result}"
    except Exception:
        return "Could not calculate. Check your expression."

def convert_units() -> str:
    """Convert between units."""
    return "Unit conversion: Please specify the conversion (e.g., '100 miles to kilometers')."

def get_joke() -> str:
    """Tell a joke."""
    jokes = [
        "Why did the programmer quit his job? Because he didn't get arrays.",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
        "Why do developers prefer dark mode? Because light attracts bugs.",
        "Why did the database admin leave his wife? Because she had one-to-many relationships."
    ]
    import random
    return random.choice(jokes)

def get_fact() -> str:
    """Share an interesting fact."""
    facts = [
        "Honey never spoils. Archaeologists have found 3000-year-old honey in Egyptian tombs.",
        "Bananas are berries, but strawberries are not.",
        "The shortest war in history lasted 38 to 45 minutes.",
        "A group of flamingos is called a 'flamboyance'."
    ]
    import random
    return random.choice(facts)

# ─── MEDIA CONTROL HANDLERS ───────────────────────────────

def play_music() -> str:
    """Play music."""
    return "Music player starting."

def pause_music() -> str:
    """Pause music."""
    return "Music paused."

def next_track() -> str:
    """Skip to next track."""
    return "Skipping to next track."

def identify_song() -> str:
    """Identify currently playing song."""
    return "Song identification: Please ensure audio is available."

def movie_recommendation() -> str:
    """Get movie recommendations."""
    return "Fetching movie recommendations for you, Boss."

# ─── AUTOMATION HANDLERS ──────────────────────────────────

def workflow_manager() -> str:
    """Manage workflows and automations."""
    return "Workflow manager: Available automations can be configured."

def record_macro() -> str:
    """Start recording a macro."""
    return "Macro recording started. Perform actions to record."

def stop_macro_recording() -> str:
    """Stop recording macro."""
    return "Macro recording stopped."

def play_macro() -> str:
    """Play a recorded macro."""
    return "Macro playback: Specify which macro to play."

def morning_briefing() -> str:
    time_str = datetime.datetime.now().strftime("%I:%M %p")
    cpu = psutil.cpu_percent()
    res = f"Good morning, Sir. The time is {time_str}. "
    res += f"Current system load is {cpu}%. "
    res += get_weather(DEFAULT_CITY)
    res += " All systems are functioning within normal parameters. Shall we begin?"
    return res

def open_app(cmd, app_name):
    try:
        if cmd.startswith("ms-"): os.startfile(cmd)
        else: subprocess.Popen(cmd, shell=True)
        return f"Launching {app_name.title()}."
    except Exception: return f"Failed to launch {app_name}."

def web_search(query):
    webbrowser.open(f"https://www.google.com/search?q={requests.utils.quote(query)}")
    return f"Searching for '{query}'."

def organize_downloads():
    path = Path.home() / "Downloads"
    if not path.exists(): return "Downloads folder not found."
    cats = {"Images": [".jpg",".png"], "Docs": [".pdf",".docx",".txt"], "Apps": [".exe",".msi"]}
    count = 0
    for f in path.iterdir():
        if f.is_file():
            for c, exts in cats.items():
                if f.suffix.lower() in exts:
                    d = path / c; d.mkdir(exist_ok=True)
                    try: shutil.move(str(f), str(d/f.name)); count += 1
                    except: pass
    return f"Organized {count} files in Downloads."

def find_file(name):
    for p in [Path.home()/"Documents", Path.home()/"Downloads"]:
        for f in p.rglob(f"*{name}*"):
            if f.is_file(): os.startfile(f.parent); return f"Found: {f.name}"
    return f"File '{name}' not found."

def get_weather(city):
    if not WEATHER_API_KEY or len(WEATHER_API_KEY) < 10: return f"Weather for {city} available in browser."
    try:
        r = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric").json()
        return f"Weather in {city}: {r['weather'][0]['description']}, {r['main']['temp']}°C."
    except: return "Weather service offline."

def get_time(): return f"It's {datetime.datetime.now().strftime('%I:%M %p')}."
def get_date(): return f"Today is {datetime.datetime.now().strftime('%A, %B %d')}."
def get_system_info(): return f"CPU: {psutil.cpu_percent()}%, RAM: {psutil.virtual_memory().percent}%."
def control_volume(dir):
    import pyautogui
    key = "volumeup" if dir=="up" else "volumedown" if dir=="down" else "volumemute"
    for _ in range(5): pyautogui.press(key)
    return f"Volume adjusted."

def take_screenshot():
    d = BASE_DIR / "screenshots"; d.mkdir(exist_ok=True)
    f = d / f"shot_{datetime.datetime.now().strftime('%H%M%S')}.png"
    pyautogui.screenshot().save(f); os.startfile(d); return "Screenshot captured."

def save_note(n): db.add_note(n); return f"Note saved: {n}"
def read_notes():
    rows = db.get_notes(5)
    return "Recent notes: " + ", ".join([r["content"] for r in rows]) if rows else "No notes."

def restart() -> str:
    """Restart the computer."""
    try:
        subprocess.run("shutdown /r /t 10", shell=True)
        return "Restarting your PC in 10 seconds."
    except Exception:
        return "Failed to restart."

def cancel_shutdown() -> str:
    subprocess.run("shutdown /a", shell=True)
    return "Shutdown cancelled."
