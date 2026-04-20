"""
FRIDAY Telegram Bot Commands
Handles all system operations and commands
"""

import os
import subprocess
import socket
import psutil
import json
from datetime import datetime, timedelta
from pathlib import Path
import pyperclip

from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode

import logging
logger = logging.getLogger(__name__)


class TelegramCommands:
    """Command handlers for Telegram bot"""
    
    # Whitelisted applications - security measure
    ALLOWED_APPS = {
        "chrome": "chrome.exe",
        "firefox": "firefox.exe",
        "spotify": "spotify.exe",
        "vlc": "vlc.exe",
        "notepad": "notepad.exe",
        "steam": "steam.exe",
        "discord": "discord.exe",
        "telegram": "telegram.exe"
    }
    
    async def get_system_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Get complete system status"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage("C:\\")
            
            # CPU temperature (Windows)
            try:
                temps = psutil.sensors_temperatures()
                cpu_temp = temps.get("coretemp", [{}])[0].get("current", "N/A")
            except:
                cpu_temp = "N/A"
            
            status = f"""
📊 **System Status**

**CPU:**
• Usage: {cpu_percent}%
• Temperature: {cpu_temp}°C
• Cores: {psutil.cpu_count()}

**Memory:**
• Used: {memory.used / (1024**3):.2f} GB
• Total: {memory.total / (1024**3):.2f} GB
• Usage: {memory.percent}%

**Disk (C:):**
• Used: {disk.used / (1024**3):.2f} GB
• Total: {disk.total / (1024**3):.2f} GB
• Free: {disk.free / (1024**3):.2f} GB

**Uptime:** {self._get_uptime()}
**Boot Time:** {datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}
            """
            await update.message.reply_text(status, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def get_temperature(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Get CPU temperature"""
        try:
            temps = psutil.sensors_temperatures()
            
            if not temps:
                await update.message.reply_text("⚠️ Temperature sensors not available")
                return
            
            temp_text = "🌡️ **System Temperature**\n\n"
            for name, entries in temps.items():
                temp_text += f"**{name}:**\n"
                for entry in entries:
                    temp_text += f"• {entry.label}: {entry.current}°C\n"
            
            await update.message.reply_text(temp_text, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def get_battery(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Get battery status"""
        try:
            battery = psutil.sensors_battery()
            
            if not battery:
                await update.message.reply_text("⚠️ No battery detected (Desktop PC)")
                return
            
            status = "🔌 Plugged" if battery.power_plugged else "🔋 Unplugged"
            
            text = f"""
🔋 **Battery Status**

• Status: {status}
• Charge: {battery.percent}%
• Time Left: {self._seconds_to_time(battery.secsleft)}
            """
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def list_processes(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """List running processes"""
        try:
            processes = sorted(
                psutil.process_iter(['pid', 'name', 'memory_percent']),
                key=lambda x: x.info['memory_percent'],
                reverse=True
            )[:10]
            
            text = "⚙️ **Top 10 Processes (by memory)**\n\n"
            for p in processes:
                text += f"• {p.info['name']}: {p.info['memory_percent']:.1f}%\n"
            
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def lock_screen(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Lock screen"""
        try:
            os.system("rundll32.exe user32.dll,LockWorkStation")
            await update.message.reply_text("🔒 Screen locked!")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def sleep_pc(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Put PC to sleep"""
        try:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            await update.message.reply_text("😴 PC going to sleep...")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def restart_pc(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Restart PC"""
        try:
            await update.message.reply_text("🔄 Restarting PC in 30 seconds... Press the menu button to cancel!")
            os.system("shutdown /r /t 30 /c 'Restart initiated from Telegram'")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def shutdown_pc(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Shutdown PC"""
        try:
            await update.message.reply_text("⛔ Shutting down PC in 30 seconds... Press the menu button to cancel!")
            os.system("shutdown /s /t 30 /c 'Shutdown initiated from Telegram'")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def take_screenshot(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Take screenshot and send"""
        try:
            from PIL import ImageGrab
            
            screenshot = ImageGrab.grab()
            screenshot_path = "screenshot.png"
            screenshot.save(screenshot_path)
            
            with open(screenshot_path, 'rb') as photo:
                await update.message.reply_photo(photo)
            
            os.remove(screenshot_path)
        except Exception as e:
            await update.message.reply_text(f"❌ Error taking screenshot: {str(e)}")
    
    async def list_files(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """List files in Downloads"""
        try:
            downloads = Path.home() / "Downloads"
            files = list(downloads.glob("*"))[:20]
            
            text = "📁 **Recent files in Downloads:**\n\n"
            for file in sorted(files, key=lambda x: x.stat().st_mtime, reverse=True):
                size = file.stat().st_size / (1024*1024)
                text += f"• {file.name} ({size:.1f} MB)\n"
            
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def open_app(self, update: Update, context: ContextTypes.DEFAULT_TYPE, app_name: str) -> None:
        """Open application"""
        try:
            if app_name.lower() not in self.ALLOWED_APPS:
                await update.message.reply_text(f"❌ App '{app_name}' is not in the allowed list")
                return
            
            app_path = self.ALLOWED_APPS[app_name.lower()]
            subprocess.Popen(app_path)
            await update.message.reply_text(f"✅ Opening {app_name}...")
        except Exception as e:
            await update.message.reply_text(f"❌ Error opening app: {str(e)}")
    
    async def get_event_logs(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Get Windows event logs"""
        try:
            # Using wevtutil to get event logs
            result = subprocess.run(
                'wevtutil qe System /c:10 /rd:true /f:text',
                capture_output=True,
                text=True,
                shell=True
            )
            
            logs = result.stdout[:2000] if result.stdout else "No recent events"
            text = f"📋 **Recent System Events:**\n\n```\n{logs}\n```"
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def get_login_history(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Get login history"""
        try:
            result = subprocess.run(
                'wevtutil qe Security /c:10 /rd:true /f:text /q:"*[System[EventID=4624]]"',
                capture_output=True,
                text=True,
                shell=True
            )
            
            logs = result.stdout[:2000] if result.stdout else "No login events found"
            text = f"🔐 **Login History:**\n\n```\n{logs}\n```"
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def get_shutdown_logs(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Get shutdown/restart logs"""
        try:
            result = subprocess.run(
                'wevtutil qe System /c:10 /rd:true /f:text /q:"*[System[EventID=1074 or EventID=1076]]"',
                capture_output=True,
                text=True,
                shell=True
            )
            
            logs = result.stdout[:2000] if result.stdout else "No shutdown events found"
            text = f"⏹️ **Shutdown/Restart Logs:**\n\n```\n{logs}\n```"
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def get_system_events(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Get system events"""
        try:
            result = subprocess.run(
                'wevtutil qe System /c:20 /rd:true /f:text',
                capture_output=True,
                text=True,
                shell=True
            )
            
            logs = result.stdout[:2000] if result.stdout else "No events found"
            text = f"🔄 **System Events:**\n\n```\n{logs}\n```"
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def get_clipboard(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Get clipboard content"""
        try:
            clipboard = pyperclip.paste()
            
            if not clipboard:
                await update.message.reply_text("📋 Clipboard is empty")
                return
            
            # Limit to 1000 chars
            if len(clipboard) > 1000:
                clipboard = clipboard[:1000] + "\n... (truncated)"
            
            text = f"📋 **Clipboard Content:**\n\n```\n{clipboard}\n```"
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def get_network_info(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Get network information"""
        try:
            # Get IP
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
            
            # Get network stats
            net_io = psutil.net_io_counters()
            
            text = f"""
🌐 **Network Information**

• Hostname: {hostname}
• Local IP: {ip}
• Bytes Sent: {net_io.bytes_sent / (1024**3):.2f} GB
• Bytes Received: {net_io.bytes_recv / (1024**3):.2f} GB
• Packets Sent: {net_io.packets_sent:,}
• Packets Received: {net_io.packets_recv:,}
            """
            await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    async def handle_file_upload(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle file uploads to PC"""
        try:
            file = await update.message.effective_attachment.get_file()
            
            # Save to Downloads
            downloads = Path.home() / "Downloads"
            file_path = downloads / file.file_name
            
            await file.download_to_drive(str(file_path))
            
            await update.message.reply_text(
                f"✅ File saved to:\n`{file_path}`",
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Error uploading file: {str(e)}")
    
    async def handle_custom_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, command: str) -> None:
        """Handle custom commands"""
        try:
            if command.startswith("/cancel"):
                os.system("shutdown /a")
                await update.message.reply_text("✅ Scheduled shutdown/restart cancelled!")
            else:
                await update.message.reply_text("❓ Unknown command. Use the menu buttons!")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    
    def _get_uptime(self) -> str:
        """Format uptime"""
        uptime_seconds = int(datetime.now().timestamp() - psutil.boot_time())
        days = uptime_seconds // 86400
        hours = (uptime_seconds % 86400) // 3600
        minutes = (uptime_seconds % 3600) // 60
        return f"{days}d {hours}h {minutes}m"
    
    def _seconds_to_time(self, seconds: int) -> str:
        """Convert seconds to readable time"""
        if seconds > 3600:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}h {minutes}m"
        else:
            minutes = seconds // 60
            return f"{minutes}m"
