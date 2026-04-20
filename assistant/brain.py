"""
FRIDAY AI Assistant — Gemini AI Brain
Handles all AI conversation, memory, and intent routing.
"""

import datetime
from pathlib import Path

import google.generativeai as genai
from assistant.config import GEMINI_API_KEY, ASSISTANT_NAME
from assistant import db

# ─── Personality Prompts ──────────────────────────────────
PERSONALITIES = {
    "professional": "You are a professional, highly efficient AI assistant. Your tone is formal and polite.",
    "casual": "You are a friendly, laid-back AI assistant. You use casual language and are very approachable.",
    "sarcastic": "You are a witty, slightly sarcastic AI assistant inspired by Tony Stark's FRIDAY. You have a sharp tongue but are still helpful.",
}

DEFAULT_PROMPT = f"""You are {ASSISTANT_NAME}, an advanced AI assistant. 
Today's date and time: {datetime.datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")}
Keep responses under 3 sentences unless the user asks for detail.
"""

class FridayBrain:
    def __init__(self):
        self.model = None
        self.chat = None
        self.personality = db.get_setting("personality", "sarcastic")
        self._init_gemini()

    def _init_gemini(self):
        """Initialize Gemini client with current personality."""
        if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
            raise ValueError("Gemini API key not configured. Run setup first.")

        genai.configure(api_key=GEMINI_API_KEY)
        
        system_instruction = f"{DEFAULT_PROMPT}\n{PERSONALITIES.get(self.personality, PERSONALITIES['sarcastic'])}"
        
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-latest",
            system_instruction=system_instruction
        )
        # Restore prior conversation history from SQLite
        self.chat = self.model.start_chat(history=self._format_history_for_gemini())

    def _format_history_for_gemini(self) -> list:
        """Convert stored history from SQLite to Gemini format."""
        history = db.get_history(limit=20)
        formatted = []
        for entry in history:
            formatted.append({"role": entry["role"], "parts": [entry["text"]]})
        return formatted

    def think(self, user_input: str) -> str:
        """Send message to Gemini and get response."""
        try:
            # Check for personality switch command
            for p in PERSONALITIES:
                if f"switch to {p} mode" in user_input.lower():
                    self.set_personality(p)
                    return f"Switching to {p} mode, Sir. How can I help you now?"

            response = self.chat.send_message(user_input)
            reply = response.text.strip()

            # Save to SQLite
            db.add_memory("user", user_input)
            db.add_memory("model", reply)

            return reply
        except Exception as e:
            return f"I encountered an error: {str(e)[:100]}"

    def set_personality(self, personality: str):
        if personality in PERSONALITIES:
            self.personality = personality
            db.set_setting("personality", personality)
            self._init_gemini()

    def clear_memory(self):
        """Wipe conversation history from SQLite."""
        db.clear_memory()
        self.chat = self.model.start_chat(history=[])
        return "Memory cleared. Starting fresh, Sir."

    def get_greeting(self) -> str:
        """Generate a contextual greeting."""
        hour = datetime.datetime.now().hour
        period = "morning" if hour < 12 else "afternoon" if hour < 17 else "evening"
        return f"Good {period}! {ASSISTANT_NAME} online. Mode: {self.personality.title()}."

    def clear_memory(self):
        """Wipe conversation history."""
        self.history = []
        self._save_memory()
        # Restart chat session
        self.chat = self.model.start_chat(history=[])
        return "Memory cleared. Starting fresh, Sir."

    def get_greeting(self) -> str:
        """Generate a contextual greeting."""
        hour = datetime.datetime.now().hour
        if hour < 12:
            period = "morning"
        elif hour < 17:
            period = "afternoon"
        else:
            period = "evening"

        return (f"Good {period}! FRIDAY online and ready. "
                f"All systems operational. How can I assist you today?")
