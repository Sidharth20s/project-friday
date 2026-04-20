# 🤖 Telegram Bot - Command Reference

Quick command reference for FRIDAY Telegram Bot.

---

## 📊 System Status Commands

```
/system          Full system status (CPU, RAM, Disk, Uptime)
/battery         Battery status (laptops only)
/temp            CPU temperature
/processes       Top 10 running processes by memory
/network         Network info (IP, data usage)
/status          Alias for /system
```

**Example Response:**
```
📊 System Status

CPU: 45% | 62°C
Memory: 8.2GB/16GB (51%)
Disk: 512GB/1TB free
Uptime: 5d 12h 30m
```

---

## 📸 Files & Screenshots

```
/screenshot      Take screenshot and send image
/files           List recent files in Downloads
/upload          Upload file to PC (send file via Telegram)
/download path   Download file from PC
/screen          Alias for /screenshot
```

**Example:**
```
/screenshot
→ Receives image file

/download C:\Users\Documents\file.pdf
→ Downloads file to Telegram
```

---

## 🎮 Application Control

```
/open chrome     Open Google Chrome
/open firefox    Open Firefox
/open spotify    Open Spotify
/open steam      Open Steam
/open vlc        Open VLC Media Player
/open discord    Open Discord
/open notepad    Open Notepad
/open app_name   Open any whitelisted app
/close app_name  Close any running application
```

**Whitelisted Apps:**
- chrome, firefox, spotify, steam, vlc, discord, telegram, notepad

---

## 🔒 System Control

```
/lock            Lock screen immediately
/sleep           Put PC to sleep
/restart         Restart PC (30 second delay)
/shutdown        Shutdown PC (30 second delay)
/cancel          Cancel pending restart/shutdown
```

**Security Note:** Restart/shutdown commands give 30-second warning

---

## 📋 Event Logs & History

```
/logs            Recent system event logs
/logins          Login history (who accessed PC)
/shutdown_logs   Shutdown and restart history
/events          System events log
```

**Example Response:**
```
🔐 Login History:

User: Administrator logged in at 2024-04-20 09:30
User: Administrator logged in at 2024-04-20 08:15
User: Guest accessed at 2024-04-20 07:45
```

---

## 📱 Clipboard & Data

```
/clipboard       Show clipboard content
/clip            Alias for /clipboard
```

**Features:**
- Auto-sends clipboard when it changes (if enabled)
- Content limited to 1000 characters
- Shows as code block for formatting

---

## 🎯 Menu Buttons

Instead of typing commands, use these menu buttons in Telegram:

### ⚙️ System Control
- 📊 System Status
- 🌡️ Temperature
- 🔋 Battery
- ⚙️ Processes
- 🔒 Lock PC
- 😴 Sleep Mode
- 🔄 Restart
- ⛔ Shutdown

### 📁 Files & Media
- 📸 Screenshot
- 🎥 Screen Recording (future)
- 📁 Open Files
- 💾 Download File
- ⬆️ Upload File
- 🗑️ Delete File

### 🎮 Applications
- 🌐 Chrome
- 🦊 Firefox
- 🎵 Spotify
- 🎮 Steam
- 📝 Notepad
- 🎬 VLC
- 🔎 Search Apps
- ❌ Close App

### 📊 Monitoring
- 📋 Event Logs
- 🔐 Login History
- ⏹️ Shutdown Logs
- 🔄 System Events
- 📱 Clipboard
- 🌐 Network

---

## 💬 Message Examples

### Control Your PC

**You:** `/screenshot`  
**FRIDAY:** 📸 [sends image of your desktop]

**You:** `/open spotify`  
**FRIDAY:** ✅ Opening Spotify...

**You:** `/status`  
**FRIDAY:** 
```
📊 System Status

CPU: 72%
RAM: 12.5GB/16GB
Disk: 850GB/1TB free
Temperature: 65°C
```

**You:** `/logins`  
**FRIDAY:**
```
🔐 Login History:
• Administrator: 2024-04-20 09:30
• Administrator: 2024-04-20 08:15
• Guest: 2024-04-20 07:45
```

---

## 🔧 Configuration Commands

### Check Configuration

```bash
# Verify bot is running
/system → If responds, bot is working

# View available commands
# Use the menu buttons in Telegram
```

### Update Settings

Edit `telegram/config.json`:

```json
{
  "NOTIFICATION_SETTINGS": {
    "send_clipboard_alerts": true,
    "alert_cpu_threshold": 80
  }
}
```

Then restart FRIDAY:
```bash
python main.py
```

---

## ⚙️ Special Commands

### Start Bot
```
/start
```
Shows welcome menu and main buttons

### Help (Coming Soon)
```
/help
```
Shows this command reference

### Status Check
```
/status
```
Quick system health check

---

## 🚨 Emergency Commands

### Stop Scheduled Operations
```
/cancel
```
Cancels pending restart or shutdown

### Immediate Lock
```
/lock
```
Instantly locks screen (no delay)

---

## 📊 Response Format

All responses follow this format:

**Success:**
```
✅ Action completed successfully
Details: ...
```

**Error:**
```
❌ Error occurred
Reason: ...
Try: Alternative approach
```

**Info:**
```
📊 Information
Details: Structured data
```

---

## ⏰ Timing

| Operation | Time |
|-----------|------|
| Screenshot | ~1-2 seconds |
| System Status | ~0.5 seconds |
| File List | ~1 second |
| Login History | ~2-3 seconds |
| Restart | 30 second countdown |
| Shutdown | 30 second countdown |

---

## 🔐 Security

### Commands That Need Confirmation
- Restart
- Shutdown
- Delete File (future)

### Commands That Are Logged
ALL commands are logged for security audit:
```
C:\Users\YourName\.friday\logs\telegram_commands.log
```

### Rate Limiting
- Maximum: 10 commands per minute
- Auto-rejects if exceeded
- Prevents bot spam

---

## 💡 Pro Tips

### Faster Control
```
Use menu buttons instead of typing commands
- Tap once instead of typing /command
- Faster on mobile
```

### Clipboard Shortcuts
```
Copy text → Paste on PC via /clipboard
Or set auto-clipboard alerts in config
```

### Scheduled Operations
```
/restart → Restart with 30 second warning
/cancel → Stop it before it starts
Perfect for scheduling in Telegram's reminder
```

### Monitoring Setup
```
Use menu → 📊 Monitoring → 📋 Event Logs
Check periodically for system health
```

---

## 🚀 Getting Help

### Command Not Working?

**Step 1:** Check command spelling
```
Correct: /screenshot (all lowercase)
Wrong: /ScreenShot
```

**Step 2:** Verify you're in the right menu
```
Use menu buttons for easier access
```

**Step 3:** Check logs
```
C:\Users\YourName\.friday\logs\telegram_commands.log
```

### Bot Not Responding?

**Step 1:** Verify internet connection
**Step 2:** Restart FRIDAY
**Step 3:** Check telegram/config.json
**Step 4:** Verify User ID is correct

---

## 📚 Full Documentation

For complete setup guide, see: [TELEGRAM_BOT_SETUP.md](TELEGRAM_BOT_SETUP.md)

---

**Quick Start:**
1. Get bot token from @BotFather
2. Get your User ID from @userinfobot
3. Update `telegram/config.json`
4. Run `python main.py`
5. Open Telegram and start commanding! 🎉

---

*Last updated: April 2026*
*FRIDAY v2.0 - Telegram Bot Command Reference*
