# 🤖 FRIDAY Telegram Bot Setup Guide

Complete guide to set up and configure FRIDAY Telegram Bot for remote Windows control from anywhere in the world.

---

## 📋 Quick Start (5 minutes)

### Step 1: Create Telegram Bot Token

1. **Open Telegram and find @BotFather**
   - Search for "BotFather" in Telegram
   - Click to open the official bot

2. **Create new bot**
   - Type `/newbot`
   - Name your bot: `FRIDAY` (or any name)
   - Username: `friday_windows_bot` (must be unique)
   - BotFather will give you a **TOKEN** (save this!)

3. **Example token:**
   ```
   1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg
   ```

### Step 2: Get Your User ID

1. **Find your Telegram User ID**
   - Open Telegram
   - Search for `@userinfobot`
   - Click "Start"
   - It will show your **User ID** (save this!)

2. **Or find it here:**
   - Go to: https://t.me/userinfobot
   - Click START

3. **Example User ID:**
   ```
   123456789
   ```

### Step 3: Configure FRIDAY

1. **Open** `telegram/config.json`

2. **Fill in your details:**
   ```json
   {
     "TELEGRAM_TOKEN": "1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefg",
     "USER_ID": 123456789,
     "ADMIN_IDS": [123456789]
   }
   ```

3. **Save the file**

### Step 4: Install Dependencies

```bash
pip install python-telegram-bot pyperclip
```

### Step 5: Start FRIDAY

```bash
python main.py
```

Done! 🎉 Now open Telegram and message your bot!

---

## 🎮 How to Use

### Send Commands

Open the bot in Telegram and use the menu buttons or type commands:

**System Control**
- `/system` → Full system status
- `/battery` → Battery info
- `/temp` → CPU temperature
- `/lock` → Lock screen
- `/sleep` → Sleep mode
- `/restart` → Restart PC
- `/shutdown` → Shutdown PC

**Files & Screenshots**
- `/screenshot` → Take screenshot
- `/files` → List recent files
- `/upload` → Send file to PC
- `/download <path>` → Get file from PC

**Applications**
- `/open chrome` → Open Chrome
- `/open spotify` → Open Spotify
- `/close <app>` → Close application

**Monitoring**
- `/status` → Live system status
- `/logs` → Event logs
- `/logins` → Login history
- `/clipboard` → Clipboard content
- `/network` → Network info

### Menu Buttons

Use the menu buttons in Telegram for quick access:

```
⚙️ System Control  →  [CPU, RAM, Battery, Lock, Restart, Shutdown]
📁 Files & Media   →  [Screenshot, File Manager, Upload, Download]
🎮 Applications    →  [Chrome, Firefox, Spotify, Steam, VLC]
📊 Monitoring      →  [System Status, Event Logs, Login History, Clipboard]
```

---

## 🔐 Security Features

### ✅ Built-in Protections

- **User ID Verification** - Only you can control your PC
- **Command Rate Limiting** - Prevents spam (10 commands/minute)
- **Command Logging** - All commands logged for audit trail
- **Dangerous Confirmations** - Asks before restart/shutdown
- **Clipboard Monitoring** - Optional alerts when clipboard changes
- **System Alerts** - Optional CPU/RAM/Disk usage alerts

### 🔒 Recommended Settings

**In `telegram/config.json`:**

```json
{
  "NOTIFICATION_SETTINGS": {
    "send_clipboard_alerts": true,
    "send_system_alerts": true,
    "alert_cpu_threshold": 80,
    "alert_memory_threshold": 85,
    "alert_disk_threshold": 90
  },
  "SECURITY": {
    "rate_limit_enabled": true,
    "max_commands_per_minute": 10,
    "log_all_commands": true,
    "require_confirmation_for_dangerous": true
  }
}
```

### 👥 Multiple Users (Advanced)

To allow multiple users to control your PC:

```json
{
  "ADMIN_IDS": [123456789, 987654321, 555666777]
}
```

Each user ID can send commands independently.

---

## 🚀 Advanced Features

### Remote Access Anywhere

The bot uses **Telegram's servers** for communication, so you can:
- ✅ Control your PC from anywhere (home, office, traveling)
- ✅ Access even if PC is behind a firewall
- ✅ No VPN or port forwarding needed
- ✅ Work on mobile, tablet, or another computer

### Clipboard Monitoring

When clipboard changes, FRIDAY sends the content to Telegram:

```
📋 Clipboard Updated:
https://www.example.com
```

**Disable:** Set `"send_clipboard_alerts": false` in config

### System Alerts

Get alerts when system resources are overused:

```
⚠️ High CPU Usage: 92%
Consider closing some applications
```

**Configure:** Adjust thresholds in `NOTIFICATION_SETTINGS`

### Command History

All commands are logged here:
```
C:\Users\YourName\.friday\logs\telegram_commands.log
```

View what commands were executed and when.

---

## 🐛 Troubleshooting

### Problem: "Bot not responding"

**Solution 1:** Check token in `telegram/config.json`
```bash
# Is it correct? Compare with @BotFather
```

**Solution 2:** Restart FRIDAY
```bash
# Kill and restart: python main.py
```

**Solution 3:** Check internet connection
```bash
# Telegram needs internet to work
```

### Problem: "Unauthorized access" message

**Solution:** Check User ID in config
- Go to @userinfobot
- Copy your exact User ID
- Update `telegram/config.json`
- Restart FRIDAY

### Problem: Cannot install `python-telegram-bot`

**Solution:** Use specific version
```bash
pip install python-telegram-bot==20.3
```

### Problem: Clipboard not working

