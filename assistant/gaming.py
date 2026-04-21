"""
FRIDAY AI Assistant — Gaming Integration
Handles Steam, Epic Games, and gaming sessions.
"""

import os
import subprocess
import webbrowser
import psutil
from typing import Dict, List

POPULAR_STEAM_GAMES = {
    "counter-strike": "730",
    "csgo": "730",
    "cs go": "730",
    "dota 2": "570",
    "gta 5": "271590",
    "gta v": "271590",
    "apex legends": "1172470",
    "team fortress 2": "440",
    "pubg": "578080",
    "cyberpunk 2077": "1091500"
}

class GamingSystem:
    def __init__(self):
        pass

    def launch_steam(self):
        """Open Steam."""
        try:
            webbrowser.open("steam://open/main")
            return "Launching Steam."
        except Exception:
            return "Failed to launch Steam."

    def play_steam_game(self, game_name: str):
        """Launch a Steam game by name."""
        game_name = game_name.lower()
        app_id = POPULAR_STEAM_GAMES.get(game_name)
        
        if app_id:
            webbrowser.open(f"steam://run/{app_id}")
            return f"Launching {game_name.title()} via Steam."
        else:
            return f"I don't have the ID for '{game_name}'. Try saying 'Launch Steam' and opening it manually."

    def launch_epic(self):
        """Open Epic Games Launcher."""
        try:
            # Common install paths for Epic
            paths = [
                os.environ.get("ProgramFiles(x86)", "") + r"\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe",
                os.environ.get("ProgramFiles", "") + r"\Epic Games\Launcher\Portal\Binaries\Win32\EpicGamesLauncher.exe"
            ]
            for p in paths:
                if os.path.exists(p):
                    subprocess.Popen(p)
                    return "Launching Epic Games Launcher."
            
            # Fallback to URI scheme
            webbrowser.open("com.epicgames.launcher://")
            return "Launching Epic Games Launcher via URI."
        except Exception:
            return "Failed to launch Epic Games Launcher."

    def get_running_games(self) -> List[str]:
        """Check for common game processes."""
        game_procs = ["steam", "epicgameslauncher", "valorant", "league of legends", "csgo", "dota2"]
        running = []
        for proc in psutil.process_iter(['name']):
            try:
                name = proc.info['name'].lower()
                if any(gp in name for gp in game_procs):
                    running.append(name)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return list(set(running))

    def start_gaming_session(self, duration_hours: float):
        """Schedule a system shutdown after gaming session."""
        seconds = int(duration_hours * 3600)
        os.system(f"shutdown /s /t {seconds}")
        return f"Gaming session started. System will shut down in {duration_hours} hours."

gaming_system = GamingSystem()
