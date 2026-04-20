"""
FRIDAY Enhanced Brain — Advanced AI with Feature Integration
Integrates calendar, weather, notes, automations, and system control.
"""

import datetime
import json
from pathlib import Path
import google.generativeai as genai

from assistant.config import GEMINI_API_KEY, ASSISTANT_NAME
from assistant import db
from assistant.features import (
    system_monitor, weather, calendar, notes,
    remote, automations
)

# System instruction template
SYSTEM_TEMPLATE = """You are {name}, an advanced AI assistant inspired by Jarvis from Iron Man.
Today's date and time: {datetime}

CAPABILITIES:
- You can access system information (CPU, RAM, temperature)
- You can fetch weather reports
- You can manage calendar events and reminders
- You can take and search notes
- You can control applications and system functions
- You can create and manage automations
- You can access running applications

When a user asks about system status, weather, calendar, or other features, provide the most relevant information.
Keep responses concise (under 3 sentences) unless asked for more detail.
Maintain a professional but slightly witty tone, like Tony Stark's FRIDAY.
"""

class EnhancedFridayBrain:
    """Advanced brain with feature integration and contextual awareness."""

    def __init__(self):
        self.model = None
        self.chat = None
        self.personality = db.get_setting("personality", "sarcastic")
        self.features = {
            "system": system_monitor,
            "weather": weather,
            "calendar": calendar,
            "notes": notes,
            "remote": remote,
            "automations": automations,
        }
        self._init_gemini()

    def _init_gemini(self):
        """Initialize Gemini with enhanced system instruction."""
        if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
            raise ValueError("Gemini API key not configured. Run setup first.")

        genai.configure(api_key=GEMINI_API_KEY)

        system_instruction = SYSTEM_TEMPLATE.format(
            name=ASSISTANT_NAME,
            datetime=datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
        )

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-latest",
            system_instruction=system_instruction
        )
        self.chat = self.model.start_chat(history=self._format_history_for_gemini())

    def _format_history_for_gemini(self) -> list:
        """Convert conversation history for Gemini."""
        history = db.get_history(limit=20)
        formatted = []
        for entry in history:
            formatted.append({"role": entry["role"], "parts": [entry["text"]]})
        return formatted

    def _process_feature_request(self, text: str) -> str:
        """Detect and process feature requests."""
        text_lower = text.lower()

        # System status
        if any(phrase in text_lower for phrase in ["system status", "how's my system", "cpu usage", "memory usage", "temperature"]):
            status = system_monitor.get_system_status()
            return f"System Status: CPU {status['cpu_percent']}%, RAM {status['ram']['percent']}%, Temp {status['temperature']}°C"

        # Weather
        if any(phrase in text_lower for phrase in ["weather", "temperature", "forecast", "sunny", "rainy"]):
            city = self._extract_city(text)
            weather_data = weather.get_weather(city)
            if "error" not in weather_data:
                return f"Weather in {weather_data['city']}: {weather_data['temperature']}°C, {weather_data['description']}"
            return str(weather_data)

        # Calendar events
        if any(phrase in text_lower for phrase in ["upcoming events", "my calendar", "next event", "schedule"]):
            events = calendar.get_upcoming_events()
            if events:
                return f"Upcoming events: {events[0]['title']} at {events[0]['date_time']}"
            return "No upcoming events"

        # Notes
        if "note" in text_lower:
            if "search" in text_lower or "find" in text_lower:
                query = text.replace("search notes", "").replace("find note", "").strip()
                results = notes.search_notes(query)
                if results:
                    return f"Found {len(results)} note(s): {results[0]['title']}"
                return "No notes found"

        # Running apps
        if "running" in text_lower and "app" in text_lower:
            apps = system_monitor.get_running_apps()
            return f"Running applications: {', '.join(apps[:5])}..."

        return None

    def _extract_city(self, text: str) -> str:
        """Extract city name from text."""
        # Simple extraction (can be improved with NER)
        words = text.split()
        for i, word in enumerate(words):
            if word.lower() in ["in", "for"] and i + 1 < len(words):
                return words[i + 1]
        return "auto"

    def think(self, user_input: str) -> str:
        """Process input and generate response with feature integration."""
        try:
            # Check for personality switch
            for personality in ["professional", "casual", "sarcastic"]:
                if f"switch to {personality}" in user_input.lower():
                    self.set_personality(personality)
                    return f"Switched to {personality} mode, Sir."

            # Check for feature requests
            feature_response = self._process_feature_request(user_input)
            if feature_response:
                context = f"Context: {feature_response}\n\nUser: {user_input}"
                response = self.chat.send_message(context)
            else:
                response = self.chat.send_message(user_input)

            reply = response.text.strip()

            # Save to history
            db.add_memory("user", user_input)
            db.add_memory("model", reply)

            return reply

        except Exception as e:
            return f"I encountered an error: {str(e)[:100]}"

    def set_personality(self, personality: str):
        """Change assistant personality."""
        if personality in ["professional", "casual", "sarcastic"]:
            self.personality = personality
            db.set_setting("personality", personality)
            self._init_gemini()

    def add_calendar_event(self, title: str, datetime_str: str, description: str = ""):
        """Add a calendar event."""
        event = calendar.add_event(title, description, datetime_str)
        return f"Event '{title}' added to calendar"

    def add_note(self, title: str, content: str, tags: list = None):
        """Add a note."""
        note = notes.add_note(title, content, tags or [])
        return f"Note '{title}' saved"

    def create_automation(self, name: str, trigger: str, actions: list):
        """Create an automation."""
        auto = automations.create_automation(name, trigger, actions)
        return f"Automation '{name}' created"

    def get_system_report(self) -> str:
        """Generate a comprehensive system report."""
        status = system_monitor.get_system_status()
        report = f"""
SYSTEM REPORT — {datetime.datetime.now().strftime('%H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CPU: {status['cpu_percent']}%
RAM: {status['ram']['used_gb']}GB / {status['ram']['total_gb']}GB ({status['ram']['percent']}%)
Disk: {status['disk']['free_gb']}GB free
Temperature: {status['temperature']}°C
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return report.strip()

    def clear_memory(self):
        """Clear conversation history."""
        db.clear_memory()
        self.chat = self.model.start_chat(history=[])
        return "Memory cleared. Starting fresh, Sir."

    def get_greeting(self) -> str:
        """Generate contextual greeting."""
        hour = datetime.datetime.now().hour
        period = "morning" if hour < 12 else "afternoon" if hour < 17 else "evening"
        return f"Good {period}! {ASSISTANT_NAME} online. Mode: {self.personality.title()}."
