from PyQt5 import QtWidgets, QtGui, QtCore

class DevelopersPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Main layout with more spacing
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Set a light background color as fallback
        self.setStyleSheet("background-color: #f5f5f5;")
        
        # Title with better visibility
        title_container = QtWidgets.QWidget()
        title_container.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.85); 
            border-radius: 10px; 
            padding: 15px;
        """)
        title_layout = QtWidgets.QVBoxLayout(title_container)
        
        # Title
        self.title_label = QtWidgets.QLabel("Meet Our Developers")
        self.title_label.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #333;
        """)
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_layout.addWidget(self.title_label)
        
        # Description text
        self.description_label = QtWidgets.QLabel(
            "This application is developed by a dedicated team of two passionate developers, "
            "working together page by page to build a complete hospital management system."
        )
        self.description_label.setStyleSheet("font-size: 14px; color: #555;")
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(QtCore.Qt.AlignCenter)
        title_layout.addWidget(self.description_label)
        
        self.layout.addWidget(title_container)
        
        # Scrollable area for developers
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        # Container widget for the scrollable content
        scroll_content = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(10, 10, 10, 10)
        
        # Developers grid layout
        dev_grid = QtWidgets.QGridLayout()
        dev_grid.setSpacing(20)
        dev_grid.setContentsMargins(0, 0, 0, 0)
        
        developers = [
            {
                "name": "ABDELKADER ANMIRA",
                "role": "Lead Developer",
                "image": "resources/abdo.jpg",  # Use forward slashes for cross-platform compatibility
                "education": "DATA ENGINEERING STUDENT at ENSAH",
                "skills": ["Python", "PyQt5", "Database Design", "web development"],
                "contact": "anmiraabdelkader@gmail.com"
            },
            {
                "name": "SOUFIANE BOUZIANNI",
                "role": "Lead Developer",
                "image": "resources/soufiane.jpg",
                "education": "DATA ENGINEERING STUDENT at ENSAH",
                "skills": ["Python", "PyQt5", "Database Design", "web development"],
                "contact": "abdelkbirzeblkbir@gmail.com"
            }
        ]
        
        for i, dev_info in enumerate(developers):
            dev_card = self.create_developer_card(dev_info)
            dev_grid.addWidget(dev_card, i // 2, i % 2)
        
        scroll_layout.addLayout(dev_grid)
        scroll_area.setWidget(scroll_content)
        self.layout.addWidget(scroll_area)

    def create_developer_card(self, dev_info):
        card = QtWidgets.QWidget()
        card.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
            padding: 15px;
        """)
        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setSpacing(10)
        
        # Profile picture
        profile_pic = QtWidgets.QLabel()
        try:
            pixmap = QtGui.QPixmap(dev_info["image"])
            if not pixmap.isNull():
                profile_pic.setPixmap(pixmap.scaled(
                    180, 180, 
                    QtCore.Qt.KeepAspectRatio, 
                    QtCore.Qt.SmoothTransformation
                ))
            else:
                profile_pic.setText("Image not found")
                profile_pic.setStyleSheet("background-color: #eee; padding: 60px;")
        except Exception as e:
            profile_pic.setText(f"Error loading image: {str(e)}")
            profile_pic.setStyleSheet("background-color: #fee; padding: 60px;")
        
        profile_pic.setAlignment(QtCore.Qt.AlignCenter)
        profile_pic.setMinimumSize(180, 180)
        card_layout.addWidget(profile_pic)
        
        # Name and role
        name_label = QtWidgets.QLabel(dev_info["name"])
        name_label.setStyleSheet("font-weight: bold; font-size: 18px; color: #333;")
        name_label.setAlignment(QtCore.Qt.AlignCenter)
        card_layout.addWidget(name_label)
        
        role_label = QtWidgets.QLabel(dev_info["role"])
        role_label.setStyleSheet("color: #555; font-size: 15px;")
        role_label.setAlignment(QtCore.Qt.AlignCenter)
        card_layout.addWidget(role_label)
        
        # Information sections
        sections = [
            ("Education", dev_info["education"]),
            ("Skills", ", ".join(dev_info["skills"])),
            ("Contact", dev_info["contact"])
        ]
        
        for title, content in sections:
            section = self.create_info_section(title, content)
            card_layout.addWidget(section)
        
        return card
    
    def create_info_section(self, title, content):
        section = QtWidgets.QWidget()
        section_layout = QtWidgets.QVBoxLayout(section)
        section_layout.setContentsMargins(0, 5, 0, 5)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("""
            font-weight: bold; 
            color: #333; 
            font-size: 14px;
            margin-bottom: 3px;
        """)
        
        content_label = QtWidgets.QLabel(content)
        content_label.setStyleSheet("color: #555; font-size: 13px;")
        content_label.setWordWrap(True)
        
        section_layout.addWidget(title_label)
        section_layout.addWidget(content_label)
        
        return section