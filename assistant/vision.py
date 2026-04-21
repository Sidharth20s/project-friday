"""
FRIDAY AI Assistant — Vision Processing
Handles screen analysis and webcam vision.
"""

import cv2
import pyautogui
import numpy as np
from pathlib import Path
from datetime import datetime
import os

class VisionSystem:
    def __init__(self, data_dir: str = "data/vision"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def capture_screen(self) -> str:
        """Capture screen and return path to image."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.data_dir / f"screen_{timestamp}.png"
        screenshot = pyautogui.screenshot()
        screenshot.save(filename)
        return str(filename)

    def capture_webcam(self, index: int = 0) -> str:
        """Capture webcam frame and return path to image."""
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            return "Error: Camera not accessible"
        
        ret, frame = cap.read()
        if not ret:
            cap.release()
            return "Error: Failed to capture frame"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.data_dir / f"webcam_{timestamp}.jpg"
        cv2.imwrite(str(filename), frame)
        cap.release()
        return str(filename)

    def analyze_image(self, image_path: str, query: str = "What's in this image?") -> str:
        """Analyze image using AI (Gemini)."""
        # This will be integrated with brain.py or a similar AI handler
        # For now, return a placeholder
        return f"Analyzing {os.path.basename(image_path)} with query: {query}"

vision_system = VisionSystem()
