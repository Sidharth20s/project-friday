"""
FRIDAY AI Assistant — Configuration Manager
Handles API keys, settings, and first-run setup.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root
BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


def get_setting(key: str, default: str = "") -> str:
    return os.getenv(key, default)


def save_setting(key: str, value: str):
    """Write or update a key=value line in .env file."""
    lines = []
    found = False

    if ENV_FILE.exists():
        with open(ENV_FILE, "r") as f:
            lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith(f"{key}="):
            new_lines.append(f"{key}={value}\n")
            found = True
        else:
            new_lines.append(line)

    if not found:
        new_lines.append(f"{key}={value}\n")

    with open(ENV_FILE, "w") as f:
        f.writelines(new_lines)

    os.environ[key] = value


def first_run_setup():
    """Interactive first-run setup if API key is missing."""
    api_key = get_setting("GEMINI_API_KEY")
    if api_key and api_key != "your_gemini_api_key_here":
        return api_key  # Already configured

    print("\n" + "=" * 60)
    print("  Welcome to FRIDAY — Your Personal AI Assistant")
    print("=" * 60)
    print("\n  First-time setup required!\n")
    print("  You need a FREE Google Gemini API key.")
    print("  Get one at: https://aistudio.google.com/\n")
    print("  Steps:")
    print("    1. Go to https://aistudio.google.com/")
    print("    2. Sign in with your Google account")
    print("    3. Click 'Get API key' → 'Create API key'")
    print("    4. Copy and paste it below\n")
    print("=" * 60)

    while True:
        key = input("\n  Paste your Gemini API key here: ").strip()
        if len(key) > 20:
            save_setting("GEMINI_API_KEY", key)
            print("\n  ✅ API key saved! FRIDAY is ready.\n")
            return key
        else:
            print("  ❌ That doesn't look right. Please try again.")


# ─── Loaded Settings ──────────────────────────────────────
GEMINI_API_KEY    = get_setting("GEMINI_API_KEY")
WEATHER_API_KEY   = get_setting("WEATHER_API_KEY")
DEFAULT_CITY      = get_setting("DEFAULT_CITY", "New Delhi")
WAKE_WORD         = get_setting("WAKE_WORD", "hey friday")
ASSISTANT_NAME    = get_setting("ASSISTANT_NAME", "Friday")
VOICE_SPEED       = int(get_setting("VOICE_SPEED", "175"))
VOICE_VOLUME      = float(get_setting("VOICE_VOLUME", "1.0"))
WEB_PORT          = int(get_setting("WEB_PORT", "5051"))

# ─── Telegram Integration ──────────────────────────────────
TELEGRAM_USER_ID  = get_setting("TELEGRAM_USER_ID")
TELEGRAM_BOT_API  = get_setting("TELEGRAM_BOT_API")
