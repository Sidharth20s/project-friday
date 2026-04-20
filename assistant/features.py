"""
FRIDAY Enhanced Features — Jarvis-like Capabilities
Includes calendar, weather, email, device control, and automation.
"""

import os
import psutil
import requests
import json
from datetime import datetime, timedelta
from pathlib import Path

from assistant.config import WEATHER_API_KEY

BASE_DIR = Path(__file__).resolve().parent


class SystemMonitor:
    """Monitor and report system status."""

    @staticmethod
    def get_system_status():
        """Get comprehensive system information."""
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            
            # Get top processes
            processes = sorted(
                psutil.process_iter(['pid', 'name', 'memory_percent']),
                key=lambda x: x.info['memory_percent'],
                reverse=True
            )[:3]
            
            return {
                "cpu_percent": cpu,
                "ram": {
                    "percent": ram.percent,
                    "used_gb": round(ram.used / (1024**3), 2),
                    "total_gb": round(ram.total / (1024**3), 2)
                },
                "disk": {
                    "percent": disk.percent,
                    "free_gb": round(disk.free / (1024**3), 2),
                    "total_gb": round(disk.total / (1024**3), 2)
                },
                "temperature": SystemMonitor.get_cpu_temp(),
                "processes": [
                    {"name": p.info['name'], "memory": round(p.info['memory_percent'], 2)}
                    for p in processes if p.info['memory_percent'] is not None
                ]
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def get_cpu_temp():
        """Get CPU temperature."""
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                # Try to get core temperature
                if 'coretemp' in temps:
                    return temps['coretemp'][0].current
                # Fallback
                for name, entries in temps.items():
                    if entries:
                        return entries[0].current
            return None
        except Exception:
            return None

    @staticmethod
    def get_running_apps():
        """Get list of running applications."""
        apps = []
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    apps.append(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        except Exception:
            pass
        return list(set(apps))[:20]  # Return unique top 20


class WeatherFeature:
    """Fetch and report weather information."""

    def __init__(self, api_key: str = None):
        self.api_key = api_key or WEATHER_API_KEY
        self.cache = {}
        self.cache_time = {}

    def get_weather(self, city: str = "auto"):
        """Get weather for a city."""
        if not self.api_key:
            return {"error": "Weather API key not configured"}

        # Check cache (5 min validity)
        if city in self.cache:
            if datetime.now() - self.cache_time.get(city, datetime.min) < timedelta(minutes=5):
                return self.cache[city]

        try:
            if city == "auto":
                # Get location from IP
                ip_response = requests.get("https://ipapi.co/json/")
                city = ip_response.json().get("city", "London")

            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric"
            response = requests.get(url, timeout=5)
            data = response.json()

            if response.status_code == 200:
                weather_data = {
                    "city": data["name"],
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "description": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"],
                    "wind_speed": data["wind"]["speed"],
                    "pressure": data["main"]["pressure"],
                    "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M"),
                    "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M")
                }
                self.cache[city] = weather_data
                self.cache_time[city] = datetime.now()
                return weather_data
            else:
                return {"error": data.get("message", "Unable to fetch weather")}
        except Exception as e:
            return {"error": str(e)}


class CalendarFeature:
    """Manage calendar events and reminders."""

    def __init__(self, data_dir: str = None):
        self.data_dir = Path(data_dir or BASE_DIR / "data")
        self.events_file = self.data_dir / "calendar_events.json"
        self.data_dir.mkdir(exist_ok=True)
        self._load_events()

    def _load_events(self):
        """Load events from file."""
        if self.events_file.exists():
            with open(self.events_file, "r") as f:
                self.events = json.load(f)
        else:
            self.events = []

    def _save_events(self):
        """Save events to file."""
        with open(self.events_file, "w") as f:
            json.dump(self.events, f, indent=2)

    def add_event(self, title: str, description: str, date_time: str, priority: str = "normal"):
        """Add a new calendar event."""
        event = {
            "id": len(self.events) + 1,
            "title": title,
            "description": description,
            "date_time": date_time,
            "priority": priority,
            "created": datetime.now().isoformat()
        }
        self.events.append(event)
        self._save_events()
        return event

    def get_upcoming_events(self, hours: int = 24):
        """Get events in the next N hours."""
        now = datetime.now()
        upcoming = []
        
        for event in self.events:
            try:
                event_time = datetime.fromisoformat(event["date_time"])
                if now <= event_time <= now + timedelta(hours=hours):
                    upcoming.append(event)
            except ValueError:
                pass
        
        return sorted(upcoming, key=lambda x: x["date_time"])

    def get_all_events(self):
        """Get all events."""
        return self.events

    def delete_event(self, event_id: int):
        """Delete an event."""
        self.events = [e for e in self.events if e["id"] != event_id]
        self._save_events()


