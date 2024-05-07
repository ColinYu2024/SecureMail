import os
import datetime
import requests
import imapclient
import sys

from google.auth.transport.requests import Request as AuthRequest
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = 'True'

SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/userinfo.email']

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class LoginManager:
    def __init__(self, token_path=resource_path('token.json'), creds_path=resource_path('credentials.json')):
        self.token_path = token_path
        self.creds_path = creds_path
        self.server = None
        self.service = None
        self.sender_email = None
        self.creds = None
        self.login()

    def login(self):
        self.creds = self._get_credentials()
        if self.creds is None or not self.creds.valid:
            self.creds = self._refresh_credentials()
        self._save_credentials()
        self._initialize_imap()

    def _get_credentials(self):
        if os.path.exists(self.token_path) and os.path.getsize(self.token_path) > 0:
            return Credentials.from_authorized_user_file(self.token_path)
        return None

    def _refresh_credentials(self):
        if not self.creds or not self.creds.expired:
            flow = InstalledAppFlow.from_client_secrets_file(resource_path('credentials.json'), SCOPES)
            self.creds = flow.run_local_server(port=0)
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=3600)  # 1 hour
            self.creds.expiry = expiry_time
        else:
            self.creds.refresh(AuthRequest())
        return self.creds

    def _save_credentials(self):
        with open(self.token_path, 'w') as token:
            token.write(self.creds.to_json())
    
    def _initialize_imap(self):
        access_token = self.creds.token
        email_response = requests.get('https://www.googleapis.com/oauth2/v1/userinfo',
                                      headers={'Authorization': f'Bearer {access_token}'})
        email_data = email_response.json()
        self.sender_email = email_data.get('email')
        self.service = build('gmail', 'v1', credentials=self.creds)
        self.server = imapclient.IMAPClient('imap.gmail.com', ssl=True)
        self.server.oauth2_login(self.sender_email, self.creds.token)