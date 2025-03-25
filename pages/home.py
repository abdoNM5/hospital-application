from PyQt5 import QtWidgets, QtGui, QtCore
# import pages.res1_rc

class HomePage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setAlignment(QtCore.Qt.AlignCenter)


        # Frame for Login Form
        self.login_frame = QtWidgets.QFrame()
        self.login_frame.setFixedSize(400, 350)  # Slightly larger for better spacing
        self.login_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0,0,0,0.8);  /* Semi-transparent white */
                border-radius: 15px;
                border: 1px solid #E0E0E0;
            }
        """)

        login_layout = QtWidgets.QVBoxLayout(self.login_frame)
        login_layout.setAlignment(QtCore.Qt.AlignCenter)
        login_layout.setSpacing(15)  # Increase spacing between elements
        login_layout.setContentsMargins(20, 20, 20, 20)  # Add padding inside the frame

        # Title
        self.title_label = QtWidgets.QLabel("Hospital Login")
        self.title_label.setFont(QtGui.QFont("Segoe UI", 18, QtGui.QFont.Bold))  # Modern font
        self.title_label.setStyleSheet("""
    QLabel {
        color: #0078D4;          /* Text color */
        background-color: transparent;  /* Transparent background */
        border: none;            /* No border */
        font-family: 'Segoe UI'; /* Modern font */
        font-size: 18px;         /* Font size */
        font-weight: bold;       /* Bold text */
    }
""")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        login_layout.addWidget(self.title_label)

        # Username Field
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #F5F5F5;
                border: 1px solid #D3D3D3;
                border-radius: 5px;
                padding-left: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #0078D4;
            }
        """)
        login_layout.addWidget(self.username_input)

        # Password Field
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFixedHeight(40)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #F5F5F5;
                border: 1px solid #D3D3D3;
                border-radius: 5px;
                padding-left: 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #0078D4;
            }
        """)
        login_layout.addWidget(self.password_input)

        # Show Password Checkbox
        self.show_password = QtWidgets.QCheckBox("Show Password")
        self.show_password.setStyleSheet("color: white; font-size: 12px;")
        self.show_password.stateChanged.connect(self.toggle_password_visibility)
        login_layout.addWidget(self.show_password)

        # Login Button
        self.login_button = QtWidgets.QPushButton("Login")
        self.login_button.setFixedHeight(45)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;
                color: white;
                font-size: 16px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #005FA3;
            }
            QPushButton:pressed {
                background-color: #004A80;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        login_layout.addWidget(self.login_button)

        # Add Login Frame to Main Layout
        self.main_layout.addWidget(self.login_frame)

    def toggle_password_visibility(self):
        if self.show_password.isChecked():
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username == "admin" and password == "password123":  # Replace with real authentication
            QtWidgets.QMessageBox.information(self, "Login Successful", "Welcome to XYZ Hospital!")
        else:
            QtWidgets.QMessageBox.warning(self, "Login Failed", "Invalid username or password.")