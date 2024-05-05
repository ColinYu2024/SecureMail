import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLabel, QPushButton
from EmailSignatureReader import EmailHandler, Message
from datetime import datetime


class EmailViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Email Viewer')
        self.setGeometry(100, 100, 600, 400)

        self.sender_label = QLabel("From:")
        self.date_label = QLabel("Date:")
        self.subject_label = QLabel("Subject:")
        self.message_label = QLabel("Message:")
        self.message_text = QTextEdit()
        self.signature_label = QLabel("Signature:")

        self.next_email_button = QPushButton("Get Next Email")

        layout = QVBoxLayout()
        layout.addWidget(self.sender_label)
        layout.addWidget(self.date_label)
        layout.addWidget(self.subject_label)
        layout.addWidget(self.message_label)
        layout.addWidget(self.message_text)
        layout.addWidget(self.signature_label)
        layout.addWidget(self.next_email_button)

        self.setLayout(layout)

        self.next_email_button.clicked.connect(self.handle_next_email)

        self.email_handler = EmailHandler()
        self.handle_next_email()

    def handle_next_email(self):
        self.email_handler.handle_next_unread_email()
        email_data = self.email_handler.get_email_data()
        self.update_ui(email_data)

    def update_ui(self, message: Message):
        if message:
            # Format date nicely
            formatted_date = datetime.strptime(message.date, "%a, %d %b %Y %H:%M:%S %z").strftime("%B %d, %Y %I:%M %p")

            # Extract sender's email from sender
            sender_name, sender_email, _ = message.sender.split('_')
            print(sender_name, sender_email)
            sender_email = sender_email.strip('_').strip()

            self.sender_label.setText(f"From: {sender_name.strip()} ({sender_email})")
            self.date_label.setText(f"Date: {formatted_date}")
            self.subject_label.setText(f"Subject: {sender_name.strip()}")
            self.message_text.setPlainText(message.message)
            self.signature_label.setText(f"Signature: {'Yes' if message.signature else 'No'}")
        else:
            self.sender_label.setText("No new emails found.")
            self.date_label.setText("")
            self.subject_label.setText("")
            self.message_text.setPlainText("")
            self.signature_label.setText("")


def main():
    app = QApplication(sys.argv)

    email_viewer = EmailViewer()
    email_viewer.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
