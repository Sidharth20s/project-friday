"""
FRIDAY AI Assistant — Desktop Agent
Uses pyautogui to autonomously control the Windows desktop.
"""

import pyautogui
import time
from typing import List, Dict, Any

class DesktopAgent:
    def __init__(self):
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5

    def execute_task(self, instructions: List[Dict[str, Any]]) -> str:
        """Execute a series of desktop actions."""
        results = []
        for action in instructions:
            type = action.get("type")
            target = action.get("target") # Can be text for OCR or (x, y)
            value = action.get("value")

            try:
                if type == "click":
                    if isinstance(target, (list, tuple)):
                        pyautogui.click(target[0], target[1])
                        results.append(f"Clicked at {target}")
                    else:
                        # Try to find by image or text (future integration)
                        results.append(f"Click on {target} not yet implemented via OCR")
                elif type == "type":
                    pyautogui.write(value, interval=0.1)
                    results.append(f"Typed '{value}'")
                elif type == "press":
                    pyautogui.press(value)
                    results.append(f"Pressed {value}")
                elif type == "hotkey":
                    pyautogui.hotkey(*value)
                    results.append(f"Pressed hotkey {value}")
                elif type == "wait":
                    time.sleep(float(value))
                    results.append(f"Waited for {value}s")
            except Exception as e:
                results.append(f"Error in {type}: {str(e)}")
                break

        return "\n".join(results)

desktop_agent = DesktopAgent()
