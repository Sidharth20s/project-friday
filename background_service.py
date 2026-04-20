"""
FRIDAY Background Service — Windows System Tray Integration
Runs FRIDAY in the background with system tray icon and global hotkeys.
"""

import sys
import threading
import time
from pathlib import Path
from pystray import Icon, Menu, MenuItem
from PIL import Image
import keyboard
import logging

# Add project root to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from assistant.config import WEB_PORT, first_run_setup
from main import FridayCore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(BASE_DIR / "logs" / "friday_service.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class FridayBackgroundService:
    """Manages FRIDAY as a background service with system tray icon."""

    def __init__(self):
        self.friday = FridayCore()
        self.tray_icon = None
        self.running = True
        self.voice_active = False
        
        # Create logs directory
        (BASE_DIR / "logs").mkdir(exist_ok=True)
        
        logger.info("FRIDAY Background Service initialized")

    def create_icon(self):
        """Create system tray icon."""
        try:
            # Try to use a generated icon, fallback to default
            image = Image.new("RGB", (64, 64), color="blue")
        except Exception as e:
            logger.warning(f"Could not create icon: {e}")
            image = Image.new("RGB", (64, 64), color="blue")
        
        menu = Menu(
            MenuItem("🎙️ Voice Command", self.on_voice_click),
            MenuItem("📝 Text Command", self.on_text_click),
            MenuItem("🌐 Open Web UI", self.on_open_ui),
            MenuItem("⚙️ Settings", self.on_settings),
            Menu.SEPARATOR,
            MenuItem("📊 Status", self.on_status),
            MenuItem("❌ Exit", self.on_exit),
        )

        self.tray_icon = Icon(
            "FRIDAY Assistant",
            image,
            menu=menu,
            title="FRIDAY - AI Assistant"
        )

    def on_voice_click(self, icon, item):
        """Handle voice command from tray menu."""
        logger.info("Voice command activated from tray")
        threading.Thread(target=self.friday.voice.listen_for_command, daemon=True).start()

    def on_text_click(self, icon, item):
        """Handle text input from tray."""
        logger.info("Text command activated from tray")
        # This could open a dialog or web UI
        import webbrowser
        webbrowser.open(f"http://localhost:{WEB_PORT}")

    def on_open_ui(self, icon, item):
        """Open web UI in default browser."""
        import webbrowser
        logger.info("Opening web UI")
        webbrowser.open(f"http://localhost:{WEB_PORT}")

    def on_settings(self, icon, item):
        """Open settings."""
        logger.info("Settings requested")
        import webbrowser
        webbrowser.open(f"http://localhost:{WEB_PORT}/settings")

    def on_status(self, icon, item):
        """Show current status."""
        from assistant.features.system_monitor import get_system_status
        status = get_system_status()
        logger.info(f"System Status: {status}")

    def on_exit(self, icon, item):
        """Exit the service."""
        logger.info("FRIDAY service shutting down")
        self.running = False
        self.tray_icon.stop()

    def setup_global_hotkey(self):
        """Setup global hotkey (Ctrl+Alt+F) to activate voice command."""
        def hotkey_handler():
            logger.info("Global hotkey triggered")
            self.on_voice_click(None, None)

        try:
            keyboard.add_hotkey("ctrl+alt+f", hotkey_handler)
            logger.info("Global hotkey (Ctrl+Alt+F) registered successfully")
        except Exception as e:
            logger.warning(f"Could not register global hotkey: {e}")

    def run(self):
        """Start the background service."""
        logger.info("Starting FRIDAY background service...")
        
        # Setup global hotkey
        self.setup_global_hotkey()
        
        # Start Flask in background
        from web.app import socketio
        web_thread = threading.Thread(
            target=lambda: socketio.run(
                __import__("web.app", fromlist=["app"]).app,
                host="127.0.0.1",
                port=WEB_PORT,
                debug=False,
                use_reloader=False
            ),
            daemon=True
        )
        web_thread.start()
        logger.info(f"Web server started on port {WEB_PORT}")
        
        # Create and show tray icon
        self.create_icon()
        
        try:
            self.tray_icon.run()
        except Exception as e:
            logger.error(f"Error in tray icon: {e}")
            self.running = False

    def run_in_background(self):
        """Run as pure background service without tray (for Windows Service)."""
        logger.info("Running FRIDAY as background service (no UI)")
        
        self.setup_global_hotkey()
        
        # Start Flask
        from web.app import socketio, app
        web_thread = threading.Thread(
            target=lambda: socketio.run(
                app,
                host="127.0.0.1",
                port=WEB_PORT,
                debug=False,
                use_reloader=False
            ),
            daemon=True
        )
        web_thread.start()
        
        logger.info(f"Background service running on port {WEB_PORT}")
        
        # Keep alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Background service stopped")


def main():
    """Main entry point."""
    first_run_setup()
    
    service = FridayBackgroundService()
    service.run()


if __name__ == "__main__":
    main()
