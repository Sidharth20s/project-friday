"""
FRIDAY AI Assistant — Browser Agent
Uses Playwright to autonomously navigate and interact with the web.
"""

import asyncio
from playwright.async_api import async_playwright
from typing import List, Dict, Any, Optional

class BrowserAgent:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        """Initialize the browser."""
        if not self.playwright:
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=False)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()

    async def stop(self):
        """Close the browser."""
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        self.playwright = None

    async def execute_task(self, instructions: List[Dict[str, Any]]) -> str:
        """Execute a series of browser actions."""
        if not self.page:
            await self.start()

        results = []
        for action in instructions:
            type = action.get("type")
            target = action.get("target")
            value = action.get("value")

            try:
                if type == "goto":
                    await self.page.goto(target)
                    results.append(f"Navigated to {target}")
                elif type == "click":
                    await self.page.click(target)
                    results.append(f"Clicked {target}")
                elif type == "type":
                    await self.page.fill(target, value)
                    results.append(f"Typed '{value}' into {target}")
                elif type == "press":
                    await self.page.press(target, value)
                    results.append(f"Pressed {value}")
                elif type == "wait":
                    await self.page.wait_for_timeout(int(value))
                    results.append(f"Waited for {value}ms")
                elif type == "screenshot":
                    path = f"data/vision/agent_shot_{int(asyncio.get_event_loop().time())}.png"
                    await self.page.screenshot(path=path)
                    results.append(f"Screenshot saved to {path}")
            except Exception as e:
                results.append(f"Error in {type} on {target}: {str(e)}")
                break

        return "\n".join(results)

# Global browser agent instance
browser_agent = BrowserAgent()
