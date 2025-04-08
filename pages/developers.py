from PyQt5 import QtWidgets, QtGui, QtCore

class DevelopersPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Set background image directly on the widget
        self.setAutoFillBackground(True)
        palette = self.palette()
        background_image = QtGui.QPixmap("resources/appbg.png")
        if not background_image.isNull():
            palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(background_image))
        else:
            # Fallback if image not found
            palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#f5f5f5"))
        self.setPalette(palette)
        
        self.setup_ui()

    def setup_ui(self):
        # Main layout with more spacing
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Title with better visibility
        title_container = QtWidgets.QWidget()
        title_container.setStyleSheet("background-color: rgba(255, 255, 255, 0.85); border-radius: 10px; padding: 15px;")
        title_layout = QtWidgets.QVBoxLayout(title_container)
        
        # Title
        self.title_label = QtWidgets.QLabel("Meet Our Developers")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_layout.addWidget(self.title_label)
        
        # Description text
        self.description_label = QtWidgets.QLabel("This application is developed by a dedicated team of two passionate developers, working together page by page to build a complete hospital management system.")
        self.description_label.setStyleSheet("font-size: 14px; color: #555;")
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(QtCore.Qt.AlignCenter)
        title_layout.addWidget(self.description_label)
        
        self.layout.addWidget(title_container)
        
        # Scrollable area for developers to ensure all content is visible
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        
        # Container widget for the scrollable content
        scroll_content = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
        
        # Developers grid layout
        dev_grid = QtWidgets.QGridLayout()
        dev_grid.setSpacing(20)
        dev_grid.setContentsMargins(0, 0, 0, 0)
        
        developers = [
            {
                "name": "ABDELKADER ANMIRA",
                "role": "Lead Developer",
                "image": r"resources\abdo.jpg",
                "education": "DATA ENGINEERING STUDENT at ENSAH",
                "skills": ["Python", "PyQt5", "Database Design","web developement"],
                "contact": "anmiraabdelkader@gmail.com"
            },
            {
                "name": "SOUFIANE BOUZIANNI",
                "role": "Lead Developer",
                "image": r"resources\soufiane.jpg",
                "education": "DATA ENGINEERING STUDENT at ENSAH",
                "skills": ["Python", "PyQt5", "Database Design","web developement"],
                "contact": "abdelkbirzeblkbir@gmail.com"
            }
        ]
        
        for i, dev_info in enumerate(developers):
            dev_card = self.create_developer_card(dev_info)
            # Position cards in grid (2 columns)
            dev_grid.addWidget(dev_card, i // 2, i % 2)
        
        scroll_layout.addLayout(dev_grid)
        scroll_area.setWidget(scroll_content)
        self.layout.addWidget(scroll_area)

    def create_developer_card(self, dev_info):
        # Main card widget with compact layout
        card = QtWidgets.QWidget()
        card_layout = QtWidgets.QVBoxLayout(card)
        card_layout.setSpacing(8)
        card_layout.setContentsMargins(0, 0, 0, 0)
        
        # Container for profile pic and name/role
        top_container = QtWidgets.QWidget()
        top_container.setStyleSheet("background-color: rgba(255, 255, 255, 0.85); border-radius: 10px; padding: 15px;")
        top_layout = QtWidgets.QVBoxLayout(top_container)
        top_layout.setSpacing(10)
        
        # Profile picture - LARGER SIZE
        profile_pic = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(dev_info["image"])
        if not pixmap.isNull():
            # Increased size from 120x120 to 180x180
            profile_pic.setPixmap(pixmap.scaled(180, 180, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
            # Set minimum size to ensure the image has enough space
            profile_pic.setMinimumSize(180, 180)
        else:
            profile_pic.setText("No Image")
            profile_pic.setStyleSheet("background-color: #ddd; padding: 60px;")
            profile_pic.setMinimumSize(180, 180)
        profile_pic.setAlignment(QtCore.Qt.AlignCenter)
        top_layout.addWidget(profile_pic)
        
        # Name and role
        name_label = QtWidgets.QLabel(dev_info["name"])
        name_label.setStyleSheet("font-weight: bold; font-size: 18px; color: #333;") # Increased font size
        name_label.setAlignment(QtCore.Qt.AlignCenter)
        
        role_label = QtWidgets.QLabel(dev_info["role"])
        role_label.setStyleSheet("color: #555; font-size: 15px;") # Increased font size
        role_label.setAlignment(QtCore.Qt.AlignCenter)
        
        top_layout.addWidget(name_label)
        top_layout.addWidget(role_label)
        card_layout.addWidget(top_container)
        
        # Information container with all info frames
        info_container = QtWidgets.QWidget()
        info_container.setStyleSheet("background-color: rgba(255, 255, 255, 0.85); border-radius: 10px; margin-top: 8px;")
        info_layout = QtWidgets.QVBoxLayout(info_container)
        info_layout.setSpacing(10)
        
        # Education section
        edu_section = self.create_info_section("Education", dev_info["education"])
        info_layout.addWidget(edu_section)
        
        # Add separator
        separator1 = QtWidgets.QFrame()
        separator1.setFrameShape(QtWidgets.QFrame.HLine)
        separator1.setFrameShadow(QtWidgets.QFrame.Sunken)
        separator1.setStyleSheet("background-color: #ccc; max-height: 1px;")
        info_layout.addWidget(separator1)
        
        # Skills section
        skills_section = self.create_info_section("Skills", ", ".join(dev_info["skills"]))
        info_layout.addWidget(skills_section)
        
        # Add separator
        separator2 = QtWidgets.QFrame()
        separator2.setFrameShape(QtWidgets.QFrame.HLine)
        separator2.setFrameShadow(QtWidgets.QFrame.Sunken)
        separator2.setStyleSheet("background-color: #ccc; max-height: 1px;")
        info_layout.addWidget(separator2)
        
        # Contact section
        contact_section = self.create_info_section("Contact", dev_info["contact"])
        info_layout.addWidget(contact_section)
        
        card_layout.addWidget(info_container)
        
        return card
    
    def create_info_section(self, title, content):
        """Create a section with title and content"""
        section = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(section)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(2)
        
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet("font-weight: bold; color: #333; font-size: 14px;")
        
        content_label = QtWidgets.QLabel(content)
        content_label.setStyleSheet("color: #555; font-size: 13px;")
        content_label.setWordWrap(True)
        
        layout.addWidget(title_label)
        layout.addWidget(content_label)
        
        return section

        self.setStyleSheet("background-color: #f5f5f5; padding: 20px;")
        
        # Title
        self.title_label = QtWidgets.QLabel("Meet Our Developers")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.title_label)
        
        # Description text
        self.description_label = QtWidgets.QLabel("This application is developed by a dedicated team of two passionate developers, working together page by page to build a complete hospital management system.")
        self.description_label.setStyleSheet("font-size: 14px; color: #555; text-align: center; padding: 10px;")
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.description_label)
        
        # Developers list
        developers = [
            ("You", "Developer", "profile1.png"),
            ("Your Friend", "Developer", "profile2.png")
        ]
        
        grid_layout = QtWidgets.QGridLayout()
        
        for i, (name, role, image) in enumerate(developers):
            dev_widget = self.create_developer_card(name, role, image)
            grid_layout.addWidget(dev_widget, i // 2, i % 2)
        
        self.layout.addLayout(grid_layout)

    def create_developer_card(self, name, role, image):
        card = QtWidgets.QWidget()
        card_layout = QtWidgets.QVBoxLayout(card)
        
        profile_pic = QtWidgets.QLabel()
        pixmap = QtGui.QPixmap(image).scaled(80, 80, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        profile_pic.setPixmap(pixmap)
        profile_pic.setAlignment(QtCore.Qt.AlignCenter)
        
        name_label = QtWidgets.QLabel(name)
        name_label.setStyleSheet("font-weight: bold; text-align: center;")
        name_label.setAlignment(QtCore.Qt.AlignCenter)
        
        role_label = QtWidgets.QLabel(role)
        role_label.setStyleSheet("color: gray; text-align: center;")
        role_label.setAlignment(QtCore.Qt.AlignCenter)
        
        card_layout.addWidget(profile_pic)
        card_layout.addWidget(name_label)
        card_layout.addWidget(role_label)
        
        card.setStyleSheet("background-color: white; border-radius: 10px; padding: 10px;")
        return card
