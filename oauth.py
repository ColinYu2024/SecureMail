
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

import base64
import os
import sys
import pprint
from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    creds = None
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API to fetch UNREAD messages
    results = service.users().messages().list(userId='me', q="is:unread", maxResults=5).execute()
    messages = results.get('messages', [])

    if not messages:
        print('No unread messages found.')
    else:
        print('Unread messages:')
        for message in messages:
            # Get value of 'payload' from dictionary 'txt' 
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            payload = msg['payload'] 
            headers = payload['headers']
            subject = [header['value'] for header in headers if header['name'] == 'Subject']
            #pprint.pprint(msg)
            #sys.exit()
            # Look for Subject and Sender Email in the headers
            print(subject)
            for d in headers:
                #print(d['name'])
                if d['name'] == 'X-Digital-Signature': 
                    print(d['value'])
            print()  

        
            #pprint.pprint(msg)
            #print(f"From: {msg['payload']['headers'][15]['value']} Subject: {msg['payload']['headers'][19]['value']}")
            #print()
if __name__ == '__main__':
    main()
