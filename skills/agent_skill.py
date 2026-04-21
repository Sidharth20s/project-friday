from assistant.skills import Skill
from assistant.browser_agent import browser_agent
from assistant.desktop_agent import desktop_agent
import asyncio
import threading

class AgentSkill(Skill):
    def __init__(self):
        super().__init__()
        self.description = "Autonomous agent for web and desktop tasks"
        self.keywords = ["agent", "automatically", "run and click", "test", "automate"]
        self.priority = 90

    def execute(self, command: str, context: dict = None) -> str:
        cmd = command.lower()
        
        if "test" in cmd and ("app" in cmd or "web" in cmd):
            return "Starting autonomous testing agent... (This feature uses Playwright for web and PyAutoGUI for desktop)."

        if "go to chrome" in cmd or "search on chrome" in cmd:
            # Demonstration of a browser agent task
            query = cmd.replace("go to chrome and", "").replace("search on chrome for", "").replace("go to chrome", "").strip()
            
            # Run in a separate thread/event loop to avoid blocking the main assistant
            def run_browser():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                tasks = [
                    {"type": "goto", "target": "https://www.google.com"},
                    {"type": "type", "target": "textarea[name='q']", "value": query if query else "FRIDAY AI Assistant"},
                    {"type": "press", "target": "textarea[name='q']", "value": "Enter"},
                    {"type": "wait", "value": "2000"},
                    {"type": "screenshot"}
                ]
                loop.run_until_complete(browser_agent.execute_task(tasks))
                loop.close()

            threading.Thread(target=run_browser).start()
            return f"Agent deployed to Chrome. Searching for '{query if query else 'FRIDAY'}'."

        if "automate desktop" in cmd:
            # Example desktop task
            tasks = [
                {"type": "press", "value": "win"},
                {"type": "wait", "value": "1"},
                {"type": "type", "value": "notepad"},
                {"type": "press", "value": "enter"},
                {"type": "wait", "value": "1"},
                {"type": "type", "value": "FRIDAY AGENT IS RUNNING."}
            ]
            desktop_agent.execute_task(tasks)
            return "Desktop automation agent started."

        return "Agent system ready. I can automate your browser (Chrome) or desktop tasks. Try saying 'Go to Chrome and search for local news'."

