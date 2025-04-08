import sys
import time
from PyQt5 import QtWidgets, QtGui, QtCore
import oracledb

# New Imports for workspace widgets
from .patient import PatientWidget


# ------------------------- HomePage (Login Window) -------------------------
class HomePage(QtWidgets.QWidget):
    def __init__(self, main_window=None, parent=None):
        super().__init__(parent)
        self.main_window = main_window  # Reference to the QStackedWidget
        print("HomePage initialized with main_window:", self.main_window)
        self.is_signup_mode = False  # Track whether we're in login or signup mode
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: white;")  # Main background color

        # Create QLabel to hold the background image
        self.bg_label = QtWidgets.QLabel(self)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        pixmap = QtGui.QPixmap("resources/hospital-bg3.jpg")
        self.bg_label.setPixmap(pixmap)
        self.bg_label.setScaledContents(True)

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

        # Additional fields for signup (initially hidden)
        self.fullname_input = QtWidgets.QLineEdit()
        self.fullname_input.setPlaceholderText("Full Name")
        self.fullname_input.setFixedHeight(40)
        self.fullname_input.setStyleSheet("""
            QLineEdit {
                background-color: #F5F5F5;
                border: 1px solid #D3D3D3;
                border-radius: 5px;
                padding-left: 10px;
                font-size: 14px;
            }
        """)
        self.fullname_input.setVisible(False)
        login_layout.addWidget(self.fullname_input)

        self.role_input = QtWidgets.QComboBox()
        self.role_input.addItems(["Doctor", "Nurse", "Surgeon", "Paramedic"])
        self.role_input.setFixedHeight(40)
        self.role_input.setStyleSheet("""
            QComboBox {
                background-color: #F5F5F5;
                border: 1px solid #D3D3D3;
                border-radius: 5px;
                padding-left: 10px;
                font-size: 14px;
            }
            QComboBox QAbstractItemView {
                background-color: white;  /* change dropdown background */
                color: black;             /* text color of dropdown items */
                selection-background-color: #87CEFA; /* background when item is selected */
                selection-color: black;   /* text color when selected */
            }
        """)
        self.role_input.setVisible(False)
        login_layout.addWidget(self.role_input)

        self.phone_input = QtWidgets.QLineEdit()
        self.phone_input.setPlaceholderText("Phone Number")
        self.phone_input.setFixedHeight(40)
        self.phone_input.setStyleSheet("""
            QLineEdit {
                background-color: #F5F5F5;
                border: 1px solid #D3D3D3;
                border-radius: 5px;
                padding-left: 10px;
                font-size: 14px;
            }
        """)
        self.phone_input.setVisible(False)
        login_layout.addWidget(self.phone_input)

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

        # Create a horizontal layout for the buttons
        btn_layout = QtWidgets.QHBoxLayout()
        
        # Login Button
        self.login_button = QtWidgets.QPushButton("Login")
        self.login_button.setFixedSize(100, 40)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;
                color: white;
                font-size: 16px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        btn_layout.addWidget(self.login_button, alignment=QtCore.Qt.AlignLeft)
        
        # Sign Up Button
        self.signup_button = QtWidgets.QPushButton("Sign Up")
        self.signup_button.setFixedSize(100, 40)
        self.signup_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        self.signup_button.clicked.connect(self.toggle_signup_mode)
        btn_layout.addWidget(self.signup_button, alignment=QtCore.Qt.AlignRight)
        
        login_layout.addLayout(btn_layout)

        # Message Label (Initially Invisible)
        self.message_label = QtWidgets.QLabel("")
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.message_label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.8);
            color: transparent;
            border: 1px solid rgba(0, 0, 0, 0.8);
            padding: 5px;
            border-radius: 5px;
            font-size: 14px;
        """)
        self.message_label.setFixedHeight(30)
        self.message_label.setVisible(False)
        login_layout.addWidget(self.message_label)

        # Add Login Frame to Main Layout
        self.main_layout.addWidget(self.login_frame)

    def toggle_password_visibility(self):
        if self.show_password.isChecked():
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

    def toggle_signup_mode(self):
        self.is_signup_mode = not self.is_signup_mode
        
        # Update UI based on mode
        if self.is_signup_mode:
            self.title_label.setText("Hospital Sign Up")
            self.login_button.setText("Cancel")
            self.signup_button.setText("Register")
            self.fullname_input.setVisible(True)
            self.role_input.setVisible(True)
            self.phone_input.setVisible(True)
            # Adjust frame size to fit all elements
            self.login_frame.setFixedSize(400, 500)
            # Change button function
            self.signup_button.clicked.disconnect()
            self.signup_button.clicked.connect(self.handle_signup)
        else:
            self.title_label.setText("Hospital Login")
            self.login_button.setText("Login")
            self.signup_button.setText("Sign Up")
            self.fullname_input.setVisible(False)
            self.role_input.setVisible(False)
            self.phone_input.setVisible(False)
            # Reset frame size
            self.login_frame.setFixedSize(400, 350)
            # Reset button function
            self.signup_button.clicked.disconnect()
            self.signup_button.clicked.connect(self.toggle_signup_mode)
            
        # Clear any previous messages
        self.message_label.setVisible(False)

    def display_message(self, message, success):
        self.message_label.setText(message)
        self.message_label.setVisible(True)
        if success:
            self.message_label.setStyleSheet("""
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border-radius: 5px;
                font-size: 14px;
            """)
        else:
            self.message_label.setStyleSheet("""
                background-color: #F44336;
                color: #D3D3D3;
                padding: 5px;
                border-radius: 5px;
                font-size: 14px;
            """)

    def handle_login(self):
        # Handle cancel button press when in signup mode
        if self.is_signup_mode:
            self.toggle_signup_mode()
            return
        
        print("handle_login() called")
        worker_id = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not worker_id or not password:
            print("Missing worker_id or password")
            self.display_message("Please enter both Worker ID and Password.", success=False)
            return

        try:
            print("Attempting database connection...")
            connection = oracledb.connect(user="system", password="Abdo2004@", dsn="localhost:1521/FREE")
            cursor = connection.cursor()
            
            # Fetch full_name, role, and password
            query = "SELECT full_name, role, password FROM employees WHERE worker_id = :worker_id"
            cursor.execute(query, {"worker_id": worker_id})
            result = cursor.fetchone()
            print("Database query executed, result:", result)

            if result and result[2] == password:
                full_name, role = result[0], result[1]
                print(f"Login successful! User: {full_name}, Role: {role}")
                
                # Create and show the centered splash screen
                if self.main_window:
                    splash = SplashScreen(self.main_window, worker_id, full_name, role)
                    self.main_window.addWidget(splash)
                    self.main_window.setCurrentWidget(splash)
                else:
                    self.hide()
            else:
                print("Login failed: incorrect credentials")
                self.display_message("Login Failed. Incorrect Worker ID or Password.", success=False)
        except oracledb.DatabaseError as e:
            print("Database error:", e)
            self.display_message(f"Database Error: {str(e)}", success=False)
        finally:
            try:
                cursor.close()
                connection.close()
                print("Database connection closed.")
            except Exception as e:
                print("Error closing database connection:", e)

    def handle_signup(self):
        worker_id = self.username_input.text().strip()
        full_name = self.fullname_input.text().strip()
        role = self.role_input.currentText()
        phone = self.phone_input.text().strip()
        password = self.password_input.text().strip()

        # Validate inputs
        if not worker_id or not full_name or not password or not phone:
            self.display_message("Please fill all fields.", success=False)
            return

        try:
            connection = oracledb.connect(user="system", password="Abdo2004@", dsn="localhost:1521/FREE")
            cursor = connection.cursor()
            
            # Check if worker_id already exists
            cursor.execute("SELECT COUNT(*) FROM employees WHERE worker_id = :worker_id", {"worker_id": worker_id})
            if cursor.fetchone()[0] > 0:
                self.display_message("Worker ID already exists!", success=False)
                return
                
            # Insert new employee
            insert_query = """
                INSERT INTO employees (worker_id, full_name, role, CONTACT_NUMBER, password) 
                VALUES (:worker_id, :full_name, :role, :CONTACT_NUMBER, :password)
            """
            cursor.execute(insert_query, {
                "worker_id": worker_id,
                "full_name": full_name,
                "role": role,
                "CONTACT_NUMBER": phone,
                "password": password
            })
            connection.commit()
            
            self.display_message("Registration successful! You can now login.", success=True)
            # Switch back to login mode after successful registration
            self.toggle_signup_mode()
            
        except oracledb.DatabaseError as e:
            print("Database error:", e)
            self.display_message(f"Registration Error: {str(e)}", success=False)
        finally:
            try:
                cursor.close()
                connection.close()
            except:
                pass

    def resizeEvent(self, event):
        self.bg_label.setGeometry(0, 0, self.width(), self.height())

# ------------------------- SplashScreen Widget -------------------------
class SplashScreen(QtWidgets.QWidget):
    def __init__(self, main_window, worker_id, full_name, role, parent=None):
        super().__init__(parent)
        self.main_window = main_window  # QStackedWidget reference
        self.worker_id = worker_id
        self.full_name = full_name
        self.role = role

        # Remove window frame and set transparent background
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.counter = 0
        self.n = 100  
        self.initUI()
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)

    def initUI(self):
    # Outer layout centers the splash container in the available space
     layout = QtWidgets.QVBoxLayout(self)
     layout.setAlignment(QtCore.Qt.AlignCenter)

    # Container with the background image set via stylesheet.
     container = QtWidgets.QWidget()
    # Increase container size so it can hold all the content
     container.setFixedSize(600, 400)
     container.setStyleSheet("""
        QWidget {
            border-radius: 5px;
            background-image: url('resources/splash1.jpg');
            background-repeat: no-repeat;
            background-position: center;
            background-size: cover;
        }
    """)
     container_layout = QtWidgets.QVBoxLayout(container)
     container_layout.setContentsMargins(20, 20, 20, 20)
     container_layout.setSpacing(10)
     container_layout.setAlignment(QtCore.Qt.AlignCenter)

    # Welcome text (ensure it wraps if needed)
     self.labelWelcome = QtWidgets.QLabel(f"WELCOME  {self.role} {self.full_name.upper()}")
     self.labelWelcome.setAlignment(QtCore.Qt.AlignCenter)
     self.labelWelcome.setWordWrap(True)
     self.labelWelcome.setStyleSheet("color: black; font-size: 30px; font-weight: bold;")
     container_layout.addWidget(self.labelWelcome)

    # Loading label
     self.labelLoading = QtWidgets.QLabel("loading...")
     self.labelLoading.setAlignment(QtCore.Qt.AlignCenter)
     self.labelLoading.setStyleSheet("color: black; font-size: 16px;")
     container_layout.addWidget(self.labelLoading)

    # Progress bar
     self.progressBar = QtWidgets.QProgressBar()
     self.progressBar.setFixedHeight(30)
     self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
     self.progressBar.setFormat('%p%')
     self.progressBar.setTextVisible(True)
     self.progressBar.setRange(0, self.n)
     self.progressBar.setValue(0)
     container_layout.addWidget(self.progressBar)

     layout.addWidget(container)

    def loading(self):
        self.progressBar.setValue(self.counter)
        if self.counter % 50 == 0:
            print("Splash progress:", self.counter)
        if self.counter == int(self.n * 0.3):
            self.labelLoading.setText("loading... [30%]")
        elif self.counter == int(self.n * 0.6):
            self.labelLoading.setText("loading... [60%]")
        elif self.counter >= self.n:
            self.timer.stop()
            # Once done, create the main application page
            main_app_page = MainWindow(self.worker_id, self.full_name, self.role, main_window=self.main_window)
            self.main_window.addWidget(main_app_page)
            self.main_window.setCurrentWidget(main_app_page)
        self.counter += 1

# ------------------------- MainWindow (Main Application) -------------------------
import random
import numpy as np
import seaborn as sns
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QtWidgets.QWidget):
    def __init__(self, worker_id, full_name, role, main_window=None, parent=None):
        super().__init__(parent)
        self.worker_id = worker_id
        self.full_name = full_name
        self.role = role
        self.main_window = main_window  # QStackedWidget reference
        self.background_pixmap = QtGui.QPixmap("resources/app3bg.jpg")
        self.setup_ui()
        self.showMaximized()

    def setup_ui(self):
        self.setWindowTitle("Main Application")
        self.setStyleSheet("background-color: transparent;")
        
        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: transparent; border: none;")
        
        container_widget = QtWidgets.QWidget(self)
        main_layout = QtWidgets.QVBoxLayout(container_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Header with title (logout button will be at bottom left)
        header_widget = QtWidgets.QWidget(self)
        header_layout = QtWidgets.QHBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QtWidgets.QLabel(f"Welcome, {self.full_name}", self)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setFont(QtGui.QFont("Segoe UI", 22, QtGui.QFont.Bold))
        title_label.setStyleSheet("color: #333; background-color: rgba(255,255,255,0.7); padding: 10px;")
        header_layout.addWidget(title_label)
        main_layout.addWidget(header_widget)
        
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.setSpacing(20)
        
        user_info_card = self.create_user_info_card(self.worker_id, self.full_name, self.role)
        top_layout.addWidget(user_info_card)
        
        activity_diagram = self.create_activity_diagram()
        top_layout.addWidget(activity_diagram)
        main_layout.addLayout(top_layout)

        workspaces_label = QtWidgets.QLabel("WORK SPACES", self)
        workspaces_label.setAlignment(QtCore.Qt.AlignCenter)
        workspaces_label.setFont(QtGui.QFont("Segoe UI", 20, QtGui.QFont.Bold))
        workspaces_label.setStyleSheet("color: #333; background-color: rgba(255,255,255,0.7); padding: 8px;")
        main_layout.addWidget(workspaces_label)

        workspace_container = QtWidgets.QWidget(self)
        workspace_layout = QtWidgets.QHBoxLayout(workspace_container)
        workspace_layout.setContentsMargins(30, 30, 30, 30)
        workspace_layout.setSpacing(20)

        workspaces = [
            ("Patients Space", "Manage patient records and information.", "resources/icons8-patient-50.png"),
            ("Data Dashboard", "Analyze and visualize data trends effectively.", "resources/icons8-data-visualization-50.png"),
            ("Worker Timing", "Track employee work schedules and performance.", "resources/icons8-doctor-50.png")
        ]

        for title, desc, icon_path in workspaces:
            card = self.create_workspace_card(title, desc, icon_path)
            # Connect click event to the corresponding workspace handler
            card.mousePressEvent = lambda event, ws=title: self.handle_workspace_click(event, ws)
            workspace_layout.addWidget(card)

        workspace_container.setLayout(workspace_layout)
        main_layout.addWidget(workspace_container)

        scroll_area.setWidget(container_widget)

        # Outer layout that includes the scroll area and a bottom bar for the logout button.
        outer_layout = QtWidgets.QVBoxLayout(self)
        outer_layout.addWidget(scroll_area)

        # Bottom bar with logout button aligned to bottom left.
        bottom_bar = QtWidgets.QHBoxLayout()
        logout_btn = QtWidgets.QPushButton("Log Out", self)
        logout_btn.setFixedSize(100, 40)
        # Updated style: white background with blue text.
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #0078D4;
                font-size: 14px;
                border: 1px solid #0078D4;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """)
        # Set the icon using the relative resource path.
        logout_icon = QtGui.QIcon("resources/logout_icon.png")
        logout_btn.setIcon(logout_icon)
        logout_btn.clicked.connect(self.logout)
        bottom_bar.addWidget(logout_btn, alignment=QtCore.Qt.AlignLeft)
        outer_layout.addLayout(bottom_bar)
        self.setLayout(outer_layout)

    def handle_workspace_click(self, event, workspace):
        """
        When a workspace card is clicked, load the corresponding widget from its module.
        """
        if workspace == "Patients Space":
            widget = PatientWidget(self.worker_id, self.full_name, self.role, main_window=self.main_window)
        elif workspace == "Data Dashboard":
            widget = DataWidget(self.worker_id, self.full_name, self.role, main_window=self.main_window)
        elif workspace == "Worker Timing":
            widget = WorkerWidget(self.worker_id, self.full_name, self.role, main_window=self.main_window)
        else:
            return
        self.main_window.addWidget(widget)
        self.main_window.setCurrentWidget(widget)

    def logout(self):
        # Return to the authentication page (assumed to be index 0 in the QStackedWidget)
        if self.main_window:
            self.main_window.setCurrentIndex(0)

    def create_user_info_card(self, worker_id, full_name, role):
        card = QtWidgets.QFrame(self)
        card.setFixedSize(480, 200)
        card.setStyleSheet(
            """
            QFrame {
                background-color: #E6F7FF;
                border-radius: 15px;
                border: 1px solid #90C8F7;
            }
            QFrame:hover {
                border: 2px solid #0078D4;
            }
            """
        )
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)
        
        header_label = QtWidgets.QLabel("User Info", self)
        header_label.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        header_label.setStyleSheet("color: #0078D4; border-bottom: 1px solid #0078D4; padding-bottom: 5px;")
        header_label.setFixedHeight(40)
        layout.addWidget(header_label)
        
        details_label = QtWidgets.QLabel(self)
        details_label.setText(f"ID: {worker_id}\nName: {full_name}\nRole: {role}")
        details_label.setFont(QtGui.QFont("Segoe UI", 16))
        details_label.setAlignment(QtCore.Qt.AlignCenter)
        details_label.setStyleSheet("color: #333;")
        layout.addWidget(details_label, 1)
        
        layout.setStretch(0, 1)
        layout.setStretch(1, 3)
        
        return card

    def create_activity_diagram(self):
        sns.set_style("whitegrid")
        fig = Figure(figsize=(7, 4))
        ax = fig.add_subplot(111)
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        activities = np.random.randint(50, 200, size=len(days))
        
        ax.bar(days, activities, color='dodgerblue', alpha=0.7)
        
        total = int(sum(activities))
        ax.text(0.5, max(activities)*1.05, f"Total: {total}", fontsize=12, fontweight='bold',
                color='black', transform=ax.transAxes, ha='center')
        
        ax.set_xlabel("Days", fontsize=12)
        ax.set_ylabel("Users", fontsize=12)
        ax.set_title("Users activity weekly ", fontsize=14, color='dodgerblue')
        for tick in ax.get_xticklabels():
            tick.set_rotation(45)
            tick.set_fontsize(10)
        
        fig.subplots_adjust(top=0.85, bottom=0.25)
        fig.tight_layout(rect=[0, 0.05, 1, 0.95])
        
        canvas = FigureCanvas(fig)
        canvas.setFixedSize(480, 400)
        return canvas

    def create_workspace_card(self, title, description, icon_path):
        card = QtWidgets.QFrame(self)
        card.setFixedSize(280, 400)
        card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 1px solid #DDD;
            }
            QFrame:hover {
                border: 2px solid #0078D4;
            }
            """
        )
        layout = QtWidgets.QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        icon_label = QtWidgets.QLabel(self)
        icon_pixmap = QtGui.QPixmap(icon_path).scaled(70, 70, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        icon_label.setFixedHeight(80)
        layout.addWidget(icon_label)
        
        title_label = QtWidgets.QLabel(title, self)
        title_label.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setFixedHeight(40)
        layout.addWidget(title_label)
        
        description_label = QtWidgets.QLabel(description, self)
        description_label.setFont(QtGui.QFont("Segoe UI", 14))
        description_label.setAlignment(QtCore.Qt.AlignCenter)
        description_label.setWordWrap(True)
        layout.addWidget(description_label, 1)
        
        layout.setStretch(0, 1)
        layout.setStretch(1, 1)
        layout.setStretch(2, 3)
        
        return card

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        if not self.background_pixmap.isNull():
            painter.drawPixmap(self.rect(), self.background_pixmap)
        else:
            super().paintEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # Assuming you use a QStackedWidget to manage pages:
    stacked_widget = QtWidgets.QStackedWidget()
    # Add HomePage as the initial widget.
    home_page = HomePage(main_window=stacked_widget)
    stacked_widget.addWidget(home_page)
    stacked_widget.show()
    sys.exit(app.exec_())
