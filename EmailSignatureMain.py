import sys
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from EmailSignatureReaderUI import EmailViewer
from EmailSignatureSendingUi import EmailApp

class EmailSignatureMain(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Email Signature Main')
        self.setGeometry(100, 100, 500, 300)

        self.reader_button = QPushButton("Open Email Reader")
        self.sender_button = QPushButton("Open Email Sender")

        layout = QVBoxLayout()
        layout.addWidget(self.reader_button)
        layout.addWidget(self.sender_button)

        self.setLayout(layout)

        self.reader_button.clicked.connect(self.open_reader)
        self.sender_button.clicked.connect(self.open_sender)

    def open_reader(self):
        self.reader_window = EmailViewer()
        self.reader_window.show()

    def open_sender(self):
        self.sender_window = EmailApp()
        self.sender_window.show()

def main():
    app = QApplication(sys.argv)
    main_window = EmailSignatureMain()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
