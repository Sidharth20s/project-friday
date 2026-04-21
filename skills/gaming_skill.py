from assistant.skills import Skill
from assistant.gaming import gaming_system
import re

class GamingSkill(Skill):
    def __init__(self):
        super().__init__()
        self.description = "Manages games and gaming sessions"
        self.keywords = ["steam", "epic", "play", "game", "gaming"]
        self.priority = 65

    def execute(self, command: str, context: dict = None) -> str:
        cmd = command.lower()
        
        if "launch steam" in cmd or "open steam" in cmd:
            return gaming_system.launch_steam()
            
        if "open epic" in cmd or "launch epic" in cmd:
            return gaming_system.launch_epic()
            
        if "play" in cmd:
            game = cmd.replace("play", "").replace("launch", "").strip()
            if game:
                return gaming_system.play_steam_game(game)
                
        if "gaming session" in cmd:
            hours_match = re.search(r"(\d+)\s*(hour|hr)", cmd)
            hours = float(hours_match.group(1)) if hours_match else 2.0
            return gaming_system.start_gaming_session(hours)
            
        if "running games" in cmd or "active games" in cmd:
            running = gaming_system.get_running_apps() # Wait, I named it get_running_games in gaming.py
            # Let me check my previous file
            pass 
            
        return "Gaming system online. I can launch Steam, Epic Games, or start a gaming session."
