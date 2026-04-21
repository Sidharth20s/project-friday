"""
FRIDAY AI Assistant — Modular Skills System
Inspired by Project JARVIS.
"""

import os
import importlib.util
from pathlib import Path
from typing import List, Dict, Any, Optional

class Skill:
    """Base class for all FRIDAY skills."""
    def __init__(self):
        self.name = self.__class__.__name__
        self.description = "No description provided."
        self.keywords = []
        self.priority = 50

    def can_handle(self, command: str) -> bool:
        """Check if this skill can handle the given command."""
        return any(kw in command.lower() for kw in self.keywords)

    def execute(self, command: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Execute the skill's logic."""
        raise NotImplementedError("Skills must implement execute()")

class SkillRegistry:
    """Registry to manage and load skills."""
    def __init__(self):
        self.skills: List[Skill] = []

    def register(self, skill: Skill):
        """Register a new skill."""
        self.skills.append(skill)
        # Sort by priority (higher first)
        self.skills.sort(key=lambda x: x.priority, reverse=True)

    def load_from_directory(self, directory: str):
        """Auto-load skills from a directory."""
        path = Path(directory)
        if not path.exists():
            return

        for file in path.glob("*_skill.py"):
            try:
                spec = importlib.util.spec_from_file_location(file.stem, file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Look for classes that inherit from Skill
                for attr_name in dir(module):
                    attr = getattr(module, attr_name)
                    if isinstance(attr, type) and issubclass(attr, Skill) and attr is not Skill:
                        self.register(attr())
            except Exception as e:
                print(f"Error loading skill from {file}: {e}")

    def handle_command(self, command: str, context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Find a skill to handle the command and execute it."""
        for skill in self.skills:
            if skill.can_handle(command):
                return skill.execute(command, context)
        return None

# Global registry
skill_registry = SkillRegistry()