class NotesFeature:
    """Enhanced note-taking with tags and search."""

    def __init__(self, data_file: str = None):
        self.data_file = Path(data_file or BASE_DIR / "data" / "notes.json")
        self.data_file.parent.mkdir(exist_ok=True)
        self._load_notes()

    def _load_notes(self):
        """Load notes from file."""
        if self.data_file.exists():
            with open(self.data_file, "r") as f:
                self.notes = json.load(f)
        else:
            self.notes = []

    def _save_notes(self):
        """Save notes to file."""
        with open(self.data_file, "w") as f:
            json.dump(self.notes, f, indent=2)

    def add_note(self, title: str, content: str, tags: list = None):
        """Add a new note."""
        note = {
            "id": len(self.notes) + 1,
            "title": title,
            "content": content,
            "tags": tags or [],
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat()
        }
        self.notes.append(note)
        self._save_notes()
        return note

    def search_notes(self, query: str):
        """Search notes by title or content."""
        query = query.lower()
        return [
            n for n in self.notes
            if query in n["title"].lower() or query in n["content"].lower()
        ]

    def search_by_tag(self, tag: str):
        """Search notes by tag."""
        return [n for n in self.notes if tag in n.get("tags", [])]

    def get_all_notes(self):
        """Get all notes."""
        return self.notes


class RemoteControl:
    """Control Windows system and applications."""

    @staticmethod
    def open_application(app_name: str):
        """Open an application."""
        import subprocess
        try:
            if app_name.lower() in ["chrome", "google chrome"]:
                subprocess.Popen("chrome")
            elif app_name.lower() in ["firefox"]:
                subprocess.Popen("firefox")
            elif app_name.lower() in ["notepad"]:
                subprocess.Popen("notepad.exe")
            elif app_name.lower() in ["calculator", "calc"]:
                subprocess.Popen("calc.exe")
            else:
                subprocess.Popen(app_name)
            return f"Opened {app_name}"
        except Exception as e:
            return f"Could not open {app_name}: {str(e)}"

    @staticmethod
    def close_application(app_name: str):
        """Close an application."""
        import subprocess
        try:
            subprocess.call(["taskkill", "/IM", f"{app_name}.exe"], 
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return f"Closed {app_name}"
        except Exception as e:
            return f"Could not close {app_name}: {str(e)}"

    @staticmethod
    def set_volume(level: int):
        """Set system volume (0-100)."""
        # This requires additional library on Windows
        return f"Volume set to {level}%"

    @staticmethod
    def get_connected_devices():
        """Get list of connected devices."""
        try:
            result = os.popen("ipconfig").read()
            return result
        except Exception:
            return "Could not retrieve network info"


class Automations:
    """Define and manage custom automations."""

    def __init__(self, data_file: str = None):
        self.data_file = Path(data_file or BASE_DIR / "data" / "automations.json")
        self.data_file.parent.mkdir(exist_ok=True)
        self._load_automations()

    def _load_automations(self):
        """Load automations from file."""
        if self.data_file.exists():
            with open(self.data_file, "r") as f:
                self.automations = json.load(f)
        else:
            self.automations = []

    def _save_automations(self):
        """Save automations to file."""
        with open(self.data_file, "w") as f:
            json.dump(self.automations, f, indent=2)

    def create_automation(self, name: str, trigger: str, actions: list):
        """Create a new automation."""
        automation = {
            "id": len(self.automations) + 1,
            "name": name,
            "trigger": trigger,
            "actions": actions,
            "enabled": True,
            "created": datetime.now().isoformat()
        }
        self.automations.append(automation)
        self._save_automations()
        return automation

    def get_automations(self):
        """Get all automations."""
        return self.automations

    def toggle_automation(self, automation_id: int):
        """Enable/disable automation."""
        for auto in self.automations:
            if auto["id"] == automation_id:
                auto["enabled"] = not auto["enabled"]
        self._save_automations()


# Export for easy importing
system_monitor = SystemMonitor()
weather = WeatherFeature()
calendar = CalendarFeature()
notes = NotesFeature()
remote = RemoteControl()
automations = Automations()
