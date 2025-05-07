import imaplib
import email
from email.header import decode_header
import re
import os
from dotenv import load_dotenv
import logging
from typing import List, Dict

load_dotenv()

class OutlookEmailProcessor:
    def __init__(self):
        self.imap_server = os.getenv("OUTLOOK_IMAP_SERVER", "outlook.office365.com")
        self.username = os.getenv("OUTLOOK_EMAIL")
        self.password = os.getenv("OUTLOOK_PASSWORD")
        
        if not all([self.username, self.password]):
            raise ValueError("Outlook credentials missing in .env")

    def fetch_emails(self, limit=10) -> List[Dict]:
        emails = []
        
        try:
            with imaplib.IMAP4_SSL(self.imap_server) as mail:
                mail.login(self.username, self.password)
                mail.select("inbox")

                # Search for unread emails with "error" or "issue"
                status, messages = mail.search(None, '(UNSEEN SUBJECT "error" SUBJECT "issue")')
                if status != "OK":
                    return emails

                email_ids = messages[0].split()[:limit]
                
                for email_id in email_ids:
                    status, msg_data = mail.fetch(email_id, "(RFC822)")
                    if status != "OK":
                        continue

                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8")

                    emails.append({
                        "subject": subject,
                        "body": self._get_email_body(msg),
                        "error_message": self._extract_error(msg),
                        "resolution": "",
                    })

                    # Mark as read
                    mail.store(email_id, '+FLAGS', '\\Seen')

        except Exception as e:
            logging.error(f"IMAP Error: {e}")
            raise

        return emails

    def _get_email_body(self, msg) -> str:
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        else:
            return msg.get_payload(decode=True).decode()
        return ""


# add here any custom pattern 
    def _extract_error(self, msg) -> str:
        body = self._get_email_body(msg)
        error_patterns = [r"Error: (.+)", r"Exception: (.+)", r"Failed to (.+)"]
        for pattern in error_patterns:
            match = re.search(pattern, body)
            if match:
                return match.group(1)
        return "No specific error found"