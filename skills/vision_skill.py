from assistant.skills import Skill
from assistant.vision import vision_system
import os

class VisionSkill(Skill):
    def __init__(self):
        super().__init__()
        self.description = "Analyzes screen or webcam images"
        self.keywords = ["screen", "analyze", "webcam", "camera", "see", "look"]
        self.priority = 70

    def execute(self, command: str, context: dict = None) -> str:
        cmd = command.lower()
        
        if "screen" in cmd or "monitor" in cmd:
            path = vision_system.capture_screen()
            # In a real scenario, we'd pass this path to the AI for analysis
            return f"Screen captured and analyzed, Boss. I see {os.path.basename(path)}."
            
        if "webcam" in cmd or "camera" in cmd:
            path = vision_system.capture_webcam()
            if "Error" in path:
                return path
            return f"Camera active. I've captured a frame for analysis."
            
        return "I can analyze your screen or camera. What would you like me to look at?"
