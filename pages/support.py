from PyQt5 import QtWidgets, QtCore, QtGui

class SuportPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Set base styling for the page
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                color: #333333;
            }
            QPushButton {
                background-color: #0056b3;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #003d82;
            }
        """)
        
        # Header section
        header = QtWidgets.QWidget()
        header_layout = QtWidgets.QHBoxLayout(header)
        
        # Title
        title_label = QtWidgets.QLabel("Support Center")
        title_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #0056b3;")
        header_layout.addWidget(title_label)
        
        # Add the header to main layout
        main_layout.addWidget(header)
        
        # Content container (white card)
        content_container = QtWidgets.QFrame()
        content_container.setFrameShape(QtWidgets.QFrame.StyledPanel)
        content_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        content_layout = QtWidgets.QVBoxLayout(content_container)
        content_layout.setContentsMargins(25, 25, 25, 25)
        content_layout.setSpacing(20)
        
        # Support intro text
        intro_label = QtWidgets.QLabel("Our support team is here to help you with any issues or questions.")
        intro_label.setWordWrap(True)
        intro_label.setStyleSheet("font-size: 16px;")
        content_layout.addWidget(intro_label)
        
        # Support options section
        support_options = QtWidgets.QWidget()
        options_layout = QtWidgets.QGridLayout(support_options)
        options_layout.setVerticalSpacing(15)
        options_layout.setHorizontalSpacing(20)
        
        # Support options with icons
        options = [
            ("Email Support", "✉️ techsupport@hospitalapp.com", self.email_support),
            ("Live Chat", "💬 Chat with our team in real-time", self.open_chat),
            ("Help Center", "📖 Browse our knowledge base", self.open_help_center),
            ("Phone Support", "📞 Call us at +1 (800) 555-1234", self.call_support)
        ]
        
        for i, (title, desc, func) in enumerate(options):
            option_widget = self.create_support_option(title, desc, func)
            options_layout.addWidget(option_widget, i // 2, i % 2)
        
        content_layout.addWidget(support_options)
        
        # Hours of operation
        hours_label = QtWidgets.QLabel("Support Hours: Monday-Friday, 8:00 AM - 8:00 PM EST")
        hours_label.setStyleSheet("font-size: 14px; color: #666;")
        hours_label.setAlignment(QtCore.Qt.AlignCenter)
        content_layout.addWidget(hours_label)
        
        # Add content container to main layout
        main_layout.addWidget(content_container)
        
        # Add spacer at the bottom
        main_layout.addStretch()
    
    def create_support_option(self, title, description, on_click):
        container = QtWidgets.QFrame()
        container.setStyleSheet("""
            QFrame {
                background-color: #f0f7ff;
                border-radius: 6px;
                padding: 5px;
            }
            QFrame:hover {
                background-color: #e0f0ff;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(container)
        layout.setContentsMargins(15, 15, 15, 15)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #0056b3;")
        
        desc_label = QtWidgets.QLabel(description)
        desc_label.setWordWrap(True)
        desc_label.setStyleSheet("font-size: 14px; color: #444;")
        
        button = QtWidgets.QPushButton("Connect")
        button.setFixedWidth(100)
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.clicked.connect(on_click)
        
        layout.addWidget(title_label)
        layout.addWidget(desc_label)
        layout.addWidget(button, 0, QtCore.Qt.AlignRight)
        
        return container
    
    # Support action methods
    def email_support(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("mailto:techsupport@hospitalapp.com"))
    
    def open_chat(self):
        # Implementation for opening live chat
        print("Opening live chat interface")
    
    def open_help_center(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://hospitalapp.com/help"))
    
    def call_support(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("tel:+18005551234"))