from PyQt5 import QtWidgets, QtGui, QtCore
import oracledb

class HomePage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: white;")  # Main background color

        # Create QLabel to hold the background image
        self.bg_label = QtWidgets.QLabel(self)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())  # Full size
        pixmap = QtGui.QPixmap(r"C:\Users\nmira\OneDrive\Documents\hosîtal2\resources\healthcare.webp")  
        self.bg_label.setPixmap(pixmap)
        self.bg_label.setScaledContents(True)  # Scale image to fit

        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setAlignment(QtCore.Qt.AlignCenter)

        # Frame for Login Form
        self.login_frame = QtWidgets.QFrame(self)
        self.login_frame.setFixedSize(400, 350)
        self.login_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 0, 0, 0.8);
                border-radius: 15px;
                border: 1px solid #E0E0E0;
            }
        """)

        login_layout = QtWidgets.QVBoxLayout(self.login_frame)
        login_layout.setAlignment(QtCore.Qt.AlignCenter)
        login_layout.setSpacing(15)
        login_layout.setContentsMargins(20, 20, 20, 20)

        # Title
        self.title_label = QtWidgets.QLabel("Hospital Login")
        self.title_label.setFont(QtGui.QFont("Segoe UI", 18, QtGui.QFont.Bold))
        self.title_label.setStyleSheet("color: #0078D4;")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        login_layout.addWidget(self.title_label)

        # Username Input
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("worker id")
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #F5F5F5;
                border: 1px solid #D3D3D3;
                border-radius: 5px;
                padding-left: 10px;
                font-size: 14px;
            }
        """)
        login_layout.addWidget(self.username_input)

        # Password Input
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFixedHeight(40)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        login_layout.addWidget(self.password_input)

        # Show Password Checkbox
        self.show_password = QtWidgets.QCheckBox("Show Password")
        self.show_password.setStyleSheet("color: white; font-size: 12px; background: transparent;")
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
        """)
        self.login_button.clicked.connect(self.handle_login)
        login_layout.addWidget(self.login_button)

        # Message Label (Initially Invisible)
        self.message_label = QtWidgets.QLabel("")
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.message_label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.8); /* Same as login frame */
            color: transparent;  /* Text invisible initially */
            border: 1px solid rgba(0, 0, 0, 0.8); /* Same as frame to blend in */
            padding: 5px;
            border-radius: 5px;
            font-size: 14px;
        """)
        self.message_label.setFixedHeight(30)  # Set height for better appearance
        self.message_label.setVisible(False)  # Hide it at the start
        login_layout.addWidget(self.message_label)  # Add below login button

        # Add Login Frame to Main Layout
        self.main_layout.addWidget(self.login_frame)

    def toggle_password_visibility(self):
        if self.show_password.isChecked():
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

    def display_message(self, message, success):
        """Displays success or failure messages on the bottom label."""
        self.message_label.setText(message)
        self.message_label.setVisible(True)  # Show the label when needed

        if success:
            self.message_label.setStyleSheet("""
                background-color: #4CAF50; /* Green background for success */
                color: white; /* White text for success */
                padding: 5px;
                border-radius: 5px;
                font-size: 14px;
            """)
        else:
            self.message_label.setStyleSheet("""
                background-color: #F44336; /* Red background for error */
                color: #D3D3D3; /* White text for error */
                padding: 5px;
                border-radius: 5px;
                font-size: 14px;
            """)

    def handle_login(self):
        worker_id = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not worker_id or not password:
            self.display_message("Please enter both Worker ID and Password.", success=False)
            return

        try:
            connection = oracledb.connect(user="system", password="Abdo2004@", dsn="localhost:1521/FREE")
            cursor = connection.cursor()

            query = "SELECT password FROM employees WHERE worker_id = :worker_id"
            cursor.execute(query, {"worker_id": worker_id})
            result = cursor.fetchone()

            if result and result[0] == password:
                self.display_message("Login Successful. Welcome!", success=True)
            else:
                self.display_message("Login Failed. Incorrect Worker ID or Password.", success=False)

        except oracledb.DatabaseError as e:
            self.display_message(f"Database Error: {str(e)}", success=False)

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def resizeEvent(self, event):
        """Ensures the background scales when resizing the window"""
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
