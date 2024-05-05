import json
import base64
import requests
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import requests
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend


class Keygen:
    @staticmethod
    def generate_key():
        private_key = ed25519.Ed25519PrivateKey.generate()
        return private_key, private_key.public_key()

    @staticmethod
    def sign_message(private_key, message):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(message.encode())
        signature = private_key.sign(digest.finalize())
        return base64.b64encode(signature).decode(), private_key.public_key()
    


class EmailClient:
    def __init__(self, service, sender_email):
        self.service = service
        self.sender_email = sender_email

    def send_email(self, message):
        if not self.service:
            raise ValueError("Gmail API service is not initialized. Call initialize_service first.")
        print("sending email")
        message = (self.service.users().messages().send(userId='me', body=message).execute())
        return message

    def close_connection(self):
        self.sender_email = None
        self.service = None

class EmailSender:
    def __init__(self, service, sender_email):
        self.service = service
        self.sender_email = sender_email
        self.email_client = EmailClient(self.service, sender_email)
        self.keygen = Keygen()

    def send_signed_email(self, recipient_email, subject, body):
        private_key, public_key = self.keygen.generate_key()
        signature, public_key = self.keygen.sign_message(private_key, body)
        message = self.create_message(recipient_email, self.email_client.sender_email, subject, body, signature,public_key)
        self.email_client.send_email(message)

    def create_message(self, to, sender, subject, message_text, signature, public_key):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        message['X-Digital-Signature'] = signature

        if public_key:
            public_key_str = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()
            public_key_str_cleaned = public_key_str.replace("\n", "").replace("-----BEGIN PUBLIC KEY-----", "").replace(
                "-----END PUBLIC KEY-----", "")
            message["X-Public-Key-Debug"] = public_key_str_cleaned

        message['X-Digital-Signature'] = signature

        if public_key:
            public_key_str = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ).decode()
            public_key_str_cleaned = public_key_str.replace("\n", "").replace("-----BEGIN PUBLIC KEY-----", "").replace(
                "-----END PUBLIC KEY-----", "")
            message["X-Public-Key-Debug"] = public_key_str_cleaned

        raw_message = base64.urlsafe_b64encode(message.as_bytes())
        return {'raw': raw_message.decode()}
        return {'raw': raw_message.decode()}

    def send_unsigned_email(self, recipient_email, subject, body):
        message = self.create_message(recipient_email, self.email_client.sender_email, subject, body, '', '')
        self.email_client.send_email(message)

    def close_connection(self):
        self.email_client.close_connection()
