import sys
import time
from PyQt5 import QtWidgets, QtGui, QtCore
import oracledb

# New Imports for workspace widgets
from .patient import PatientWidget
from .dashboard import DiseaseStatsDashboard  # Import DiseaseStatsDashboard from its module
from .workerTiming import WorkerTimingSpace  # Import WorkerTimingSpace from its module


# ------------------------- HomePage (Login Window) -------------------------
class HomePage(QtWidgets.QWidget):
    def __init__(self, main_window=None, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.is_signup_mode = False
        self.setup_ui()
        # Start with animation
        self.animate_login_appearance()

    def setup_ui(self):
        # Set main properties
        self.setStyleSheet("background-color: #f0f2f5;")
        
        # Create a blur effect for background
        self.blur_effect = QtWidgets.QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(10)
        
        # Background image with parallax effect
        self.bg_label = QtWidgets.QLabel(self)
        self.bg_label.setObjectName("BackgroundLabel")
        self.bg_pixmap = QtGui.QPixmap("resources/hospital-bg3.jpg")

        # Make sure the background label fills the entire window
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.bg_label.setScaledContents(True)  # This ensures the image scales to fill the label
        self.bg_label.setPixmap(self.bg_pixmap)
        self.bg_label.lower()  # Move to bottom layer
        
        # Create the main scroll area that will contain everything
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: transparent; border: none;")
        
        # Create a container widget for the scroll area
        self.scroll_container = QtWidgets.QWidget()
        self.scroll_container.setStyleSheet("background-color: transparent;")
        
        # Main layout for scroll container
        self.scroll_layout = QtWidgets.QVBoxLayout(self.scroll_container)
        self.scroll_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.scroll_layout.setSpacing(20)
        
        # Overlay for depth effect
        self.overlay = QtWidgets.QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 0.4);")
        self.overlay.setGeometry(0, 0, self.width(), self.height())
        
        # Create hospital logo/icon
        self.logo_label = QtWidgets.QLabel()
        logo_pixmap = QtGui.QPixmap("resources/hospital-logo.png")
        if logo_pixmap.isNull():
            # Create a fallback icon if image doesn't exist
            self.logo_label.setText("🏥")
            self.logo_label.setFont(QtGui.QFont("Segoe UI", 48))
            self.logo_label.setStyleSheet("color: white; background-color: transparent;")
        else:
            self.logo_label.setPixmap(logo_pixmap.scaled(80, 80, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        
        self.logo_label.setAlignment(QtCore.Qt.AlignCenter)
        self.logo_label.setFixedHeight(100)
        self.scroll_layout.addWidget(self.logo_label)

        # Login Card Frame with glass morphism effect
        self.login_frame = QtWidgets.QFrame()
        self.login_frame.setFixedSize(400, 500)  # Initially height is 0 for animation
        self.login_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.85);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.3);
            }
        """)
        
        # Add shadow effect to login frame
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QtGui.QColor(0, 0, 0, 100))
        shadow.setOffset(0, 5)
        self.login_frame.setGraphicsEffect(shadow)
        
        # Login form layout
        self.login_layout = QtWidgets.QVBoxLayout(self.login_frame)
        self.login_layout.setAlignment(QtCore.Qt.AlignTop)
        self.login_layout.setSpacing(15)
        self.login_layout.setContentsMargins(30, 30, 30, 50)

        # Title with dynamic color
        self.title_label = QtWidgets.QLabel("Welcome Back")
        title_font = QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #1a237e; margin-bottom: 10px;")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.login_layout.addWidget(self.title_label)
        
        # Subtitle
        self.subtitle_label = QtWidgets.QLabel("Sign in to continue")
        self.subtitle_label.setFont(QtGui.QFont("Segoe UI", 12))
        self.subtitle_label.setStyleSheet("color: #757575; margin-bottom: 15px;")
        self.subtitle_label.setAlignment(QtCore.Qt.AlignCenter)
        self.login_layout.addWidget(self.subtitle_label)

        # Username/Worker ID Input with icon
        self.username_container = QtWidgets.QWidget()
        username_layout = QtWidgets.QHBoxLayout(self.username_container)
        username_layout.setContentsMargins(0, 0, 0, 0)
        
        self.username_icon = QtWidgets.QLabel()
        self.username_icon.setFixedSize(20, 20)
        self.username_icon.setPixmap(self.create_icon("person"))
        username_layout.addWidget(self.username_icon)
        
        self.username_input = QtWidgets.QLineEdit()
        self.username_input.setPlaceholderText("Worker ID")
        self.username_input.setFixedHeight(50)
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 2px solid #3f51b5;
                background-color: transparent;
                padding-left: 10px;
                font-size: 16px;
                font-family: 'Segoe UI';
            }
            QLineEdit:focus {
                border-bottom: 2px solid #5c6bc0;
            }
        """)
        username_layout.addWidget(self.username_input)
        self.login_layout.addWidget(self.username_container)
        
        # Signup fields (initially hidden)
        self.signup_fields_widget = QtWidgets.QWidget()
        signup_fields_layout = QtWidgets.QVBoxLayout(self.signup_fields_widget)
        signup_fields_layout.setContentsMargins(0, 0, 0, 0)
        signup_fields_layout.setSpacing(30)  # Increased spacing between signup fields
        
        # Full Name Input
        self.fullname_container = QtWidgets.QWidget()
        fullname_layout = QtWidgets.QHBoxLayout(self.fullname_container)
        fullname_layout.setContentsMargins(0, 0, 0, 0)
        
        self.fullname_icon = QtWidgets.QLabel()
        self.fullname_icon.setFixedSize(20, 20)
        self.fullname_icon.setPixmap(self.create_icon("badge"))
        fullname_layout.addWidget(self.fullname_icon)
        
        self.fullname_input = QtWidgets.QLineEdit()
        self.fullname_input.setPlaceholderText("Full Name")
        self.fullname_input.setFixedHeight(45)
        self.fullname_input.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 2px solid #3f51b5;
                background-color: transparent;
                padding-left: 10px;
                font-size: 16px;
                font-family: 'Segoe UI';
            }
            QLineEdit:focus {
                border-bottom: 2px solid #5c6bc0;
            }
        """)
        fullname_layout.addWidget(self.fullname_input)
        signup_fields_layout.addWidget(self.fullname_container)
        
        # Role Selection
        self.role_container = QtWidgets.QWidget()
        role_layout = QtWidgets.QHBoxLayout(self.role_container)
        role_layout.setContentsMargins(0, 0, 0, 0)
        
        self.role_icon = QtWidgets.QLabel()
        self.role_icon.setFixedSize(20, 20)
        self.role_icon.setPixmap(self.create_icon("work"))
        role_layout.addWidget(self.role_icon)
        
        self.role_input = QtWidgets.QComboBox()
        self.role_input.addItems(["Doctor", "Nurse", "Surgeon", "Paramedic", "Administrator"])
        self.role_input.setFixedHeight(45)
        self.role_input.setStyleSheet("""
            QComboBox {
                border: none;
                border-bottom: 2px solid #3f51b5;
                background-color: transparent;
                padding-left: 10px;
                font-size: 16px;
                font-family: 'Segoe UI';
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: url(resources/down-arrow.png);
                width: 16px;
                height: 16px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #e0e0e0;
                selection-background-color: #e8eaf6;
                selection-color: #3f51b5;
                color: #212121;
            }
        """)
        role_layout.addWidget(self.role_input)
        signup_fields_layout.addWidget(self.role_container)
        
        # Phone Number Input
        self.phone_container = QtWidgets.QWidget()
        phone_layout = QtWidgets.QHBoxLayout(self.phone_container)
        phone_layout.setContentsMargins(0, 0, 0, 0)
        
        self.phone_icon = QtWidgets.QLabel()
        self.phone_icon.setFixedSize(20, 20)
        self.phone_icon.setPixmap(self.create_icon("phone"))
        phone_layout.addWidget(self.phone_icon)
        
        self.phone_input = QtWidgets.QLineEdit()
        self.phone_input.setPlaceholderText("Phone Number")
        self.phone_input.setFixedHeight(45)
        self.phone_input.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 2px solid #3f51b5;
                background-color: transparent;
                padding-left: 10px;
                font-size: 16px;
                font-family: 'Segoe UI';
            }
            QLineEdit:focus {
                border-bottom: 2px solid #5c6bc0;
            }
        """)
        phone_layout.addWidget(self.phone_input)
        signup_fields_layout.addWidget(self.phone_container)
        
        self.signup_fields_widget.setVisible(False)
        self.login_layout.addWidget(self.signup_fields_widget)
        
        # Password Input with icon
        self.password_container = QtWidgets.QWidget()
        password_layout = QtWidgets.QHBoxLayout(self.password_container)
        password_layout.setContentsMargins(0, 0, 0, 0)
        
        self.password_icon = QtWidgets.QLabel()
        self.password_icon.setFixedSize(20, 20)
        self.password_icon.setPixmap(self.create_icon("lock"))
        password_layout.addWidget(self.password_icon)
        
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setFixedHeight(50)
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: none;
                border-bottom: 2px solid #3f51b5;
                background-color: transparent;
                padding-left: 10px;
                font-size: 16px;
                font-family: 'Segoe UI';
            }
            QLineEdit:focus {
                border-bottom: 2px solid #5c6bc0;
            }
        """)
        password_layout.addWidget(self.password_input)
        
        # Show/Hide password button
        self.show_password_btn = QtWidgets.QPushButton()
        self.show_password_btn.setFixedSize(24, 24)
        # Use text for eye icon if image doesn't exist
        self.show_password_btn.setText("👁️")
        self.show_password_btn.setStyleSheet("background: transparent; border: none; font-size: 16px;")
        self.show_password_btn.setCursor(QtCore.Qt.PointingHandCursor)
        self.show_password_btn.clicked.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.show_password_btn)
        
        self.login_layout.addWidget(self.password_container)
        
        # Remember me and Forgot password row
        self.options_container = QtWidgets.QWidget()
        options_layout = QtWidgets.QHBoxLayout(self.options_container)
        options_layout.setContentsMargins(0, 0, 0, 0)
        
        self.remember_me = QtWidgets.QCheckBox("Remember me")
        self.remember_me.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                font-family: 'Segoe UI';
                color: #616161;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #9fa8da;
                border-radius: 3px;
            }
            QCheckBox::indicator:checked {
                background-color: #3f51b5;
                border: 2px solid #3f51b5;
            }
        """)
        options_layout.addWidget(self.remember_me, alignment=QtCore.Qt.AlignCenter)
        
        self.login_layout.addWidget(self.options_container)
        
        # Login Button (Gradient effect)
        self.login_button = QtWidgets.QPushButton("Sign In")
        self.login_button.setFixedHeight(50)
        self.login_button.setFont(QtGui.QFont("Segoe UI", 14, QtGui.QFont.Bold))
        self.login_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #303f9f, stop:1 #3f51b5);
                color: white;
                border-radius: 25px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3949ab, stop:1 #5c6bc0);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #283593, stop:1 #3f51b5);
            }
        """)
        self.login_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.login_button.clicked.connect(self.handle_login)
        self.login_layout.addWidget(self.login_button)
        
        # Horizontal line with "or" text
        self.separator_widget = QtWidgets.QWidget()
        separator_layout = QtWidgets.QHBoxLayout(self.separator_widget)
        separator_layout.setContentsMargins(0, 10, 0, 10)
        
        self.left_line = QtWidgets.QFrame()
        self.left_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.left_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.left_line.setStyleSheet("background-color: #e0e0e0;")
        separator_layout.addWidget(self.left_line)
        
        self.or_label = QtWidgets.QLabel("OR")
        self.or_label.setStyleSheet("color: #9e9e9e; font-size: 14px;")
        self.or_label.setFixedWidth(40)
        self.or_label.setAlignment(QtCore.Qt.AlignCenter)
        separator_layout.addWidget(self.or_label)
        
        self.right_line = QtWidgets.QFrame()
        self.right_line.setFrameShape(QtWidgets.QFrame.HLine)
        self.right_line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.right_line.setStyleSheet("background-color: #e0e0e0;")
        separator_layout.addWidget(self.right_line)
        
        self.login_layout.addWidget(self.separator_widget)
        
        # Sign Up Button
        self.signup_button = QtWidgets.QPushButton("Create New Account")
        self.signup_button.setFixedHeight(50)
        self.signup_button.setFont(QtGui.QFont("Segoe UI", 14))
        self.signup_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #3f51b5;
                border: 2px solid #3f51b5;
                border-radius: 25px;
            }
            QPushButton:hover {
                background-color: rgba(63, 81, 181, 0.1);
            }
            QPushButton:pressed {
                background-color: rgba(63, 81, 181, 0.2);
            }
        """)
        self.signup_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.signup_button.clicked.connect(self.toggle_signup_mode)
        self.login_layout.addWidget(self.signup_button)
        
        # Message label for feedback
        self.message_label = QtWidgets.QLabel("")
        self.message_label.setAlignment(QtCore.Qt.AlignCenter)
        self.message_label.setStyleSheet("""
            background-color: transparent;
            color: transparent;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
            font-family: 'Segoe UI';
        """)
        self.message_label.setFixedHeight(0)  # Hidden initially
        self.message_label.setVisible(False)
        self.login_layout.addWidget(self.message_label)
        
        # Add Login Frame to scroll layout
        self.scroll_layout.addWidget(self.login_frame, alignment=QtCore.Qt.AlignCenter)
        
        # Set the scroll container as the widget for the scroll area
        self.scroll_area.setWidget(self.scroll_container)
        
        # Main layout for the entire widget
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

    def create_icon(self, icon_type):
        """Create an icon for inputs based on type"""
        icon_data = {
            "person": (0, 0, 0, "👤"),
            "badge": (0, 0, 0, "📛"),
            "work": (0, 0, 0, "💼"),
            "phone": (0, 0, 0, "📱"),
            "lock": (0, 0, 0, "🔒"),
            "eye": (0, 0, 0, "👁️")
        }
        
        # Create a pixmap
        pixmap = QtGui.QPixmap(20, 20)
        pixmap.fill(QtCore.Qt.transparent)
        
        # Create painter
        painter = QtGui.QPainter(pixmap)
        painter.setFont(QtGui.QFont("Segoe UI", 12))
        
        # Get icon info
        r, g, b, text = icon_data.get(icon_type, (0, 0, 0, "❓"))
        
        # Draw text
        painter.setPen(QtGui.QColor(r, g, b))
        painter.drawText(QtCore.QRect(0, 0, 20, 20), QtCore.Qt.AlignCenter, text)
        painter.end()
        
        return pixmap

    def animate_login_appearance(self):
        # Set initial size
        self.login_frame.setFixedWidth(400)
        self.login_frame.setMinimumHeight(500)
        
        # Position it in the center but a bit higher up
        x_pos = (self.width() - self.login_frame.width()) // 2
        y_pos = (self.height() - self.login_frame.height()) // 2 - 50  # Move it up slightly
        
        # Animate from above into view
        self.animation = QtCore.QPropertyAnimation(self.login_frame, b"pos")
        self.animation.setDuration(500)
        self.animation.setStartValue(QtCore.QPoint(x_pos, y_pos - 200))
        self.animation.setEndValue(QtCore.QPoint(x_pos, y_pos))
        self.animation.start()

    def toggle_password_visibility(self):
        """Toggle password visibility with animation"""
        if self.password_input.echoMode() == QtWidgets.QLineEdit.Password:
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.show_password_btn.setText("🔒")  # Use lock emoji for hidden state
        else:
            self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)
            self.show_password_btn.setText("👁️")  # Use eye emoji for visible state

    def resizeEvent(self, event):
        """Handle resize events properly"""
        # Update background label to fill the window
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        
        # Update overlay size to match the window
        self.overlay.setGeometry(0, 0, self.width(), self.height())
        
        # Call the original resize event
        super().resizeEvent(event)

    def showEvent(self, event):
        """Handle window show event to properly position elements"""
        super().showEvent(event)
        # Update background and overlay to match the window size
        self.bg_label.setGeometry(0, 0, self.width(), self.height())
        self.overlay.setGeometry(0, 0, self.width(), self.height())
        self.overlay.lower()
    def toggle_signup_mode(self):
        self.is_signup_mode = not self.is_signup_mode
        
        # Create height animation
        self.height_anim = QtCore.QPropertyAnimation(self.login_frame, b"minimumHeight")
        self.height_anim.setDuration(300)
        
        # Create position animation to adjust scroll position
        self.pos_anim = QtCore.QPropertyAnimation(self.login_frame, b"pos")
        self.pos_anim.setDuration(300)
        current_pos = self.login_frame.pos()
        
        # Update UI based on mode
        if self.is_signup_mode:
            self.title_label.setText("Create Account")
            self.subtitle_label.setText("Join our medical team")
            self.login_button.setText("Back to Login")
            self.signup_button.setText("Register")
            
            # Start animation to expand - INCREASED HEIGHT for better spacing
            self.height_anim.setStartValue(self.login_frame.height())
            self.height_anim.setEndValue(700)  # Increased height even more for better spacing
            
            # Move frame up for better visibility
            self.pos_anim.setStartValue(current_pos)
            self.pos_anim.setEndValue(QtCore.QPoint(current_pos.x(), current_pos.y() - 100))
            
            # Show signup fields with fade effect
            self.signup_fields_widget.setVisible(True)
            self.signup_fields_widget.setStyleSheet("""
                QLineEdit, QComboBox {
                    border: none;
                    border-bottom: 2px solid #3f51b5;
                    background-color: transparent;
                    padding-left: 10px;
                    font-size: 16px;
                    font-family: 'Segoe UI';
                }
                QLineEdit:focus, QComboBox:focus {
                    border-bottom: 2px solid #5c6bc0;
                }
            """)
            
            # Create opacity animation for fields
            self.opacity_anim = QtCore.QPropertyAnimation(self.signup_fields_widget, b"styleSheet")
            self.opacity_anim.setDuration(400)
            self.opacity_anim.setStartValue("opacity: 0;")
            self.opacity_anim.setEndValue("opacity: 1;")
            
            # Create animation group
            self.anim_group = QtCore.QParallelAnimationGroup()
            self.anim_group.addAnimation(self.height_anim)
            self.anim_group.addAnimation(self.opacity_anim)
            self.anim_group.addAnimation(self.pos_anim)
            self.anim_group.start()
            
            # Change button function
            self.signup_button.clicked.disconnect()
            self.signup_button.clicked.connect(self.handle_signup)
            
            # Update separator text
            self.or_label.setText("OR")
            
            # Scroll to make sure the full form is visible
            QtCore.QTimer.singleShot(100, lambda: self.scroll_area.ensureWidgetVisible(self.signup_button))
        else:
            self.title_label.setText("Welcome Back")
            self.subtitle_label.setText("Sign in to continue")
            self.login_button.setText("Sign In")
            self.signup_button.setText("Create New Account")
            
            # Start animation to shrink
            self.height_anim.setStartValue(self.login_frame.height())
            self.height_anim.setEndValue(500)
            
            # Move frame back down
            self.pos_anim.setStartValue(current_pos)
            self.pos_anim.setEndValue(QtCore.QPoint(current_pos.x(), current_pos.y() + 100))
            
            # Create animation group for return to login
            self.anim_group = QtCore.QParallelAnimationGroup()
            self.anim_group.addAnimation(self.height_anim)
            self.anim_group.addAnimation(self.pos_anim)
            self.anim_group.start()
            
            # Hide signup fields
            self.signup_fields_widget.setVisible(False)
            
            # Change button function
            self.signup_button.clicked.disconnect()
            self.signup_button.clicked.connect(self.toggle_signup_mode)
            
            # Update separator text
            self.or_label.setText("OR")
            
            # Scroll to see the full login form
            QtCore.QTimer.singleShot(100, lambda: self.scroll_area.ensureWidgetVisible(self.login_button))
        
        # Clear any previous messages
        self.hide_message()

    def display_message(self, message, success):
        """Display message with slide-down animation"""
        self.message_label.setText(message)
        
        # Set appropriate style
        if success:
            self.message_label.setStyleSheet("""
                background-color: #4caf50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                font-family: 'Segoe UI';
            """)
        else:
            self.message_label.setStyleSheet("""
                background-color: #f44336;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-size: 14px;
                font-family: 'Segoe UI';
            """)
        
        # Show with animation
        self.message_label.setVisible(True)
        
        # Create height animation
        self.msg_animation = QtCore.QPropertyAnimation(self.message_label, b"minimumHeight")
        self.msg_animation.setDuration(200)
        self.msg_animation.setStartValue(0)
        self.msg_animation.setEndValue(40)
        self.msg_animation.start()
        
        # Auto-hide message after 4 seconds
        QtCore.QTimer.singleShot(4000, self.hide_message)

    def hide_message(self):
        """Hide message with slide-up animation"""
        if self.message_label.isVisible():
            # Create hide animation
            self.msg_hide_animation = QtCore.QPropertyAnimation(self.message_label, b"minimumHeight")
            self.msg_hide_animation.setDuration(200)
            self.msg_hide_animation.setStartValue(self.message_label.height())
            self.msg_hide_animation.setEndValue(0)
            self.msg_hide_animation.finished.connect(lambda: self.message_label.setVisible(False))
            self.msg_hide_animation.start()

    def shake_animation(self, widget):
        """Create a shake animation for error feedback"""
        animation = QtCore.QPropertyAnimation(widget, b"pos")
        animation.setDuration(200)
        animation.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        
        original_pos = widget.pos()
        
        # Define shake positions
        positions = [
            original_pos + QtCore.QPoint(-10, 0),
            original_pos + QtCore.QPoint(10, 0),
            original_pos + QtCore.QPoint(-10, 0),
            original_pos + QtCore.QPoint(10, 0),
            original_pos
        ]
        
        # Add positions to animation
        for i, pos in enumerate(positions):
            animation.setKeyValueAt(i/4, pos)
        
        animation.start()


    # ------------------------- Signup Handling -------------------------
    def handle_signup(self):
        """Handle signup button press and ensure scrolling & spacing adjustments."""
        # Ensure the main scroll area shows scrollbars as needed
        self.scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

        # Adjust spacing between signup fields dynamically in case layout was not applied
        if self.signup_fields_widget.layout():
            self.signup_fields_widget.layout().setSpacing(40)

        # Gather input values
        worker_id = self.username_input.text().strip()
        password = self.password_input.text().strip()
        full_name = self.fullname_input.text().strip()
        role = self.role_input.currentText()
        phone = self.phone_input.text().strip()

        # Validate inputs
        if not worker_id or not password or not full_name or not phone:
            self.display_message("Please fill in all fields", False)
            self.shake_animation(self.login_frame)
            # Scroll to top of the form to show the message
            QtCore.QTimer.singleShot(50, lambda: self.scroll_area.verticalScrollBar().setValue(0))
            return

        # Show loading state on signup button
        self.signup_button.setText("Registering...")
        self.signup_button.setEnabled(False)

        # Simulate processing delay before actual DB logic
        QtCore.QTimer.singleShot(
            800,
            lambda: self.process_signup(worker_id, password, full_name, role, phone)
        )


    # ------------------------- Process Signup -------------------------
    def process_signup(self, worker_id, password, full_name, role, phone):
        """Perform the actual signup database insertion."""
        try:
            connection = oracledb.connect(
                # user="system",
                # password="Abdo2004@",
                # dsn="localhost:1521/FREE"
                user="system", 
                password="s2004b22", 
                dsn="192.168.21.1:1521/FREE"
            )
            cursor = connection.cursor()

            # Check for existing worker_id
            check_query = """
                SELECT COUNT(*) FROM employees
                WHERE worker_id = :worker_id
            """
            cursor.execute(check_query, {"worker_id": worker_id})
            exists = cursor.fetchone()[0] > 0

            if exists:
                self.display_message("Worker ID already exists!", False)
                self.shake_animation(self.login_frame)
                self.signup_button.setText("Register")
                self.signup_button.setEnabled(True)
                # Scroll to show the error
                QtCore.QTimer.singleShot(
                    50,
                    lambda: self.scroll_area.verticalScrollBar().setValue(
                        self.scroll_area.verticalScrollBar().maximum()
                    )
                )
                return

            # Insert the new employee record
            insert_query = """
                INSERT INTO employees
                (worker_id, password, full_name, role, phone_number)
                VALUES
                (:worker_id, :password, :full_name, :role, :phone)
            """
            cursor.execute(insert_query, {
                "worker_id": worker_id,
                "password": password,
                "full_name": full_name,
                "role": role,
                "phone": phone
            })
            connection.commit()

            # Success feedback
            self.display_message("Account created successfully!", True)

            # After a short delay, switch back to login mode
            QtCore.QTimer.singleShot(1500, self.toggle_signup_mode)

        except oracledb.DatabaseError as e:
            # Handle database errors gracefully
            self.display_message(f"Database Error: {str(e)}", False)
            self.shake_animation(self.login_frame)
        finally:
            # Restore signup button state
            self.signup_button.setText("Register")
            self.signup_button.setEnabled(True)
            # Clean up DB resources
            try:
                cursor.close()
                connection.close()
            except:
                pass


    # ------------------------- Login Handling -------------------------
    def handle_login(self):
        """Handle login button press, including canceling signup if active."""
        # If currently in signup mode, treat this as a cancel action
        if self.is_signup_mode:
            self.toggle_signup_mode()
            return

        worker_id = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not worker_id or not password:
            self.display_message("Please enter both Worker ID and Password", False)
            self.shake_animation(self.login_frame)
            return

        # Show loading state
        self.login_button.setText("Signing In...")
        self.login_button.setEnabled(False)

        # Simulate processing delay before actual login logic
        QtCore.QTimer.singleShot(800, lambda: self.process_login(worker_id, password))


    # ------------------------- Process Login -------------------------
    def process_login(self, worker_id, password):
        """Perform the actual login verification against the database."""
        try:
            connection = oracledb.connect(
                # user="system",
                # password="Abdo2004@",
                # dsn="localhost:1521/FREE"
                user="system", 
                password="s2004b22", 
                dsn="192.168.21.1:1521/FREE"
            )
            cursor = connection.cursor()

            # Fetch stored credentials
            query = """
                SELECT full_name, role, password
                FROM employees
                WHERE worker_id = :worker_id
            """
            cursor.execute(query, {"worker_id": worker_id})
            result = cursor.fetchone()

            # Verify credentials
            if result and result[2] == password:
                full_name, role = result[0], result[1]
                print("Login successful, proceeding to main")
                # Show success message
                self.display_message(f"Welcome back, {full_name}!", True)

                # Update login button style to success
                self.login_button.setText("Success!")
                self.login_button.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(
                            x1:0, y1:0, x2:1, y2:0,
                            stop:0 #2e7d32, stop:1 #4caf50
                        );
                        color: white;
                        border-radius: 25px;
                        border: none;
                    }
                """)

                # Proceed to main UI after a brief pause
                QtCore.QTimer.singleShot(
                    1000,
                    lambda: self.proceed_to_main(worker_id, full_name, role)
                )
            else:
                # Invalid credentials feedback
                self.display_message("Invalid Worker ID or Password", False)
                self.shake_animation(self.login_frame)

                # Restore login button
                self.login_button.setText("Sign In")
                self.login_button.setEnabled(True)
                self.login_button.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(
                            x1:0, y1:0, x2:1, y2:0,
                            stop:0 #303f9f, stop:1 #3f51b5
                        );
                        color: white;
                        border-radius: 25px;
                        border: none;
                    }
                    QPushButton:hover {
                        background: qlineargradient(
                            x1:0, y1:0, x2:1, y2:0,
                            stop:0 #3949ab, stop:1 #5c6bc0
                        );
                    }
                    QPushButton:pressed {
                        background: qlineargradient(
                            x1:0, y1:0, x2:1, y2:0,
                            stop:0 #283593, stop:1 #3f51b5
                        );
                    }
                """)
        except oracledb.DatabaseError as e:
            self.display_message(f"Database Error: {str(e)}", False)
            self.login_button.setText("Sign In")
            self.login_button.setEnabled(True)
        finally:
            try:
                cursor.close()
                connection.close()
            except:
                pass


    # ------------------------- Transition to Main -------------------------
    def proceed_to_main(self, worker_id, full_name, role):
   
     print("proceed_to_main called")  # Debug
     if self.main_window:
        # Store the transition parameters as instance variables
        self._transition_worker_id = worker_id
        self._transition_full_name = full_name
        self._transition_role = role
        
        # Create fade animation
        self.fade_anim = QtCore.QPropertyAnimation(self, b"windowOpacity")
        self.fade_anim.setDuration(500)
        self.fade_anim.setStartValue(1.0)
        self.fade_anim.setEndValue(0.0)
        
        # Connect signal using lambda with stored parameters
        self.fade_anim.finished.connect(
            lambda: self.show_splash_screen(
                self._transition_worker_id,
                self._transition_full_name,
                self._transition_role
            )
        )
        self.fade_anim.start()
     else:
        print("No main_window reference!")  # Debug


    # ------------------------- Splash Screen -------------------------
    def show_splash_screen(self, worker_id, full_name, role):
     print("Attempting to show splash screen")  # Debug
     if self.main_window:
        print(f"Main window exists: {self.main_window}")  # Debug
        splash = SplashScreen(self.main_window, worker_id, full_name, role)
        self.main_window.addWidget(splash)
        self.main_window.setCurrentWidget(splash)
        print("Splash screen should be visible now")  # Debug
        
        QtCore.QTimer.singleShot(2000, 
            lambda: self.show_workspace(worker_id, full_name, role))
