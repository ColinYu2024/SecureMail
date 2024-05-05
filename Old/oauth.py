
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
                '../credentials.json', SCOPES)
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
            pprint.pprint(msg)
            sys.exit()
            # Look for Subject and Sender Email in the headers 
            for d in headers: 
                if d['name'] == 'Subject': 
                    subject = d['value'] 
                if d['name'] == 'From': 
                    sender = d['value'] 
  
            # The Body of the message is in Encrypted format. So, we have to decode it. 
            # Get the data and decode it with base 64 decoder. 
            parts = payload.get('parts')[0] 
            data = parts['body']['data'] 
            data = data.replace("-","+").replace("_","/") 
            decoded_data = base64.b64decode(data) 
  
            # Now, the data obtained is in lxml. So, we will parse  
            # it with BeautifulSoup library 
            soup = BeautifulSoup(decoded_data , "lxml") 
            body = soup.body() 
  
            # Printing the subject, sender's email and message 
            print("Subject: ", subject) 
            print("From: ", sender) 
            print("Message: ", body) 
            print('\n')

        
            #pprint.pprint(msg)
            #print(f"From: {msg['payload']['headers'][15]['value']} Subject: {msg['payload']['headers'][19]['value']}")
            #print()
            sys.exit()
if __name__ == '__main__':
    main()
