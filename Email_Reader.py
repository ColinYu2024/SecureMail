import webbrowser

from imapclient import IMAPClient
import os
import email
from email.header import decode_header
import datetime
import pandas as pd
import credentials


def clean(text):
    return ''.join(c if c.isalnum() else '_' for c in text)


pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000
pd.set_option('display.max_colwidth', None)  # or 199


server = IMAPClient(host="imap.gmail.com")
server.login(credentials.USERNAME, credentials.PASSWORD)
print("logged in")
server.select_folder("INBOX")

server.idle()
while True:
    try:
        # Run every 5 minutes
        responses = server.idle_check(timeout=300)
        print("Server sent:", responses if responses else "nothing")
        # Pull and download first 10 unread emails and store in a list
        messages = server.search("UNSEEN")
        for msgid, data in server.fetch(messages, "RFC822").items():
            email_message = email.message_from_bytes(data[b"RFC822"])
            subject = email_message["Subject"]
            from_ = email_message["From"]
            date = email_message["Date"]
            print("Subject:", subject)
            print("From:", from_)
            print("Date:", date)
            print("=" * 100)
            for part in email_message.walk():
                if part.get_content_maintype() == "multipart":
                    continue
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
            # Download email

        if responses:
            # print('Restarted idle')
            server.idle_done()
            server.idle()
        else:
            # print('Restarted idle')
            server.idle_done()
            server.idle()
    except Exception as e:
        print(e)
        break
    #     break
server.logout()
