from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt

class LoginScreen(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login Screen")
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel("Username:", self)
        self.label.move(50, 50)

        self.label = QLabel("Password:", self)
        self.label.move(50, 100)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.move(150, 50)
        self.lineEdit.setPlaceholderText("Enter your username")

        self.lineEdit = QLineEdit(self)
        self.lineEdit.move(150, 100)
        self.lineEdit.setPlaceholderText("Enter your password")
        self.lineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        self.button = QPushButton("Login", self)
        self.button.move(150, 150)
        self.button.clicked.connect(self.login)


    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit.text()
        if username:
            print("Login successful")
        else:
            print("Login failed")
        if password == '1234':
            print("Login successful")
        else:
            print("Incorrect Password")




app = QApplication([])
window = LoginScreen()
window.show()
app.exec()

