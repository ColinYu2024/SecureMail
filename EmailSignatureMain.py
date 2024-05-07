import sys
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QDialog, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from EmailSignatureReaderUI import EmailViewer
from EmailSignatureSendingUi import EmailApp
from Login import LoginManager
import os

print(os.environ)  # or log this information to a file


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.creds = None
        self.server = None
        self.service = None
        self.sender_email = None

    def initUI(self):
        self.setWindowTitle('Login')
        self.setGeometry(100, 100, 500, 300)

        # Load and display logo
        logo_label = QLabel(self)
        pixmap = QPixmap(resource_path("Logo.png"))  
        pixmap = pixmap.scaledToWidth(200)  
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        self.login_button = QPushButton('Log in with Google')
        self.login_button.clicked.connect(self.handle_login)

        layout = QVBoxLayout()
        layout.addWidget(logo_label)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def handle_login(self):
        loginmanager = LoginManager()
        loginmanager.login()
        self.creds = loginmanager.creds
        self.server = loginmanager.server
        self.service = loginmanager.service
        self.sender_email = loginmanager.sender_email
        if self.server != None:
            self.accept()  # Close the login dialog and return QDialog.Accepted

class EmailSignatureMain(QWidget):
    def __init__(self, server, service, sender_email):
        super().__init__()
        self.initUI()
        self.server = server
        self.service = service
        self.sender_email = sender_email

    def initUI(self):
        self.setWindowTitle('Email Signature Main')
        self.setGeometry(100, 100, 500, 300)

        # Load and display logo
        logo_label = QLabel(self)
        pixmap = QPixmap(resource_path('Logo.png'))  
        pixmap = pixmap.scaledToWidth(200)  
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)

        self.reader_button = QPushButton("Read Emails")
        self.sender_button = QPushButton("Send Emails")

        layout = QVBoxLayout()
        layout.addWidget(logo_label)
        layout.addWidget(self.reader_button)
        layout.addWidget(self.sender_button)

        self.setLayout(layout)

        self.reader_button.clicked.connect(self.open_reader)
        self.sender_button.clicked.connect(self.open_sender)

    def open_reader(self):
        self.reader_window = EmailViewer(self.server)
        self.reader_window.show()

    def open_sender(self):
        self.sender_window = EmailApp(self.service, self.sender_email)
        self.sender_window.show()

def main():
    app = QApplication(sys.argv)

    login_dialog = LoginDialog()

    if login_dialog.exec() == QDialog.Accepted:
        server = login_dialog.server
        service = login_dialog.service
        sender_email = login_dialog.sender_email

        main_window = EmailSignatureMain(server, service, sender_email)
        main_window.show()

        sys.exit(app.exec())
    else:
        QMessageBox.warning(None, "Login Failed", "Login was not successful. Exiting application.")
        sys.exit()


if __name__ == '__main__':
    main()
