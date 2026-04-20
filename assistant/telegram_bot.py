"""
FRIDAY Telegram Bot - Windows Remote Control
Enables full Windows control from Telegram anywhere in the world
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Optional
from pathlib import Path

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode

from .telegram_commands import TelegramCommands
from .telegram_auth import validate_user, log_command
from .clipboard_monitor import ClipboardMonitor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FridayTelegramBot:
    """Main Telegram Bot Handler"""
    
    def __init__(self, config_path: str = None):
        """Initialize telegram bot"""
        self.config = self._load_config(config_path)
        self.token = self.config.get("TELEGRAM_TOKEN")
        self.user_id = self.config.get("USER_ID")
        self.admin_ids = self.config.get("ADMIN_IDS", [self.user_id])
        
        if not self.token or not self.user_id:
            raise ValueError("TELEGRAM_TOKEN and USER_ID required in config")
        
        # Initialize components
        self.commands = TelegramCommands()
        self.clipboard_monitor = ClipboardMonitor()
        self.app = None
        
    def _load_config(self, config_path: str = None) -> dict:
        """Load configuration from JSON file"""
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "..", "telegram", "config.json")
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            return {}
    
    async def start_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command"""
        if not validate_user(update.effective_user.id, self.admin_ids):
            await update.message.reply_text("❌ Unauthorized access! Your ID has been logged.")
            log_command(update.effective_user.id, "/start", "UNAUTHORIZED", "User not in admin list")
            return
        
        welcome_text = """
🤖 **Welcome to FRIDAY Bot!**

I can control your Windows PC from anywhere in the world.

🎯 **Main Commands:**
• **System Control** - CPU, RAM, processes, temperature
• **Files & Media** - Screenshots, file management
• **Apps** - Open/close applications
• **Calendar & Tasks** - Events and reminders
• **Monitoring** - Real-time system alerts

Tap the menu below to get started! 👇
        """
        
        keyboard = self._get_main_menu()
        await update.message.reply_text(
            welcome_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard
        )
        
        log_command(update.effective_user.id, "/start", "SUCCESS", "User logged in")
    
    async def system_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """System control menu"""
        if not validate_user(update.effective_user.id, self.admin_ids):
            return
        
        keyboard = ReplyKeyboardMarkup([
            ["📊 System Status", "🌡️ Temperature"],
            ["🔋 Battery", "⚙️ Processes"],
            ["🔒 Lock PC", "😴 Sleep Mode"],
            ["🔄 Restart", "⛔ Shutdown"],
            ["↩️ Back to Menu"]
        ], resize_keyboard=True)
        
        await update.message.reply_text(
            "⚙️ **System Control Menu**\n\nSelect an option:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard
        )
    
    async def files_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Files & media menu"""
        if not validate_user(update.effective_user.id, self.admin_ids):
            return
        
        keyboard = ReplyKeyboardMarkup([
            ["📸 Screenshot", "🎥 Screen Recording"],
            ["📁 Open Files", "💾 Download File"],
            ["⬆️ Upload File", "🗑️ Delete File"],
            ["↩️ Back to Menu"]
        ], resize_keyboard=True)
        
        await update.message.reply_text(
            "📁 **Files & Media Menu**\n\nSelect an option:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard
        )
    
    async def apps_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Applications menu"""
        if not validate_user(update.effective_user.id, self.admin_ids):
            return
        
        keyboard = ReplyKeyboardMarkup([
            ["🌐 Chrome", "🦊 Firefox"],
            ["🎵 Spotify", "🎮 Steam"],
            ["📝 Notepad", "🎬 VLC"],
            ["🔎 Search Apps", "❌ Close App"],
            ["↩️ Back to Menu"]
        ], resize_keyboard=True)
        
        await update.message.reply_text(
            "🎮 **Applications Menu**\n\nSelect an option:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard
        )
    
    async def monitoring_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """System monitoring menu"""
        if not validate_user(update.effective_user.id, self.admin_ids):
            return
        
        keyboard = ReplyKeyboardMarkup([
            ["📊 Live Dashboard", "🚨 Alerts"],
            ["📋 Event Logs", "🔐 Login History"],
            ["⏹️ Shutdown Logs", "🔄 System Events"],
            ["📱 Clipboard", "🌐 Network"],
            ["↩️ Back to Menu"]
        ], resize_keyboard=True)
        
        await update.message.reply_text(
            "📊 **Monitoring Menu**\n\nSelect an option:",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=keyboard
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle all messages and menu selections"""
        if not validate_user(update.effective_user.id, self.admin_ids):
            return
        
        text = update.message.text
        
        # Main menu routing
        if text == "⚙️ System Control":
            await self.system_menu(update, context)
        elif text == "📁 Files & Media":
            await self.files_menu(update, context)
        elif text == "🎮 Applications":
            await self.apps_menu(update, context)
        elif text == "📊 Monitoring":
            await self.monitoring_menu(update, context)
        
        # System commands
        elif text == "📊 System Status":
            await self.commands.get_system_status(update, context)
        elif text == "🌡️ Temperature":
            await self.commands.get_temperature(update, context)
        elif text == "🔋 Battery":
            await self.commands.get_battery(update, context)
        elif text == "⚙️ Processes":
            await self.commands.list_processes(update, context)
        elif text == "🔒 Lock PC":
            await self.commands.lock_screen(update, context)
        elif text == "😴 Sleep Mode":
            await self.commands.sleep_pc(update, context)
        elif text == "🔄 Restart":
            await self.commands.restart_pc(update, context)
        elif text == "⛔ Shutdown":
            await self.commands.shutdown_pc(update, context)
        
        # Files commands
        elif text == "📸 Screenshot":
            await self.commands.take_screenshot(update, context)
        elif text == "📁 Open Files":
            await self.commands.list_files(update, context)
        elif text == "⬆️ Upload File":
            await update.message.reply_text("📤 Send me a file to upload to your PC!")
        elif text == "💾 Download File":
            await update.message.reply_text("📥 Send the file path you want to download (e.g., C:\\Users\\Downloads\\file.pdf)")
        elif text == "🗑️ Delete File":
            await update.message.reply_text("🗑️ Send the file path you want to delete")
        
        # Apps commands
        elif text == "🌐 Chrome":
            await self.commands.open_app(update, context, "chrome")
        elif text == "🦊 Firefox":
            await self.commands.open_app(update, context, "firefox")
        elif text == "🎵 Spotify":
            await self.commands.open_app(update, context, "spotify")
        elif text == "🎮 Steam":
            await self.commands.open_app(update, context, "steam")
        elif text == "📝 Notepad":
            await self.commands.open_app(update, context, "notepad")
        elif text == "🎬 VLC":
            await self.commands.open_app(update, context, "vlc")
        elif text == "❌ Close App":
            await update.message.reply_text("❌ Send the app name you want to close (e.g., Chrome, Spotify)")
        
        # Monitoring commands
        elif text == "📋 Event Logs":
            await self.commands.get_event_logs(update, context)
        elif text == "🔐 Login History":
            await self.commands.get_login_history(update, context)
        elif text == "⏹️ Shutdown Logs":
            await self.commands.get_shutdown_logs(update, context)
        elif text == "🔄 System Events":
            await self.commands.get_system_events(update, context)
        elif text == "📱 Clipboard":
            await self.commands.get_clipboard(update, context)
        elif text == "🌐 Network":
            await self.commands.get_network_info(update, context)
        elif text == "↩️ Back to Menu":
            keyboard = self._get_main_menu()
            await update.message.reply_text(
                "🏠 **Main Menu**",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=keyboard
            )
        else:
            # Custom command handling
            if text.startswith("/"):
                await self.commands.handle_custom_command(update, context, text)
            else:
                await update.message.reply_text(
                    "I didn't understand that. Please use the menu buttons or type a command."
                )
    
    async def handle_file_upload(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle file uploads"""
        if not validate_user(update.effective_user.id, self.admin_ids):
            return
        
        await self.commands.handle_file_upload(update, context)
    
    def _get_main_menu(self) -> ReplyKeyboardMarkup:
        """Get main menu keyboard"""
        keyboard = ReplyKeyboardMarkup([
            ["⚙️ System Control", "📁 Files & Media"],
            ["🎮 Applications", "📊 Monitoring"],
        ], resize_keyboard=True)
        return keyboard
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ An error occurred. Please try again."
            )
    
    def setup_handlers(self) -> None:
        """Setup all message handlers"""
        # Command handlers
        self.app.add_handler(CommandHandler("start", self.start_handler))
        
        # Message handlers
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.app.add_handler(MessageHandler(filters.Document.ALL, self.handle_file_upload))
        
        # Error handler
        self.app.add_error_handler(self.error_handler)
    
    async def start_clipboard_monitor(self) -> None:
        """Start clipboard monitoring in background"""
        while True:
            try:
                # Use detect_change to only alert on NEW clipboard content
                new_content = self.clipboard_monitor.detect_change()
                if new_content:
                    # Send to user if new content detected
                    await self.send_to_user(
                        f"📋 **Clipboard Updated:**\n\n`{new_content[:500]}`",
                        parse_mode=ParseMode.MARKDOWN
                    )
                await asyncio.sleep(5)  # Check every 5 seconds
            except Exception as e:
                logger.error(f"Clipboard monitor error: {e}")
                await asyncio.sleep(10)
    
    async def send_to_user(self, message: str, parse_mode: str = None) -> None:
        """Send message to authenticated user"""
        try:
            await self.app.bot.send_message(
                chat_id=self.user_id,
                text=message,
                parse_mode=parse_mode
            )
        except Exception as e:
            logger.error(f"Failed to send message to user: {e}")
    
    async def start(self) -> None:
        """Start the bot"""
        self.app = Application.builder().token(self.token).build()
        self.setup_handlers()
        
        logger.info("🤖 FRIDAY Telegram Bot starting...")
        logger.info(f"✅ Connected to Telegram")
        logger.info(f"✅ User ID: {self.user_id}")
        logger.info(f"✅ Admin IDs: {self.admin_ids}")
        
        # Start clipboard monitor in background
        asyncio.create_task(self.start_clipboard_monitor())
        
        # Start polling
        await self.app.run_polling()
    
    def run(self) -> None:
        """Run bot (blocking)"""
        asyncio.run(self.start())


def start_telegram_bot(config_path: str = None) -> None:
    """Entry point for starting telegram bot"""
    try:
        bot = FridayTelegramBot(config_path)
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start Telegram bot: {e}")
        raise