**Solution:** Install pyperclip
```bash
pip install pyperclip
```

### Problem: Screenshots fail on Windows 11

**Solution:** Run as Administrator or use PIL
- Already handled in code
- Just restart FRIDAY

---

## 🔧 Configuration Reference

### Main Settings

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `TELEGRAM_TOKEN` | string | - | Your bot token from BotFather |
| `USER_ID` | integer | - | Your Telegram User ID |
| `ADMIN_IDS` | array | [USER_ID] | List of authorized user IDs |

### Allowed Commands

```json
"ALLOWED_COMMANDS": [
  "system_status",
  "battery",
  "temperature",
  "screenshot",
  "open_app",
  "close_app",
  "lock_screen",
  "sleep",
  "restart",
  "shutdown",
  "login_history",
  "shutdown_logs",
  "clipboard",
  "network_info"
]
```

### Notification Settings

```json
"NOTIFICATION_SETTINGS": {
  "send_clipboard_alerts": true,      // Send when clipboard changes
  "send_system_alerts": true,         // Alert on high usage
  "alert_cpu_threshold": 80,          // Alert when CPU > 80%
  "alert_memory_threshold": 85,       // Alert when RAM > 85%
  "alert_disk_threshold": 90          // Alert when Disk > 90%
}
```

### Security Settings

```json
"SECURITY": {
  "rate_limit_enabled": true,         // Prevent spam
  "max_commands_per_minute": 10,      // Max 10 commands/min
  "log_all_commands": true,           // Log all actions
  "require_confirmation": true        // Ask before dangerous ops
}
```

---

## 📱 API Reference

### Command Format

All commands are case-insensitive:

```
/command [arguments]
```

### System Commands

```
/system              Get full system status
/battery             Battery info (laptops only)
/temp                CPU temperature
/processes           Top 10 running processes
/uptime              How long PC running
```

### Screen Commands

```
/screenshot          Take screenshot and send
/files               List files in Downloads
/screen              Alternative to screenshot
```

### Control Commands

```
/lock                Lock screen
/sleep               Sleep mode
/restart             Restart (30 sec delay)
/shutdown            Shutdown (30 sec delay)
/cancel              Cancel restart/shutdown
```

### Info Commands

```
/logs                Event logs
/logins              Login history
/clipboard           Clipboard content
/network             Network information
/shutdown_logs       Shutdown/restart history
```

### App Commands

```
/open chrome         Open Chrome
/open spotify        Open Spotify
/open discord        Open Discord
/close <app>         Close any app
/open <app_name>     Open any whitelisted app
```

---

## 🚨 Emergency Commands

### Cancel Scheduled Shutdown

```
/cancel
```

Cancels pending restart or shutdown.

### Get Emergency Status

```
/status
```

Full system diagnostics instantly.

---

## 🎯 Use Cases

### 📌 Remote Worker

Control your office PC from home:
```
/screenshot → Check desktop
/status     → Monitor CPU usage
/clipboard  → Get copied data
```

### 💼 Server Monitoring

Keep tabs on your PC:
```
/logins     → See who's accessed PC
/logs       → Check for errors
/status     → Verify it's running
```

### 🔧 Technical Support

Help a friend fix their PC:
```
/open chrome        → Open browser
/screenshot         → See desktop
/temp               → Check temperature
/processes          → See what's running
```

### 🎮 Gaming/Media Control

```
/open spotify       → Play music
/open steam         → Launch games
/screenshot         → Screen capture
/system             → Check CPU usage
```

---

## ⚙️ Advanced Configuration

### Multiple Devices

Control multiple Windows PCs:

1. Create separate bots for each PC
   - @BotFather → `/newbot` (repeat)
   - Get a token for each PC

2. Configure each PC:
   ```json
   {
     "TELEGRAM_TOKEN": "TOKEN_FOR_PC_1",
     "USER_ID": 123456789,
     "ADMIN_IDS": [123456789]
   }
   ```

3. Create bot groups in Telegram:
   - Add all bots to a group
   - Send commands to specific bot

### Webhook Mode (Advanced)

For better performance, use webhooks instead of polling:

1. Set up HTTPS endpoint
2. Configure in `telegram/config.json`
3. Restart FRIDAY

**Note:** Requires public IP or reverse proxy

---

## 📞 Support

### Get Help

1. **Check logs:**
   ```
   C:\Users\YourName\.friday\logs\telegram_commands.log
   ```

2. **Enable debug mode:**
   ```bash
   # Edit telegram_bot.py
   logging.basicConfig(level=logging.DEBUG)
   ```

3. **Test bot:**
   ```bash
   python -c "from assistant.telegram_bot import *; print('OK')"
   ```

---

## ✨ Tips & Tricks

### 💡 Productivity

- Set up Telegram shortcuts for frequent commands
- Use iOS/Android Telegram widgets
- Create Telegram channels for notifications

### 🔒 Security Best Practices

- ✅ Keep bot token secret
- ✅ Regularly check login history
- ✅ Enable rate limiting
- ✅ Monitor command logs
- ✅ Use strong Telegram password

### ⚡ Performance

- Clipboard monitoring: every 5 seconds
- Command logging: asynchronous
- Screenshots: optimized (PNG compression)
- Rate limiting: 10 commands/minute

---

## 📚 Next Steps

1. ✅ Complete setup above
2. ✅ Test basic commands
3. ✅ Configure security settings
4. ✅ Set up notifications
5. ✅ Read troubleshooting if issues occur
6. ✅ Keep API keys safe!

---

**Happy remote controlling! 🚀**

*Last updated: April 2026*
*FRIDAY v2.0 - Telegram Bot*
