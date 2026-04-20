"""
FRIDAY AI Assistant — Main Entry Point
Orchestrates all components: Brain, Voice, Actions, and Web UI.
"""

import sys
import threading
import webbrowser
import time
from pathlib import Path

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from assistant.config import first_run_setup, WEB_PORT
from assistant.brain import FridayBrain
from assistant.voice import VoiceEngine
from assistant import actions
from web.app import app, socketio, broadcast_message, broadcast_voice_state


class FridayCore:
    """Central orchestrator that connects all modules."""

    def __init__(self):
        print("\nInitializing FRIDAY...\n")
        self.brain  = FridayBrain()
        self.voice  = VoiceEngine(on_command_callback=self._on_voice_command)
        self.running = True

    def process(self, text: str, source: str = "text") -> str:
        """Main processing pipeline: text → intent → action/AI → response."""
        if not text:
            return ""

        text = text.strip()
        print(f"[{source.upper()}] User: {text}")

        # Handle wake-word only (no command yet)
        if text == "wake_only":
            reply = "Yes Sir? I'm listening."
            self._respond(reply, source)
            return reply

        # Check cancel shutdown
        if "cancel shutdown" in text.lower():
            reply = actions.cancel_shutdown()
            self._respond(reply, source)
            return reply

        # Check clear memory
        if any(p in text.lower() for p in ["clear memory", "forget everything", "reset memory"]):
            reply = self.brain.clear_memory()
            self._respond(reply, source)
            return reply

        # Detect system action intent
        intent = actions.detect_intent(text)
        action_reply = None

        if intent["action"] != "ai_response":
            action_reply = actions.execute(intent)

        if action_reply:
            # Action succeeded — optionally let AI comment on it
            reply = action_reply
        else:
            # Let AI brain handle the response
            reply = self.brain.think(text)

        print(f"[FRIDAY] {reply}")
        self._respond(reply, source)
        return reply

    def _respond(self, text: str, source: str):
        """Broadcast to UI and optionally speak."""
        broadcast_message("friday", text)
        if source == "voice":
            broadcast_voice_state("speaking", "Speaking...")
            self.voice.speak(text)
            broadcast_voice_state("idle", "Ready")

    def _on_voice_command(self, text: str, source: str = "voice"):
        """Callback from wake word detection loop."""
        broadcast_voice_state("listening", "Heard you!")
        broadcast_message("user", text)
        self.process(text, source="voice")
        broadcast_voice_state("idle", "Ready")

    def start(self):
        """Start voice engine wake word loop."""
        greeting = self.brain.get_greeting()
        print(f"\nFRIDAY: {greeting}\n")
        time.sleep(1)  # Wait for web UI to be ready
        broadcast_message("friday", greeting)
        self.voice.speak_async(greeting)
        self.voice.start_wake_word_loop()


def open_browser_delayed(port: int, delay: float = 1.5):
    """Open browser after server starts."""
    time.sleep(delay)
    webbrowser.open(f"http://localhost:{port}")


if __name__ == "__main__":
    # ── First-run setup (API key) ──────────────────────────
    first_run_setup()

    # ── Initialize FRIDAY core ────────────────────────────
    friday = FridayCore()

    # ── Attach to Flask server ────────────────────────────
    import web.app as web_module
    web_module.friday_core = friday

    # ── Start background threads ──────────────────────────
    core_thread = threading.Thread(target=friday.start, daemon=True)
    core_thread.start()

    browser_thread = threading.Thread(
        target=open_browser_delayed, args=(WEB_PORT,), daemon=True
    )
    browser_thread.start()

    # ── Start Flask + SocketIO server ─────────────────────
    print(f"\nFRIDAY UI -> http://localhost:{WEB_PORT}\n")
    print("   Press Ctrl+C to shut down FRIDAY.\n")

    socketio.run(app, host="0.0.0.0", port=WEB_PORT, debug=False)
