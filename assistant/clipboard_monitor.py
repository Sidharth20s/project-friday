"""
Clipboard Monitor for FRIDAY Telegram Bot
Detects clipboard changes and sends notifications
"""

import logging
import threading
from datetime import datetime
import pyperclip

logger = logging.getLogger(__name__)


class ClipboardMonitor:
    """Monitor clipboard for changes"""
    
    def __init__(self):
        """Initialize clipboard monitor"""
        self.last_clipboard = ""
        self.last_check = datetime.now()
        self.check_interval = 5  # seconds
        self.enabled = True
    
    def get_clipboard(self) -> str:
        """
        Get current clipboard content
        
        Returns:
            str: Clipboard content
        """
        try:
            return pyperclip.paste()
        except Exception as e:
            logger.error(f"Error reading clipboard: {e}")
            return ""
    
    def set_clipboard(self, text: str) -> bool:
        """
        Set clipboard content
        
        Args:
            text: Text to set
        
        Returns:
            bool: Success status
        """
        try:
            pyperclip.copy(text)
            return True
        except Exception as e:
            logger.error(f"Error setting clipboard: {e}")
            return False
    
    def detect_change(self) -> Optional[str]:
        """
        Detect if clipboard has changed
        
        Returns:
            str: New clipboard content if changed, None otherwise
        """
        try:
            current_clipboard = self.get_clipboard()
            
            if current_clipboard != self.last_clipboard and len(current_clipboard) > 0:
                self.last_clipboard = current_clipboard
                self.last_check = datetime.now()
                return current_clipboard
            
            return None
        
        except Exception as e:
            logger.error(f"Error detecting clipboard change: {e}")
            return None
    
    def start_monitoring(self, callback=None) -> threading.Thread:
        """
        Start clipboard monitoring in background thread
        
        Args:
            callback: Function to call when clipboard changes
        
        Returns:
            threading.Thread: Monitor thread
        """
        def monitor():
            while self.enabled:
                try:
                    new_content = self.detect_change()
                    
                    if new_content and callback:
                        callback(new_content)
                    
                    threading.Event().wait(self.check_interval)
                
                except Exception as e:
                    logger.error(f"Clipboard monitor error: {e}")
                    threading.Event().wait(self.check_interval)
        
        thread = threading.Thread(target=monitor, daemon=True)
        thread.start()
        logger.info("📋 Clipboard monitor started")
        
        return thread
    
    def stop_monitoring(self) -> None:
        """Stop clipboard monitoring"""
        self.enabled = False
        logger.info("📋 Clipboard monitor stopped")
    
    def clear_history(self) -> None:
        """Clear clipboard history"""
        self.last_clipboard = ""
        logger.info("📋 Clipboard history cleared")
