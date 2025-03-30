from PyQt5 import QtWidgets, QtGui, QtCore

class DevelopersPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        self.layout = QtWidgets.QVBoxLayout(self)
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
