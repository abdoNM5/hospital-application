import sys
import time
from PyQt5 import QtWidgets, QtGui, QtCore
import oracledb

# ------------------------- HomePage (Login Window) -------------------------
class HomePage(QtWidgets.QWidget):
    def __init__(self, main_window=None, parent=None):
        super().__init__(parent)
        self.main_window = main_window  # Reference to the main QMainWindow (if any)
        print("HomePage initialized with main_window:", self.main_window)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("background-color: white;")  # Main background color

        # Create QLabel to hold the background image
        self.bg_label = QtWidgets.QLabel(self)
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        pixmap = QtGui.QPixmap(r"C:\Users\nmira\OneDrive\Documents\hosîtal2\resources\healthcare.webp")
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

            if result and result[2] == password:  # Compare with stored password
                full_name, role = result[0], result[1]
                print(f"Login successful! User: {full_name}, Role: {role}")
                
                # Hide login window
                if self.main_window:
                    print("Hiding main window instead of closing.")
                    self.main_window.hide()
                else:
                    print("Hiding login window.")
                    self.hide()
                
                # Pass user details (including worker_id) to SplashScreen
                QtCore.QTimer.singleShot(1000, lambda: self.launchSplash(worker_id, full_name, role))
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

    def launchSplash(self, worker_id, full_name, role):
        print("launchSplash() called")
        self.splash = SplashScreen(worker_id, full_name, role)
        self.splash.show()

    def resizeEvent(self, event):
        self.bg_label.setGeometry(0, 0, self.width(), self.height())

# ------------------------- Custom SplashScreen -------------------------
class SplashScreen(QtWidgets.QWidget):
    def __init__(self, worker_id, full_name, role):
        super().__init__()
        print("SplashScreen initialized for:", full_name, role)
        self.worker_id = worker_id
        self.full_name = full_name
        self.role = role

        self.setWindowTitle('Splash Screen Example')
        self.setFixedSize(1100, 500)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.counter = 0
        self.n = 100  

        self.initUI()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.loading)
        self.timer.start(30)

    def initUI(self):
        self.backgroundLabel = QtWidgets.QLabel(self)
        bg_pixmap = QtGui.QPixmap(r"C:\Users\nmira\OneDrive\Documents\hosîtal2\resources\splash1.jpg")
        self.backgroundLabel.setPixmap(bg_pixmap)
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.setGeometry(0, 0, self.width(), self.height())

        self.labelWelcome = QtWidgets.QLabel(self)
        self.labelWelcome.setText(f"WELCOME  {self.role} {self.full_name.upper()}")
        self.labelWelcome.setAlignment(QtCore.Qt.AlignCenter)
        self.labelWelcome.setStyleSheet("color: white; font-size: 30px; font-weight: bold;")
        self.labelWelcome.setGeometry(0, 50, self.width(), 50)

        self.labelLoading = QtWidgets.QLabel(self)
        self.labelLoading.setText("loading...")
        self.labelLoading.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLoading.setStyleSheet("color: black; font-size: 16px;")
        self.labelLoading.setGeometry(0, self.height()-140, self.width(), 30)

        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setGeometry(100, self.height()-100, self.width()-200, 30)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setTextVisible(True)
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(0)

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
            self.close()
            time.sleep(1)
            self.main_window = MainWindow(self.worker_id, self.full_name, self.role)  # Pass user info
            self.main_window.show()
        self.counter += 1

# ------------------------- MainWindow (Main Application) -------------------------
import sys
import random
import numpy as np
import seaborn as sns
from PyQt5 import QtWidgets, QtGui, QtCore

