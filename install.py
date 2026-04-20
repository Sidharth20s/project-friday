"""
FRIDAY Installer — One-click Setup for Windows
Downloads dependencies, configures environment, and prepares the system.
"""

import subprocess
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def install_dependencies():
    """Install all Python dependencies."""
    print("\n" + "="*60)
    print("Installing Dependencies...")
    print("="*60 + "\n")
    
    requirements_file = BASE_DIR / "requirements.txt"
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "--upgrade", "pip"
        ])
        
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", str(requirements_file)
        ])
        
        print("\n✓ Dependencies installed successfully!")
        return True
    except Exception as e:
        print(f"\n✗ Error installing dependencies: {e}")
        return False


def configure_api_keys():
    """Configure API keys for AI and services."""
    print("\n" + "="*60)
    print("API Configuration")
    print("="*60 + "\n")
    
    env_file = BASE_DIR / ".env"
    
    print("Enter your API keys (leave blank to skip):")
    
    gemini_key = input("\n1. Google Gemini API Key: ").strip()
    if gemini_key:
        with open(env_file, "a") as f:
            f.write(f"GEMINI_API_KEY={gemini_key}\n")
        print("✓ Gemini API key saved")
    
    openweather_key = input("\n2. OpenWeather API Key (optional): ").strip()
    if openweather_key:
        with open(env_file, "a") as f:
            f.write(f"OPENWEATHER_API_KEY={openweather_key}\n")
        print("✓ OpenWeather API key saved")
    
    print("\nℹ️  Get API keys from:")
    print("  - Gemini: https://aistudio.google.com/app/apikey")
    print("  - OpenWeather: https://openweathermap.org/api")


def run_windows_setup():
    """Run Windows-specific setup."""
    print("\n" + "="*60)
    print("Windows Setup")
    print("="*60 + "\n")
    
    try:
        subprocess.run([sys.executable, str(BASE_DIR / "setup_windows.py")])
    except Exception as e:
        print(f"✗ Error in Windows setup: {e}")


def check_system():
    """Check system requirements."""
    print("\n" + "="*60)
    print("System Requirements Check")
    print("="*60 + "\n")
    
    # Check Python version
    py_version = sys.version_info
    if py_version.major >= 3 and py_version.minor >= 9:
        print(f"✓ Python {py_version.major}.{py_version.minor}.{py_version.micro} (OK)")
    else:
        print(f"✗ Python 3.9+ required (found {py_version.major}.{py_version.minor})")
        return False
    
    # Check Windows
    if sys.platform.startswith("win"):
        print("✓ Windows OS detected")
    else:
        print("✗ Windows OS required")
        return False
    
    print("\n✓ System requirements met!")
    return True


def main():
    """Main installation process."""
    print("\n" + "█"*60)
    print("█" + " "*58 + "█")
    print("█" + "  FRIDAY AI Assistant - Windows Installation  ".center(58) + "█")
    print("█" + " "*58 + "█")
    print("█"*60)
    
    if not check_system():
        print("\n✗ System check failed. Exiting.")
        return False
    
    print("\nSetup Options:")
    print("1. Full Installation (All steps)")
    print("2. Install Dependencies Only")
    print("3. Configure API Keys Only")
    print("4. Windows Setup Only")
    print("5. Cancel")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == "1":
        if not install_dependencies():
            return False
        configure_api_keys()
        run_windows_setup()
    elif choice == "2":
        if not install_dependencies():
            return False
    elif choice == "3":
        configure_api_keys()
    elif choice == "4":
        run_windows_setup()
    elif choice == "5":
        print("Installation cancelled.")
        return True
    else:
        print("Invalid option")
        return False
    
    print("\n" + "="*60)
    print("✓ Installation Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run: python background_service.py")
    print("2. Or use the desktop shortcut if created")
    print("3. Access web UI at: http://localhost:5000")
    print("\nGlobal Hotkey: Ctrl+Alt+F (voice command)\n")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
