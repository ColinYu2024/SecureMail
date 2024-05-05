
# TBD Project

## Overview
TBD is an application designed to read and send signed emails. It lets users read and verify emails as well as signed emails. Due to time limitations, this only works for programs signed and sent by this program.

## Features
- Read emails: View sender, date, subject, body, and verification status of received emails.
- Send emails: Compose and send emails with recipient, subject, message content, and signature options.
- User Authentication: Secure login mechanism for accessing email functionalities.

## Key Packages Used
- **PySide6**: Python binding of the cross-platform GUI toolkit Qt.
- **Email**: Library for managing email messages.
- **IMAPClient**: Library for accessing and manipulating IMAP mailboxes.
- **Cryptography**: Toolkit for encryption, decryption, and signing of data.
- **google_auth**: Authentication library for accessing Google services.

## Usage
To use TBD, follow these steps:
1. Run the executable file
2. When prompted, login and follow the on poppup instructions.
3. When returning to the main screen choose whether to read or send emails.

### Reading Emails
1. To read emails, click the read emails button.
2. On the popup window, each line is labeled what the content contains. It reads each email and at the bottom tells you if the email has a verified signature or not
3. To exit, close the window

### Sending Emails
1. To send emails, click the send email button.
2. On the popup window, input the receiptent email, the subject, fill in the email contents (text only) and then choose to send the email signed or unsigned.
3. To exit, close the window
