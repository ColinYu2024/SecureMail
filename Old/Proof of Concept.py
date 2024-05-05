import base64
import time
import datetime
import email
import os
import imapclient
import requests
from email.header import decode_header
import re
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request as AuthRequest
from google.oauth2.credentials import Credentials

os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = 'True'
def clean_filename(filename):
    # Remove invalid characters from the filename
    cleaned_filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
    # Truncate filename if too long
    max_filename_length = 255  # Maximum length for most file systems
    if len(cleaned_filename) > max_filename_length:
        cleaned_filename = cleaned_filename[:max_filename_length]
    return cleaned_filename


# Define the required scopes for accessing Gmail
SCOPES = ['https://mail.google.com/', 'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/userinfo.email']

creds = None
creds_path = '../credentials.json'
token_path = '../token.json'
if os.path.exists(token_path) and os.path.getsize(token_path) > 0:
    creds = Credentials.from_authorized_user_file(token_path)
# If there are no (valid) credentials available, let the user log in.
# Print if creds have expired
print(creds.expired, creds.valid, creds.expiry)
if not creds or not creds.valid:
    if not creds.expired:
        creds.refresh(AuthRequest())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            '../credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=3600)
    creds.expiry = expiry_time
    with open(token_path, 'w') as token:
        token.write(creds.to_json())
access_token = creds.token
# Initialize IMAPClient and login using OAuth2 authentication
server = imapclient.IMAPClient('imap.gmail.com', ssl=True)
email_response = requests.get(f'https://people.googleapis.com/v1/people/me?personFields=emailAddresses?', headers={'Authorization': f'Bearer {access_token}'})
email_data = email_response.json()
email_address = email_data.get('email')
server.oauth2_login(email_address, creds.token)

print("Logged in.")

while True:
    try:
        print("Checking for new emails...")
        server.select_folder("INBOX")
        messages = server.search("UNSEEN")

        # Fetch lastest email by yuaj@bc.edu
        messages = server.search(["FROM", "yuaj@bc.edu", "UNSEEN"])
        print(f"Found {len(messages)} new unread emails.")
        for msgid, data in server.fetch(messages, "RFC822").items():
            signed = False
            print("reading email")

            # Account for empty emails
            email_message = email.message_from_bytes(data[b"RFC822"])
            print("read email")
            from_ = email_message.get("From")
            subject = email_message.get("Subject")
            subject, encoding = decode_header(email_message["Subject"])[0]

            if isinstance(subject, bytes):
                # if it's a bytes, decode to str
                subject = subject.decode(encoding)
            cleaned_subject = clean_filename(subject)

            date = email_message.get('Date')

            form_, encoding = decode_header(email_message["From"])[0]
            if isinstance(form_, bytes):
                # if it's a bytes, decode to str
                form_ = form_.decode(encoding)
            cleaned_from = clean_filename(form_)

            print("Subject:", cleaned_subject)
            print("From:", cleaned_from)
            print("Date:", date)
            # Check for digital signature and public key in email headers
            if "X-Digital-Signature" not in email_message:
                print("Email is not signed. Skipping...")
            else:
                signed = True
                # Print the digital signature
                signature = email_message["X-Digital-Signature"]
                print("Digital Signature:", signature)

                # Get debug public key from email
                public_key_str = email_message["X-Public-Key-Debug"]
                public_key = None
                print("Public Key str:", public_key_str)
                try:
                    # Restore cleaned public key
                    public_key_str = "-----BEGIN PUBLIC KEY-----\n" + public_key_str + "\n-----END PUBLIC KEY-----"
                    public_key_bytes = public_key_str.encode()
                    public_key = serialization.load_pem_public_key(public_key_bytes, backend=default_backend())
                except Exception as e:
                    print("Error loading public key:", e)

                # Calculate hash of the body using SHA-256
                email_body = email_message.get_payload()
                if isinstance(email_body, list):
                    # If the email body is multipart (i.e., a list), concatenate its parts into a single string
                    email_body = ''.join(part.get_payload(decode=True).decode() for part in email_body)
                digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
                digest.update(email_body.encode())
                hash_body = digest.finalize()

                # Decrypt the signature using the public key
                signature = base64.b64decode(signature)

                # Verify the signature with ed25519
                try:
                    public_key.verify(signature, hash_body)
                    print("Signature is valid.")
                except Exception as e:
                    print("Signature is invalid:", e)

            # Save the entire email message including headers to folder emails

            # create a folder for the email
            folder_name = "emails"
            if not os.path.isdir(folder_name):
                os.mkdir(folder_name)
            with open(f"emails/{cleaned_subject}_{cleaned_from}.eml", "wb") as file:
                file.write(data[b"RFC822"])
            print("Email saved.")
            # Mark email as unread for debugging
            server.remove_flags(msgid, [b"\\Seen"])

            # Sort emails by signed/unsigned
            # Add signed label to signed emails
            if signed:
                server.add_gmail_labels(msgid, ["Signed"])
            else:
                server.add_gmail_labels(msgid, ["Unsigned"])

            # Print headers and body
            print("Headers:")
            for key, value in email_message.items():
                print(f"{key}: {value}")
            print("Body:")
            print(email_body)

        print("Waiting for 5 minutes before checking again...")
        time.sleep(300)  # Sleep for 5 minutes before checking again

    except Exception as e:
        print("An error occurred:", e)
        break

server.logout()
