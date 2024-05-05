import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLineEdit, QLabel, QMessageBox
from EmailSignatureSender import EmailSender

class EmailApp(QWidget):
    def __init__(self, service, sender_email):
        super().__init__()
        self.service = service
        self.sender_email = sender_email
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Email Sender')
        self.setGeometry(100, 100, 400, 300)

        self.recipient_label = QLabel("Recipient Email:")
        self.recipient_line_edit = QLineEdit()

        self.subject_label = QLabel("Subject:")
        self.subject_line_edit = QLineEdit()

        self.message_label = QLabel("Message:")
        self.text_edit = QTextEdit()

        self.send_signed_button = QPushButton('Send Signed')
        self.send_unsigned_button = QPushButton('Send Unsigned')

        layout = QVBoxLayout()
        layout.addWidget(self.recipient_label)
        layout.addWidget(self.recipient_line_edit)
        layout.addWidget(self.subject_label)
        layout.addWidget(self.subject_line_edit)
        layout.addWidget(self.message_label)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.send_signed_button)
        layout.addWidget(self.send_unsigned_button)

        self.setLayout(layout)

        self.send_signed_button.clicked.connect(self.send_signed_email)
        self.send_unsigned_button.clicked.connect(self.send_unsigned_email)

    def send_signed_email(self):
        recipient_email = self.recipient_line_edit.text()
        subject = self.subject_line_edit.text()
        message = self.text_edit.toPlainText()
        if message:
            try:
                email_sender = EmailSender(self.service, self.sender_email)
                email_sender.send_signed_email(recipient_email, subject, message)
                QMessageBox.information(self, "Success", "Signed email sent successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error sending signed email: {e}")
        else:
            QMessageBox.warning(self, "Error", "Please type a message.")

    def send_unsigned_email(self):
        recipient_email = self.recipient_line_edit.text()
        subject = self.subject_line_edit.text()
        message = self.text_edit.toPlainText()
        if message:
            try:
                email_sender = EmailSender(self.service, self.sender_email)
                email_sender.send_unsigned_email(recipient_email, subject, message)
                QMessageBox.information(self, "Success", "Unsigned email sent successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error sending unsigned email: {e}")
        else:
            QMessageBox.warning(self, "Error", "Please type a message.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    email_app = EmailApp()
    email_app.show()
    sys.exit(app.exec())
