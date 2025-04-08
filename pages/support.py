from PyQt5 import QtWidgets, QtCore

class SuportPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)
        self.setStyleSheet("background-color: #fce4ec; padding: 20px;")
        
        # Title
        self.title_label = QtWidgets.QLabel("🛠 Support")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #880e4f;")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.title_label)
        
        # Support Information
        self.support_info = QtWidgets.QLabel("""
        💻 For technical support, please contact us via:
        ✉ Email: techsupport@hospitalapp.com
        💬 Live Chat: Available on our website
        📖 FAQ: Visit our Help Center for common questions
        """)
        self.support_info.setStyleSheet("font-size: 16px; color: #ad1457; text-align: center; padding: 15px; background-color: white; border-radius: 10px;")
        self.support_info.setAlignment(QtCore.Qt.AlignCenter)
        self.support_info.setWordWrap(True)
        self.layout.addWidget(self.support_info)