# in show_splash_screen
    # ------------------------- Main Workspace -------------------------
    def show_workspace(self, worker_id, full_name, role):
        """Load and display the main application workspace."""
        # remember if there was an active workspace
        print("Timer fired, showing workspace") 
        active_ws = MainWindow.active_workspace
 
        # create the real main window (your workspace)
        workspace = MainWindow(
            worker_id,
            full_name,
            role,
            main_window=self.main_window
        )
        self.main_window.addWidget(workspace)
        self.main_window.setCurrentWidget(workspace)

        # if the user had an active page before, restore it
        if active_ws:
            workspace.handle_workspace_click(None, active_ws)

        # fade it in
        fade_in = QtCore.QPropertyAnimation(workspace, b"windowOpacity")
        fade_in.setDuration(500)
        fade_in.setStartValue(0.0)
        fade_in.setEndValue(1.0)
        fade_in.start()


# ------------------------- SplashScreen Widget -------------------------
class SplashScreen(QtWidgets.QWidget):
    def __init__(self, main_window, worker_id, full_name, role, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        self.worker_id = worker_id
        self.full_name = full_name
        self.role = role

        # frameless & translucent so only our styled container shows
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.counter = 0
        self.n = 100  # total progress steps
        self._init_ui()

        # start a timer to drive the progress bar
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._loading_step)
        self.timer.start(30)

    def _init_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        # big container with your splash image
        container = QtWidgets.QWidget()
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
        cl = QtWidgets.QVBoxLayout(container)
        cl.setContentsMargins(20, 20, 20, 20)
        cl.setSpacing(10)
        cl.setAlignment(QtCore.Qt.AlignCenter)

        # welcome text
        self.labelWelcome = QtWidgets.QLabel(
            f"WELCOME {self.role} {self.full_name.upper()}"
        )
        self.labelWelcome.setAlignment(QtCore.Qt.AlignCenter)
        self.labelWelcome.setWordWrap(True)
        self.labelWelcome.setStyleSheet(
            "color: black; font-size: 30px; font-weight: bold;"
        )
        cl.addWidget(self.labelWelcome)

        # loading text
        self.labelLoading = QtWidgets.QLabel("loading...")
        self.labelLoading.setAlignment(QtCore.Qt.AlignCenter)
        self.labelLoading.setStyleSheet("color: black; font-size: 16px;")
        cl.addWidget(self.labelLoading)

        # progress bar
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setFixedHeight(30)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setFormat('%p%')
        self.progressBar.setRange(0, self.n)
        self.progressBar.setValue(0)
        cl.addWidget(self.progressBar)

        layout.addWidget(container)

    def _loading_step(self):
     self.progressBar.setValue(self.counter)

    # update loading text at milestones
     if self.counter == int(self.n * 0.3):
        self.labelLoading.setText("loading... [30%]")
     elif self.counter == int(self.n * 0.6):
        self.labelLoading.setText("loading... [60%]")

    # once complete, stop the timer (but don't transition - that's handled by show_workspace)
     if self.counter >= self.n:
        self.timer.stop()
        return

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
    active_workspace = None
    def __init__(self, worker_id, full_name, role, main_window=None, parent=None):
        super().__init__(parent)
        print(f"HomePage initialized with main_window: {main_window}")  # Debug
        self.main_window = main_window
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
        MainWindow.active_workspace = workspace  # Set the active workspace
        if workspace == "Patients Space":
            widget = PatientWidget(self.worker_id, self.full_name, self.role, main_window=self.main_window)
        elif workspace == "Data Dashboard":
            widget = DiseaseStatsDashboard(self.worker_id, self.full_name, self.role, main_window=self.main_window)
        elif workspace == "Worker Timing":
            widget = WorkerTimingSpace(self.worker_id, self.full_name, self.role, main_window=self.main_window)
        else:
            return
        self.main_window.addWidget(widget)
        self.main_window.setCurrentWidget(widget)

    def logout(self):
    # Reset the login page before switching back
     login_page = self.main_window.widget(0)  # Assuming login page is at index 0
     if isinstance(login_page, HomePage):
        # Reset login button text and style
        login_page.login_button.setText("Sign In")
        login_page.login_button.setEnabled(True)
        login_page.login_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #303f9f, stop:1 #3f51b5);
                color: white;
                border-radius: 25px;
                border: none;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3949ab, stop:1 #5c6bc0);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #283593, stop:1 #3f51b5);
            }
        """)
        # Clear input fields
        login_page.username_input.clear()
        login_page.password_input.clear()
        # Hide any messages
        login_page.hide_message()
        
    # Return to the authentication page
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
