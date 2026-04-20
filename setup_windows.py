"""
FRIDAY Windows Setup — Auto-start and Service Registration
Registers FRIDAY to start on Windows boot and creates desktop shortcuts.
"""

import os
import sys
import winreg
import shutil
from pathlib import Path
import subprocess

BASE_DIR = Path(__file__).resolve().parent


def create_startup_shortcut():
    """Create desktop shortcut for FRIDAY."""
    desktop = Path.home() / "Desktop"
    shortcut_path = desktop / "FRIDAY Assistant.lnk"

    # Use powershell to create shortcut
    ps_script = f"""
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut("{shortcut_path}")
    $shortcut.TargetPath = "{sys.executable}"
    $shortcut.Arguments = "{BASE_DIR / 'background_service.py'}"
    $shortcut.WorkingDirectory = "{BASE_DIR}"
    $shortcut.Description = "FRIDAY AI Assistant"
    $shortcut.IconLocation = "{BASE_DIR / 'web/static/friday.ico'}"
    $shortcut.Save()
    """
    
    try:
        subprocess.run(
            ["powershell", "-Command", ps_script],
            capture_output=True,
            check=True
        )
        print(f"✓ Desktop shortcut created: {shortcut_path}")
    except Exception as e:
        print(f"✗ Could not create shortcut: {e}")


def register_startup():
    """Register FRIDAY in Windows startup."""
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
        
        command = f'"{sys.executable}" "{BASE_DIR / "background_service.py"}"'
        winreg.SetValueEx(registry_key, "FRIDAY", 0, winreg.REG_SZ, command)
        winreg.CloseKey(registry_key)
        
        print("✓ FRIDAY registered in Windows startup")
    except Exception as e:
        print(f"✗ Could not register startup: {e}")


def unregister_startup():
    """Remove FRIDAY from Windows startup."""
    try:
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_WRITE)
        winreg.DeleteValue(registry_key, "FRIDAY")
        winreg.CloseKey(registry_key)
        
        print("✓ FRIDAY removed from Windows startup")
    except Exception as e:
        print(f"✗ Could not unregister startup: {e}")


def setup_environment():
    """Setup environment and directories."""
    # Create necessary directories
    (BASE_DIR / "logs").mkdir(exist_ok=True)
    (BASE_DIR / "data").mkdir(exist_ok=True)
    (BASE_DIR / "assistant/plugins").mkdir(exist_ok=True)
    
    print("✓ Directories created")


def main():
    """Run full setup."""
    print("\n" + "="*60)
    print("FRIDAY AI Assistant — Windows Setup")
    print("="*60 + "\n")
    
    setup_environment()
    
    print("\nSetup Options:")
    print("1. Enable Auto-start on Boot")
    print("2. Disable Auto-start")
    print("3. Create Desktop Shortcut")
    print("4. Full Setup (All of the above)")
    print("5. Exit")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == "1":
        register_startup()
    elif choice == "2":
        unregister_startup()
    elif choice == "3":
        create_startup_shortcut()
    elif choice == "4":
        setup_environment()
        register_startup()
        create_startup_shortcut()
        print("\n✓ Full setup complete!")
    elif choice == "5":
        print("Exiting...")
    else:
        print("Invalid option")


if __name__ == "__main__":
    main()
