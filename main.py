import sys
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from EmailSignatureReaderUI import EmailViewer
from EmailSignatureSendingUi import EmailApp

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Email Application')
        self.setGeometry(100, 100, 400, 200)

        # Load and display logo
        logo_label = QLabel(self)
        pixmap = QPixmap('Logo.png')  
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

        self.reader_button.clicked.connect(self.show_reader)
        self.sender_button.clicked.connect(self.show_sender)

    def show_reader(self):
        self.reader = EmailViewer()
        self.reader.show()

    def show_sender(self):
        self.sender = EmailApp()
        self.sender.show()

def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