# Import matplotlib and its Qt5Agg backend for embedding plots in PyQt5
import matplotlib
matplotlib.use("Qt5Agg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class MainWindow(QtWidgets.QWidget):
    def __init__(self, worker_id, full_name, role, parent=None):
        super().__init__(parent)
        self.worker_id = worker_id  # Store worker_id
        self.full_name = full_name  # Store full_name
        self.role = role            # Store role
        # Load background image once; update the path as needed.
        self.background_pixmap = QtGui.QPixmap("C:/Users/nmira/OneDrive/Documents/hosîtal2/resources/app3bg.jpg")
        self.setup_ui()
        self.showMaximized()  # Maximizes the window

    def setup_ui(self):
        self.setWindowTitle("Main Application")
        # Set transparent background (we draw our own image)
        self.setStyleSheet("background-color: transparent;")
        
        # Create a QScrollArea for vertical scrolling
        scroll_area = QtWidgets.QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: transparent; border: none;")
        
        # Main container widget inside scroll area
        container_widget = QtWidgets.QWidget(self)
        main_layout = QtWidgets.QVBoxLayout(container_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Welcome Label at the top
        title_label = QtWidgets.QLabel(f"Welcome, {self.full_name} ", self)
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_label.setFont(QtGui.QFont("Segoe UI", 22, QtGui.QFont.Bold))
        title_label.setStyleSheet("color: #333; background-color: rgba(255,255,255,0.7); padding: 10px;")
        main_layout.addWidget(title_label)
        
        # Horizontal layout for User Info and Activity Diagram
        top_layout = QtWidgets.QHBoxLayout()
        top_layout.setSpacing(20)
        
        # User info card with header "User Info" and details below it
        user_info_card = self.create_user_info_card(self.worker_id, self.full_name, self.role)
        top_layout.addWidget(user_info_card)
        
        # Activity Diagram (user activity by weekday)
        activity_diagram = self.create_activity_diagram()
        top_layout.addWidget(activity_diagram)

        main_layout.addLayout(top_layout)

        # Label for Workspace Section
        workspaces_label = QtWidgets.QLabel("WORK SPACES", self)
        workspaces_label.setAlignment(QtCore.Qt.AlignCenter)
        workspaces_label.setFont(QtGui.QFont("Segoe UI", 20, QtGui.QFont.Bold))
        workspaces_label.setStyleSheet("color: #333; background-color: rgba(255,255,255,0.7); padding: 8px;")
        main_layout.addWidget(workspaces_label)

        # Container for workspace cards
        workspace_container = QtWidgets.QWidget(self)
        workspace_layout = QtWidgets.QHBoxLayout(workspace_container)
        workspace_layout.setContentsMargins(30, 30, 30, 30)
        workspace_layout.setSpacing(20)

        # Define workspace data (Title, Description, Icon Path)
        workspaces = [
            ("Patients Space", "Manage patient records and information.", r"C:\Users\nmira\OneDrive\Documents\hosîtal2\resources\icons8-patient-50.png"),
            ("Data Dashboard", "Analyze and visualize data trends effectively.", r"C:\Users\nmira\OneDrive\Documents\hosîtal2\resources\icons8-data-visualization-50.png"),
            ("Worker Timing", "Track employee work schedules and performance.", r"C:\Users\nmira\OneDrive\Documents\hosîtal2\resources\icons8-doctor-50.png")
        ]

        for title, desc, icon_path in workspaces:
            workspace_layout.addWidget(self.create_workspace_card(title, desc, icon_path))

        workspace_container.setLayout(workspace_layout)
        main_layout.addWidget(workspace_container)

        # Set container widget to scroll area and then add to the main layout of the window
        scroll_area.setWidget(container_widget)
        outer_layout = QtWidgets.QVBoxLayout(self)
        outer_layout.addWidget(scroll_area)
        self.setLayout(outer_layout)

    def create_user_info_card(self, worker_id, full_name, role):
        """Creates a card that displays a header 'User Info' and below it the worker details."""
        card = QtWidgets.QFrame(self)
        # Reduced overall size from 520x220 to 480x200
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
        # Reduce top/bottom margins to give more space to content
        layout.setContentsMargins(15, 10, 15, 10)
        # Increase spacing between elements
        layout.setSpacing(15)
        
        # Header Label - make it more compact
        header_label = QtWidgets.QLabel("User Info", self)
        header_label.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
        header_label.setAlignment(QtCore.Qt.AlignCenter)
        header_label.setStyleSheet("color: #0078D4; border-bottom: 1px solid #0078D4; padding-bottom: 5px;")
        # Set a fixed height for the header to make it more compact
        header_label.setFixedHeight(40)
        layout.addWidget(header_label)
        
        # Details Label - give it more space
        details_label = QtWidgets.QLabel(self)
        details_label.setText(f"ID: {worker_id}\nName: {full_name}\nRole: {role}")
        # Increase font size for better visibility
        details_label.setFont(QtGui.QFont("Segoe UI", 16))
        details_label.setAlignment(QtCore.Qt.AlignCenter)
        details_label.setStyleSheet("color: #333;")
        # Set a stretch factor to make it take up more space
        layout.addWidget(details_label, 1)
        
        # Set stretch factors to allocate more space to details
        layout.setStretch(0, 1)  # Header gets 1 part
        layout.setStretch(1, 3)  # Details get 3 parts
        
        return card

    def create_activity_diagram(self):
        """Creates a Seaborn-based activity diagram (bar chart) to display user activity by weekday."""
        sns.set_style("whitegrid")
        # Increase figure height to give more room to the plot
        fig = Figure(figsize=(7, 4))
        ax = fig.add_subplot(111)
        
        # Sample data for user activity by weekday
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        activities = np.random.randint(50, 200, size=len(days))
        
        # Create a bar plot for activity counts
        ax.bar(days, activities, color='dodgerblue', alpha=0.7)
        
        # Add total activities display
        total = int(sum(activities))
        ax.text(0.5, max(activities)*1.05, f"Total: {total}", fontsize=12, fontweight='bold',
                color='black', transform=ax.transAxes, ha='center')
        
        # Set x and y labels
        ax.set_xlabel("Days", fontsize=12)
        ax.set_ylabel("Users", fontsize=12)
        ax.set_title("Users activity weekly ",fontsize=14,color='dodgerblue')
        # Adjust x-axis labels to prevent overlapping
        for tick in ax.get_xticklabels():
            tick.set_rotation(45)
            tick.set_fontsize(10)
        
        # Add more padding at the top and bottom to make sure everything is visible
        fig.subplots_adjust(top=0.85, bottom=0.25)
        
        # Call tight_layout to improve spacing but maintain our custom adjustments
        fig.tight_layout(rect=[0, 0.05, 1, 0.95])
        
        canvas = FigureCanvas(fig)
        # Reduced width from 520 to 480 to match user info card
        canvas.setFixedSize(480, 400)
        return canvas

    def create_workspace_card(self, title, description, icon_path):
        """Creates a QFrame styled as a workspace card with an icon, title, and wrapped description."""
        card = QtWidgets.QFrame(self)
        # Reduced size from 320x450 to 280x400
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
        # Reduce top/bottom margins to give more space to content
        layout.setContentsMargins(15, 15, 15, 15)
        # Keep equal spacing between elements
        layout.setSpacing(20)
        
        # Icon - make it proportionally smaller
        icon_label = QtWidgets.QLabel(self)
        icon_pixmap = QtGui.QPixmap(icon_path).scaled(70, 70, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        icon_label.setPixmap(icon_pixmap)
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        # Set fixed height for icon
        icon_label.setFixedHeight(80)
        layout.addWidget(icon_label)
        
        # Title - make it more compact
        title_label = QtWidgets.QLabel(title, self)
        title_label.setFont(QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold))
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        # Set fixed height for title
        title_label.setFixedHeight(40)
        layout.addWidget(title_label)
        
        # Description - give it more space and larger font
        description_label = QtWidgets.QLabel(description, self)
        # Increase font size for description
        description_label.setFont(QtGui.QFont("Segoe UI", 14))
        description_label.setAlignment(QtCore.Qt.AlignCenter)
        description_label.setWordWrap(True)
        # Set a stretch factor to make description take more space
        layout.addWidget(description_label, 1)
        
        # Set stretch factors to allocate more space to description
        layout.setStretch(0, 1)  # Icon gets 1 part
        layout.setStretch(1, 1)  # Title gets 1 part
        layout.setStretch(2, 3)  # Description gets 3 parts
        
        return card

    def paintEvent(self, event):
        """Override paintEvent to draw the background image across the whole window."""
        painter = QtGui.QPainter(self)
        if not self.background_pixmap.isNull():
            painter.drawPixmap(self.rect(), self.background_pixmap)
        else:
            super().paintEvent(event)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # For testing purposes, pass dummy data.
    window = MainWindow("12345", "Test User", "Tester")
    window.show()
    sys.exit(app.exec_())