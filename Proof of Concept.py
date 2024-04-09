import base64
import time
import email
import os
from imapclient import IMAPClient
from email.header import decode_header
import re
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import credentials


def clean_filename(filename):
    # Remove invalid characters from the filename
    cleaned_filename = re.sub(r'[\\/:*?"<>|]', '_', filename)
    # Truncate filename if too long
    max_filename_length = 255  # Maximum length for most file systems
    if len(cleaned_filename) > max_filename_length:
        cleaned_filename = cleaned_filename[:max_filename_length]
    return cleaned_filename




server = IMAPClient(credentials.HOST, use_uid=True, ssl=True)
server.login(credentials.USERNAME, credentials.PASSWORD)
print("Logged in.")

while True:
    try:
        print("Checking for new emails...")
        server.select_folder("INBOX")
        #messages = server.search("UNSEEN")

        # Fetch lastest email by yuaj@bc.edu
        messages = server.search(["FROM", "yuaj@bc.edu", "UNSEEN"])
        print(f"Found {len(messages)} new unread emails.")
        for msgid, data in server.fetch(messages[:1], "RFC822").items():
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

            # Verify the signature
            try:
                public_key.verify(
                    signature,
                    hash_body,
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=padding.PSS.MAX_LENGTH
                    ),
                    hashes.SHA256()
                )
                print("Signature verified.")
            except Exception as e:
                print("Signature verification failed:", e)

            # Save the entire email message including headers to folder emails

            #create a folder for the email
            folder_name = "emails"
            if not os.path.isdir(folder_name):
                os.mkdir(folder_name)
            with open(f"emails/{cleaned_subject}_{cleaned_from}.eml", "wb") as file:
                file.write(data[b"RFC822"])
            print("Email saved.")
            # Mark email as unread for debugging
            server.remove_flags(msgid, [b"\\Seen"])

        print("Waiting for 5 minutes before checking again...")
        time.sleep(300)  # Sleep for 5 minutes before checking again

    except Exception as e:
        print("An error occurred:", e)
        break

server.logout()
