
# SecureMail Project

## Overview
SecureMail is an application designed to read and send signed emails. It lets users read and verify emails as well as signed emails. This program was designed to verify if the email you have received is truely from the person who sent it with a signed hash signature.
This application is only a proof of concept as many features are very limited in scope and currently can only verify emails sent by this program.

## Intended Features
- Read emails: View sender, date, subject, body, and verification status of received emails.
- Send emails: Compose and send emails with recipient, subject, message content, and signature options.

## Key Packages Used
- **PySide6**: Python binding of the cross-platform GUI toolkit Qt.
- **Email**: Library for managing email messages.
- **IMAPClient**: Library for accessing and manipulating IMAP mailboxes.
- **Cryptography**: Toolkit for encryption, decryption, and signing of data.
- **google_auth**: Authentication library for accessing Google services.

## Usage
To use SecureMail, follow these steps:
1. Run the executable file
2. When prompted, login and follow the on poppup instructions.
3. When returning to the main screen choose whether to read or send emails.

### Reading Emails-The reader is limited in that it only works on text emails.
1. To read emails, click the read emails button.
2. On the popup window, each line is labeled what the content contains. It reads each email and at the bottom tells you if the email has a verified signature or not
3. To exit, close the window

### Sending Emails
1. To send emails, click the send email button.
2. On the popup window, input the receiptent email, the subject, fill in the email contents (text only) and then choose to send the email signed or unsigned.
3. To exit, close the window

## Technology Discussion
This program relies on google's oauth2 to securely log into the users email program. Once there, it contacts the gmail server itself to pull information from the google/gmail api. Through this, we are able to recover the person's email address without the person ever inputting it themselves. 
Once logged in, the reading and sending both use different packages to operate. 
The reading side relies on imapclient which connects into the gmail server once loged in using the oauth2 credentials. Here, it is able to access any email in the inbox and can read them and modify their status and labels. For our purposes, it reads each email one by one and then labels them as signed or unsigned depending on state.
On the sending side, the program uses googles own protcols to send the email. First, it hashes the email's body and then signs it with an ed25519 generated key. Upon doing so, it stores the signature in a custom header named X-Signature. In full release version, the read side would then pull this signature and verify it with a public key stored in a cloud server however for demostartion purposes, the public key is included in another custom header field. The read side then pulls these two fields and uses that to verify the signature on the email.
Due to current time and technological limitations, this unfortuantly means that this program can only work on emails sent by another user with this program. However, in future implementations, we want to be able to pull the signature from other sources to verify sender or something similar. 
