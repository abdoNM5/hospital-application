from PyQt5 import QtWidgets, QtCore, QtGui
import smtplib
from email.mime.text import MIMEText
import os

class ContactPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        # Main layout
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Create stacked widget with background
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.setObjectName("contactStackedWidget")
        
        # Create the contact form page
        self.contact_form_page = QtWidgets.QWidget()
        self.setup_contact_form()
        self.stacked_widget.addWidget(self.contact_form_page)
        
        # Create the confirmation page
        self.confirmation_page = QtWidgets.QWidget()
        self.setup_confirmation_page()
        self.stacked_widget.addWidget(self.confirmation_page)
        
        # Add stacked widget to main layout
        self.main_layout.addWidget(self.stacked_widget)
        
        # Style the widget
        self.setStyleSheet("""
            QWidget#contactStackedWidget {
                background-image: url('resources/app2bg.jpg');
                background-repeat: no-repeat;
                background-position: center;
                background-attachment: fixed;
            }
            
            QFrame#contactFrame {
                background-color: rgba(255, 255, 255, 220);
                border-radius: 10px;
                padding: 20px;
            }
            
            QLabel#titleLabel {
                font-size: 24px;
                font-weight: bold;
                color: #333333;
            }
            
            QLineEdit, QTextEdit {
                padding: 8px;
                border: 1px solid #cccccc;
                border-radius: 5px;
                background-color: white;
            }
            
            QPushButton#sendButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            
            QPushButton#sendButton:hover {
                background-color: #45a049;
            }
            
            QLabel#socialIconLabel {
                margin: 0 10px;
            }
        """)
    
    def setup_contact_form(self):
        # Layout for the contact form page
        page_layout = QtWidgets.QVBoxLayout(self.contact_form_page)
        page_layout.setAlignment(QtCore.Qt.AlignCenter)
        
        # Create a frame to hold the contact form
        self.contact_frame = QtWidgets.QFrame()
        self.contact_frame.setObjectName("contactFrame")
        self.contact_frame.setMinimumWidth(500)
        self.contact_frame.setMaximumWidth(600)
        
        # Contact frame layout
        frame_layout = QtWidgets.QVBoxLayout(self.contact_frame)
        
        # Title
        title_label = QtWidgets.QLabel("Contact Us")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        frame_layout.addWidget(title_label)
        
        # Form layout
        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(15)
        
        # Name field
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Your Name")
        form_layout.addRow("Name:", self.name_input)
        
        # Email field
        self.email_input = QtWidgets.QLineEdit()
        self.email_input.setPlaceholderText("Your Email")
        form_layout.addRow("Email:", self.email_input)
        
        # Subject field
        self.subject_input = QtWidgets.QLineEdit()
        self.subject_input.setPlaceholderText("Subject")
        form_layout.addRow("Subject:", self.subject_input)
        
        # Message field
        self.message_input = QtWidgets.QTextEdit()
        self.message_input.setPlaceholderText("Your Message")
        self.message_input.setMinimumHeight(150)
        form_layout.addRow("Message:", self.message_input)
        
        frame_layout.addLayout(form_layout)
        
        # Send button
        self.send_button = QtWidgets.QPushButton("Send Message")
        self.send_button.setObjectName("sendButton")
        self.send_button.clicked.connect(self.send_email)
        frame_layout.addWidget(self.send_button, 0, QtCore.Qt.AlignCenter)
        
        # Social media icons
        social_layout = QtWidgets.QHBoxLayout()
        social_layout.setAlignment(QtCore.Qt.AlignCenter)
        
        # Social media platforms - you'll need to replace with your actual icon paths
        social_platforms = ["facebook", "instagram", "linkedin"]
        self.social_icons = {}
        
        for platform in social_platforms:
            icon_label = QtWidgets.QLabel()
            icon_label.setObjectName("socialIconLabel")
            icon_path = f"{platform}_icon.png"  # You'll need these icon files
            
            # Check if the icon file exists (you should add your icons)
            if os.path.exists(icon_path):
                icon = QtGui.QPixmap(icon_path).scaled(32, 32, QtCore.Qt.KeepAspectRatio)
                icon_label.setPixmap(icon)
            else:
                # If icon doesn't exist yet, show the name instead
                icon_label.setText(platform.capitalize())
            
            icon_label.setCursor(QtCore.Qt.PointingHandCursor)
            self.social_icons[platform] = icon_label
            social_layout.addWidget(icon_label)
            
            # Connect click events
            icon_label.mousePressEvent = lambda event, p=platform: self.open_social_media(p)
            
        frame_layout.addSpacing(20)
        frame_layout.addLayout(social_layout)
        
        # Add the frame to the page layout
        page_layout.addWidget(self.contact_frame)
        
    def setup_confirmation_page(self):
        # Layout for confirmation page
        page_layout = QtWidgets.QVBoxLayout(self.confirmation_page)
        page_layout.setAlignment(QtCore.Qt.AlignCenter)
        
        # Create a frame for confirmation message
        confirm_frame = QtWidgets.QFrame()
        confirm_frame.setObjectName("contactFrame")
        confirm_frame.setMinimumWidth(500)
        confirm_frame.setMaximumWidth(600)
        
        # Confirmation layout
        confirm_layout = QtWidgets.QVBoxLayout(confirm_frame)
        
        # Confirmation message
        confirm_label = QtWidgets.QLabel("Thank you for your message!")
        confirm_label.setObjectName("titleLabel")
        confirm_label.setAlignment(QtCore.Qt.AlignCenter)
        confirm_layout.addWidget(confirm_label)
        
        detail_label = QtWidgets.QLabel("Your message has been sent successfully. We'll get back to you soon!")
        detail_label.setAlignment(QtCore.Qt.AlignCenter)
        confirm_layout.addWidget(detail_label)
        
        # Back button
        back_button = QtWidgets.QPushButton("Back to Contact Form")
        back_button.setObjectName("sendButton")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        confirm_layout.addWidget(back_button, 0, QtCore.Qt.AlignCenter)
        
        # Add the frame to the page layout
        page_layout.addWidget(confirm_frame)
    
    def send_email(self):
        """Send email to the specified recipient"""
        # Get form data
        sender_name = self.name_input.text()
        sender_email = self.email_input.text()
        subject = self.subject_input.text()
        message_content = self.message_input.toPlainText()
        
        # Recipient email (hardcoded as per requirements)
        recipient_email = "nmiraabdellader@gmail.com"
        
        # Validate inputs
        if not all([sender_name, sender_email, subject, message_content]):
            QtWidgets.QMessageBox.warning(self, "Incomplete Form", 
                                        "Please fill in all fields before sending.")
            return
        
        try:
            # Here we would normally send the email, but since we need SMTP credentials,
            # we'll just simulate success for now. In a real application, you would 
            # configure SMTP server details.
            
            # Example of how to send email (commented out because it needs credentials)
            """
            msg = MIMEText(f"Message from: {sender_name} <{sender_email}>\n\n{message_content}")
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = recipient_email
            
            # Connect to SMTP server (example for Gmail)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login('your_email@gmail.com', 'your_password')  # You would need to use app password
            server.send_message(msg)
            server.quit()
            """
            
            # Clear the form
            self.name_input.clear()
            self.email_input.clear()
            self.subject_input.clear()
            self.message_input.clear()
            
            # Show the confirmation page
            self.stacked_widget.setCurrentIndex(1)
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to send email: {str(e)}")
    
    def open_social_media(self, platform):
        """Open social media links when icons are clicked"""
        # You can replace these URLs with your actual social media profiles
        urls = {
            "facebook": "https://www.facebook.com/yourpage",
            "instagram": "https://www.instagram.com/yourprofile",
            "linkedin": "https://www.linkedin.com/in/yourprofile"
        }
        
        if platform in urls:
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(urls[platform]))