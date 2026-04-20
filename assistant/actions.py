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

    # Web search
    if any(w in t for w in ["search", "google", "look up", "find", "browse"]):
        if "find file" not in t:
            query = re.sub(r"(search|google|look up|find|browse)\s+(for\s+)?", "", t).strip()
            return {"action": "web_search", "query": query}

    # File operations
    if "organize my downloads" in t or "clean my downloads" in t:
        return {"action": "organize_downloads"}
    if "find file" in t or "search for file" in t:
        filename = re.sub(r"(find file|search for file)\s+", "", t).strip()
        return {"action": "find_file", "filename": filename}

    # Advanced Placeholders
    if "email" in t:
        return {"action": "placeholder", "feature": "Email Management"}
    if "light" in t or "ac" in t or "fan" in t or "smart home" in t:
        return {"action": "placeholder", "feature": "Smart Home Integration"}

    # Time / Date / Weather / System / Screenshot / Notes / Power
    if "time" in t: return {"action": "get_time"}
    if "date" in t or "today" in t: return {"action": "get_date"}
    if "weather" in t:
        city = DEFAULT_CITY
        city_match = re.search(r"in ([a-zA-Z\s]+)$", t)
        if city_match: city = city_match.group(1).strip()
        return {"action": "weather", "city": city}
    if any(w in t for w in ["battery", "cpu", "ram"]): return {"action": "system_info"}
    if "screenshot" in t: return {"action": "screenshot"}
    if t.startswith("remember") or "note" in t:
        if "read" in t or "my" in t: return {"action": "read_notes"}
        note = re.sub(r"(remember\s+(that\s+)?|make a note\s+(that\s+)?|note that\s+)", "", t).strip()
        return {"action": "save_note", "note": note}
    if "volume" in t:
        direction = "up" if "up" in t or "increase" in t else "down" if "down" in t or "decrease" in t else "mute"
        return {"action": "volume", "direction": direction}
    if "shutdown" in t: return {"action": "shutdown"}
    if "restart" in t: return {"action": "restart"}

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
    
    if action == "open_app": return open_app(intent["cmd"], intent["app"])
    if action == "web_search": return web_search(intent["query"])
    if action == "organize_downloads": return organize_downloads()
    if action == "find_file": return find_file(intent["filename"])
    if action == "weather": return get_weather(intent["city"])
    if action == "get_time": return get_time()
    if action == "get_date": return get_date()
    if action == "system_info": return get_system_info()
    if action == "volume": return control_volume(intent["direction"])
    if action == "screenshot": return take_screenshot()
    if action == "save_note": return save_note(intent["note"])
    if action == "read_notes": return read_notes()
    if action == "shutdown": return shutdown()
    if action == "restart": return restart()
    return None

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

def shutdown(): subprocess.run("shutdown /s /t 10", shell=True); return "Shutting down in 10s."
def restart(): subprocess.run("shutdown /r /t 10", shell=True); return "Restarting in 10s."


def _load_notes() -> list:
    if NOTES_FILE.exists():
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return []


def _save_notes(notes: list):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=2)


def open_youtube(query: str) -> str:
    url = f"https://www.youtube.com/results?search_query={requests.utils.quote(query)}"
    webbrowser.open(url)
    return f"Searching YouTube for '{query}'."


def shutdown(delay: int = 0) -> str:
    if delay > 0:
        mins = delay // 60
        subprocess.run(f"shutdown /s /t {delay}", shell=True)
        return f"PC will shut down in {mins} minute(s). Say 'cancel shutdown' to abort."
    subprocess.run("shutdown /s /t 10", shell=True)
    return "Shutting down your PC in 10 seconds."


def restart() -> str:
    subprocess.run("shutdown /r /t 10", shell=True)
    return "Restarting your PC in 10 seconds."


def cancel_shutdown() -> str:
    subprocess.run("shutdown /a", shell=True)
    return "Shutdown cancelled."
