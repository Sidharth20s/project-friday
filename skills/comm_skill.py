from assistant.skills import Skill
from assistant.whatsapp import whatsapp_system
from assistant.email_system import email_system
import re

class CommunicationSkill(Skill):
    def __init__(self):
        super().__init__()
        self.description = "Handles WhatsApp and Email"
        self.keywords = ["whatsapp", "message", "email", "mail", "send"]
        self.priority = 80

    def execute(self, command: str, context: dict = None) -> str:
        cmd = command.lower()
        
        # WhatsApp logic
        if "whatsapp" in cmd:
            if "open" in cmd:
                return whatsapp_system.open_whatsapp()
            
            # WhatsApp message to [X] saying [Y]
            msg_match = re.search(r"whatsapp\s+(?:message\s+)?to\s+([\w\d+]+)\s+(?:saying|msg|texting)?\s+(.*)", cmd)
            if msg_match:
                target = msg_match.group(1)
                message = msg_match.group(2)
                return whatsapp_system.send_message(target, message)
            
            return "I can send WhatsApp messages or open WhatsApp Web. Try: 'WhatsApp message to mom saying hello'."

        # Email logic
        if "email" in cmd or "mail" in cmd:
            if "check" in cmd or "unread" in cmd:
                return email_system.check_unread()
            
            # Send email to [X] subject [Y] body [Z]
            # Simple version for now
            email_match = re.search(r"email\s+to\s+([\w@.-]+)\s+(?:saying|about)?\s+(.*)", cmd)
            if email_match:
                to = email_match.group(1)
                body = email_match.group(2)
                return email_system.send_email(to, "Message from FRIDAY", body)

            return "I can check your inbox or send emails. Try: 'How many unread emails?'"
            
        return "Communication systems online. How can I help?"
