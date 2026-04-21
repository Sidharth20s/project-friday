"""
FRIDAY AI Assistant — WhatsApp Integration
Inspired by Project JARVIS.
"""

import pywhatkit
import webbrowser
import time
from typing import Optional

CONTACTS = {
    "mom": "+1234567890",
    "dad": "+0987654321",
    "boss": "+1122334455",
}

class WhatsAppSystem:
    def __init__(self):
        pass

    def send_message(self, target: str, message: str, instant: bool = True):
        """Send a WhatsApp message."""
        # Resolve contact name to number if possible
        phone = CONTACTS.get(target.lower(), target)
        
        try:
            if instant:
                # This opens a browser tab and sends message
                pywhatkit.sendwhatmsg_instantly(phone, message, wait_time=15, tab_close=True)
                return f"WhatsApp message sent to {target}."
            else:
                # Scheduled (requires specific time, not very useful for instant assistant)
                return "Scheduled messaging not yet optimized for voice."
        except Exception as e:
            return f"Failed to send WhatsApp message: {str(e)}"

    def open_whatsapp(self):
        """Open WhatsApp Web."""
        webbrowser.open("https://web.whatsapp.com")
        return "Opening WhatsApp Web. Please scan the QR code if not logged in."

whatsapp_system = WhatsAppSystem()
