import os
import json
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import requests

class EmailClient:
    def __init__(self, creds_path='cred.json', token_path='token.json'):
        self.creds_path = creds_path
        self.token_path = token_path
        self.sender_email = None
        self.service = None

    def _get_credentials(self):
        return Credentials.from_authorized_user_file(self.token_path)

    def initialize_service(self):
        creds = self._get_credentials()
        access_token = creds.token
        email_response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo',
                                      headers={'Authorization': f'Bearer {access_token}'})
        email_data = email_response.json()
        self.sender_email = email_data.get('email')
        self.service = build('gmail', 'v1', credentials=creds)

    def send_email(self, message):
        if not self.service:
            raise ValueError("Gmail API service is not initialized. Call initialize_service first.")
        print("sending email")
        message = (self.service.users().messages().send(userId='me', body=message)
                   .execute())
        return message

    def close_connection(self):
        self.sender_email = None
        self.service = None

    def load_credentials(self):
        with open(self.creds_path, 'r') as creds_file:
            return json.load(creds_file)

class EmailSender:
    def __init__(self, creds_path='cred.json', token_path='token.json'):
        self.email_client = EmailClient(creds_path, token_path)

    def send_signed_email(self, recipient_email, subject, body):
        self.email_client.initialize_service()
        message = self.create_message(recipient_email, self.email_client.sender_email, subject, body)
        self.email_client.send_email(message)

    def create_message(self, to, sender, subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes())
        raw_message = raw_message.decode()
        return {'raw': raw_message}

    def send_unsigned_email(self, recipient_email, subject, body):
        self.email_client.initialize_service()
        message = self.create_message(recipient_email, self.email_client.sender_email, subject, body)
        self.email_client.send_email(message)

    def close_connection(self):
        self.email_client.close_connection()