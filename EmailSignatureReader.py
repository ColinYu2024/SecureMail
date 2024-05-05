import os
import re
import base64
from email.header import decode_header
from email.policy import default as email_default_policy
from email.parser import BytesParser
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

from dataclasses import dataclass

os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = 'True'

SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/userinfo.email']

@dataclass
class Message:
    sender: str
    date: str
    subject: str
    message: str
    signature: bool = False

class EmailManager:
    def __init__(self, server):
        self.server = server

    def fetch_unread_emails(self):
        if self.server is None:
            raise ValueError("IMAP server not initialized.")
        self.server.select_folder("INBOX")
        return self.server.search("UNSEEN")

    def fetch_email_data(self, msgid):
        return self.server.fetch(msgid, "RFC822").items()

class EmailProcessor:
    def __init__(self):
        pass

    @staticmethod
    def clean_filename(filename):
        cleaned_filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
        max_filename_length = 255
        if len(cleaned_filename) > max_filename_length:
            cleaned_filename = cleaned_filename[:max_filename_length]
        return cleaned_filename

    @staticmethod
    def decode_email_header(header):
        value, encoding = decode_header(header)[0]
        if isinstance(value, bytes):
            value = value.decode(encoding)
        return value

    @staticmethod
    def decrypt_signature(public_key_str, email_body, signature):
        try:
            public_key_str = "-----BEGIN PUBLIC KEY-----\n" + public_key_str + "\n-----END PUBLIC KEY-----"
            public_key_bytes = public_key_str.encode()
            public_key = serialization.load_pem_public_key(public_key_bytes, backend=default_backend())
            digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
            digest.update(email_body.encode())
            hash_body = digest.finalize()
            signature = base64.b64decode(signature)
            public_key.verify(signature, hash_body)
            return True
        except Exception as e:
            print("Error verifying signature:", e)
            return False

class EmailHandler:
    def __init__(self, server):
        self.server = server
        self.email_manager = EmailManager(server)
        self.email_processor = EmailProcessor()
        self.current_email_data = None
        self.unread_emails = []
    
    def handle_next_unread_email(self):
        try:
            unread_emails = self.email_manager.fetch_unread_emails()
            if unread_emails:
                # Sort the unread emails by date in descending order to get the most recent one
                unread_emails.sort(reverse=True)
                for msgid in unread_emails:
                    self.process_email(msgid)
                    break  # Process only the most recent unread email
            else:
                print("No unread emails found. Exiting...")
        except Exception as e:
            print("An error occurred:", e)
        
    def process_email(self, msgid):
        try:
            email_data = self.email_manager.fetch_email_data(msgid)
            for msgid, data in email_data:
                email_message = BytesParser(policy=email_default_policy).parsebytes(data[b"RFC822"])
                from_ = email_message.get("From")
                subject = self.email_processor.decode_email_header(email_message.get("Subject"))
                cleaned_subject = self.email_processor.clean_filename(subject)
                date = email_message.get('Date')
                cleaned_from = self.email_processor.clean_filename(from_)
                print("Subject:", cleaned_subject)
                print("From:", cleaned_from)
                print("Date:", date)
                email_body = None  # Initialize email_body
                for part in email_message.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        email_body = part.get_payload(decode=True).decode()
                        break

                if email_body and email_body.strip():  # Check if email_body is not empty
                    signature = email_message.get("X-Digital-Signature", None)
                    if signature:
                        public_key_str = email_message.get("X-Public-Key-Debug")
                        if self.email_processor.decrypt_signature(public_key_str, email_body, signature):
                            print("Signature is valid.")
                            self.label_email(msgid, public_key_str, email_body, signature)  # Pass signature details
                        else:
                            print("Signature is invalid.")
                    else:
                        print("Signature not found. Assuming email is not signed.")
                        self.label_email(msgid, None, email_body, None)
                    self.current_email_data = Message(cleaned_from, date, cleaned_subject, email_body, bool(signature))
                else:
                    print("Signature not found. Assuming email is not signed.")
                    self.label_email(msgid, None, email_body, None)
                    print("This email has no text.")
                    self.current_email_data = Message(cleaned_from, date, cleaned_subject, email_body, False)
        except Exception as e:
            print("Error processing email:", e)

    def label_email(self, msgid, public_key_str, email_body, signature):
        server = self.email_manager.server
        if server is None:
            raise ValueError("IMAP server not initialized.")
        if self.email_processor.decrypt_signature(public_key_str, email_body, signature):
            server.add_gmail_labels(msgid, ["Signed"])
        else:
            server.add_gmail_labels(msgid, ["Unsigned"])

    def get_email_data(self):
        return self.current_email_data
