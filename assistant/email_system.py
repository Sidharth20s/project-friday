"""
FRIDAY AI Assistant — Email Operations
Handles sending and reading emails.
"""

import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import os
from assistant.config import EMAIL_ADDRESS, EMAIL_PASSWORD

class EmailSystem:
    def __init__(self, address: str = None, password: str = None):
        self.address = address or EMAIL_ADDRESS
        self.password = password or EMAIL_PASSWORD
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.imap_server = "imap.gmail.com"

    def send_email(self, to: str, subject: str, body: str) -> str:
        """Send an email."""
        if not self.address or not self.password:
            return "Email credentials not configured in .env"

        try:
            msg = MIMEMultipart()
            msg['From'] = self.address
            msg['To'] = to
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.address, self.password)
            server.send_message(msg)
            server.quit()
            return f"Email sent to {to}."
        except Exception as e:
            return f"Failed to send email: {str(e)}"

    def check_unread(self) -> str:
        """Count unread emails."""
        if not self.address or not self.password:
            return "Email credentials not configured."

        try:
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.address, self.password)
            mail.select("inbox")
            
            _, messages = mail.search(None, 'UNSEEN')
            unread_count = len(messages[0].split())
            mail.logout()
            
            if unread_count == 0:
                return "You have no unread emails, Boss."
            return f"You have {unread_count} unread emails."
        except Exception as e:
            return f"Could not check emails: {str(e)}"

email_system = EmailSystem()
