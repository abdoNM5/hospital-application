# Import your page classes (they must be defined in their own files)
from pages.home import HomePage
from pages.developers import DevelopersPage
from pages.contact import ContactPage
from pages.support import SuportPage


from pages.abtus import AbtusPage
from pages.exit_page import ExitPage

from pages.abtus import AboutUsPage


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(919, 600)
        
        # Main central widget and primary layout
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Create main horizontal layout to hold sidebar and content
        self.main_horizontal_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.main_horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.main_horizontal_layout.setSpacing(0)
        
        # Create a sidebar container widget that will hold both sidebar types
        self.sidebar_container = QtWidgets.QWidget()
        self.sidebar_container.setMinimumWidth(50)
        self.sidebar_container.setMaximumWidth(190)
        
        # Create stacked layout for the two sidebar types
        self.sidebar_stacked_layout = QtWidgets.QStackedLayout(self.sidebar_container)
        self.sidebar_stacked_layout.setContentsMargins(0, 0, 0, 0)
        
        # --- Icons only sidebar ---
        self.icons_only_widget = QtWidgets.QWidget()
        self.icons_only_widget.setObjectName("icons_only_widget")
        self.icons_only_layout = QtWidgets.QVBoxLayout(self.icons_only_widget)
        self.icons_only_layout.setContentsMargins(10, 10, 10, 10)
        
        # Logo for icons-only sidebar
        self.label = QtWidgets.QLabel()
        self.label.setMinimumSize(QtCore.QSize(50, 50))
        self.label.setMaximumSize(QtCore.QSize(50, 50))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/icons/resources/iStock-471629610-Converted.png"))
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.icons_only_layout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        
        # Buttons for icons-only sidebar
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        
        # Home button
        self.home_btn = QtWidgets.QPushButton()
        self.home_btn.setMinimumSize(QtCore.QSize(40, 40))
        self.home_btn.setMaximumSize(QtCore.QSize(40, 40))
        self.home_btn.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/resources/house-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap(":/icons/resources/house-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.home_btn.setIcon(icon)
        self.home_btn.setIconSize(QtCore.QSize(20, 20))
        self.home_btn.setCheckable(True)
        self.home_btn.setAutoExclusive(True)
        self.home_btn.setObjectName("home_btn")
        self.verticalLayout.addWidget(self.home_btn)
        
        # Developers button
        self.developers_btn = QtWidgets.QPushButton()
        self.developers_btn.setMinimumSize(QtCore.QSize(40, 40))
        self.developers_btn.setMaximumSize(QtCore.QSize(40, 40))
        self.developers_btn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/resources/group-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.developers_btn.setIcon(icon1)
        self.developers_btn.setIconSize(QtCore.QSize(20, 20))
        self.developers_btn.setCheckable(True)
        self.developers_btn.setAutoExclusive(True)
        self.developers_btn.setObjectName("developers_btn")
        self.verticalLayout.addWidget(self.developers_btn)
        
        # Contact button
        self.contact_btn = QtWidgets.QPushButton()
        self.contact_btn.setMinimumSize(QtCore.QSize(40, 40))
        self.contact_btn.setMaximumSize(QtCore.QSize(40, 40))
        self.contact_btn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/resources/contacts-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.contact_btn.setIcon(icon2)
        self.contact_btn.setIconSize(QtCore.QSize(20, 20))
        self.contact_btn.setCheckable(True)
        self.contact_btn.setAutoExclusive(True)
        self.contact_btn.setObjectName("contact_btn")
        self.verticalLayout.addWidget(self.contact_btn)
        
        # Support button
        self.support_btn = QtWidgets.QPushButton()
        self.support_btn.setMinimumSize(QtCore.QSize(40, 40))
        self.support_btn.setMaximumSize(QtCore.QSize(40, 40))
        self.support_btn.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/resources/support-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.support_btn.setIcon(icon3)
        self.support_btn.setIconSize(QtCore.QSize(20, 20))
        self.support_btn.setCheckable(True)
        self.support_btn.setAutoExclusive(True)
        self.support_btn.setObjectName("support_btn")
        self.verticalLayout.addWidget(self.support_btn)
        
        # About us button
        self.abtus_btn = QtWidgets.QPushButton()
        self.abtus_btn.setMinimumSize(QtCore.QSize(40, 40))
        self.abtus_btn.setMaximumSize(QtCore.QSize(40, 40))
        self.abtus_btn.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/resources/clinic-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.abtus_btn.setIcon(icon4)
        self.abtus_btn.setIconSize(QtCore.QSize(20, 20))
        self.abtus_btn.setCheckable(True)
        self.abtus_btn.setAutoExclusive(True)
        self.abtus_btn.setObjectName("abtus_btn")
        self.verticalLayout.addWidget(self.abtus_btn)
        
        # Spacer
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        
        # Exit button
        self.exit_btn = QtWidgets.QPushButton()
        self.exit_btn.setMinimumSize(QtCore.QSize(40, 40))
        self.exit_btn.setMaximumSize(QtCore.QSize(40, 40))
        self.exit_btn.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/resources/x-mark-64.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exit_btn.setIcon(icon5)
        self.exit_btn.setIconSize(QtCore.QSize(20, 20))
        self.exit_btn.setCheckable(True)
        self.exit_btn.setAutoExclusive(True)
        self.exit_btn.setObjectName("exit_btn")
        self.verticalLayout.addWidget(self.exit_btn)
        
        self.icons_only_layout.addLayout(self.verticalLayout)
        
        # --- Full sidebar with text ---
        self.keys_only_widget = QtWidgets.QWidget()
        self.keys_only_widget.setObjectName("keys_only_widget")
        self.keys_only_layout = QtWidgets.QVBoxLayout(self.keys_only_widget)
        self.keys_only_layout.setContentsMargins(10, 10, 10, 10)
        
        # Header with logo and title
        self.header_layout = QtWidgets.QHBoxLayout()
        
        self.label_2 = QtWidgets.QLabel()
        self.label_2.setMinimumSize(QtCore.QSize(40, 40))
        self.label_2.setMaximumSize(QtCore.QSize(40, 40))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap(":/icons/resources/iStock-471629610-Converted.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.header_layout.addWidget(self.label_2)
        
        self.label_3 = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setFamily("Reem Kufi")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_3.setText("Sidebar")
        self.header_layout.addWidget(self.label_3)
        
        self.keys_only_layout.addLayout(self.header_layout)
        
        # Buttons for full sidebar
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        
        # Home button
        self.home_btn2 = QtWidgets.QPushButton()
        self.home_btn2.setIcon(icon)
        self.home_btn2.setIconSize(QtCore.QSize(14, 14))
        self.home_btn2.setCheckable(True)
        self.home_btn2.setAutoExclusive(True)
        self.home_btn2.setObjectName("home_btn2")
        self.home_btn2.setText("Home")
        self.verticalLayout_2.addWidget(self.home_btn2)
        
        # Developers button
        self.developers_btn2 = QtWidgets.QPushButton()
        self.developers_btn2.setIcon(icon1)
        self.developers_btn2.setIconSize(QtCore.QSize(14, 14))
        self.developers_btn2.setCheckable(True)
        self.developers_btn2.setAutoExclusive(True)
        self.developers_btn2.setObjectName("developers_btn2")
        self.developers_btn2.setText("Developers")
        self.verticalLayout_2.addWidget(self.developers_btn2)
        
        # Contact button
        self.contact_btn2 = QtWidgets.QPushButton()
        self.contact_btn2.setIcon(icon2)
        self.contact_btn2.setIconSize(QtCore.QSize(14, 14))
        self.contact_btn2.setCheckable(True)
        self.contact_btn2.setAutoExclusive(True)
        self.contact_btn2.setObjectName("contact_btn2")
        self.contact_btn2.setText("Contact")
        self.verticalLayout_2.addWidget(self.contact_btn2)
        
        # Support button
        self.support_btn2 = QtWidgets.QPushButton()
        self.support_btn2.setIcon(icon3)
        self.support_btn2.setIconSize(QtCore.QSize(14, 14))
        self.support_btn2.setCheckable(True)
        self.support_btn2.setAutoExclusive(True)
        self.support_btn2.setObjectName("support_btn2")
        self.support_btn2.setText("Support")
        self.verticalLayout_2.addWidget(self.support_btn2)
        
        # About us button
        self.abtus_btn2 = QtWidgets.QPushButton()
        self.abtus_btn2.setIcon(icon4)
        self.abtus_btn2.setIconSize(QtCore.QSize(14, 14))
        self.abtus_btn2.setCheckable(True)
        self.abtus_btn2.setAutoExclusive(True)
        self.abtus_btn2.setObjectName("abtus_btn2")
        self.abtus_btn2.setText("Abt us")
        self.verticalLayout_2.addWidget(self.abtus_btn2)
        
        # Spacer
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        
        # Exit button
        self.exit_btn2 = QtWidgets.QPushButton()
        self.exit_btn2.setIcon(icon5)
        self.exit_btn2.setIconSize(QtCore.QSize(14, 14))
        self.exit_btn2.setCheckable(True)
        self.exit_btn2.setAutoExclusive(True)
        self.exit_btn2.setObjectName("exit_btn2")
        self.exit_btn2.setText("EXIT")
        self.verticalLayout_2.addWidget(self.exit_btn2)
        
        self.keys_only_layout.addLayout(self.verticalLayout_2)
        
        # Add both sidebar types to the stacked layout
        self.sidebar_stacked_layout.addWidget(self.icons_only_widget)  # Index 0
        self.sidebar_stacked_layout.addWidget(self.keys_only_widget)   # Index 1
        
        # Set default to full sidebar (with text)
        self.sidebar_stacked_layout.setCurrentIndex(1)
        
        # Add sidebar container to main layout
        self.main_horizontal_layout.addWidget(self.sidebar_container)
        
        # --- Main content area ---
        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setObjectName("main_widget")
        self.main_vertical_layout = QtWidgets.QVBoxLayout(self.main_widget)
        self.main_vertical_layout.setContentsMargins(10, 10, 10, 10)
        
        # Header with sidebar toggle and title
        self.header_widget = QtWidgets.QWidget()
        self.header_layout = QtWidgets.QHBoxLayout(self.header_widget)
        self.header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Sidebar toggle button
        self.sidebar_btn = QtWidgets.QPushButton()
        self.sidebar_btn.setMinimumSize(QtCore.QSize(40, 40))
        self.sidebar_btn.setMaximumSize(QtCore.QSize(40, 40))
        self.sidebar_btn.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/icons/resources/sidebar2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sidebar_btn.setIcon(icon7)
        self.sidebar_btn.setIconSize(QtCore.QSize(22, 22))
        self.sidebar_btn.setCheckable(True)
        self.sidebar_btn.setAutoExclusive(False)
        self.sidebar_btn.setObjectName("sidebar_btn")
        self.header_layout.addWidget(self.sidebar_btn)
        
        # Spacer
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.header_layout.addItem(spacerItem2)
        
        # Title
        self.title_ensah = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setFamily("Segoe UI Light")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.title_ensah.setFont(font)
        self.title_ensah.setObjectName("title_ensah")
        self.title_ensah.setText("WELCOME TO ENSA-H HOSPITAL")
        self.header_layout.addWidget(self.title_ensah)
        
        self.main_vertical_layout.addWidget(self.header_widget)
        
        # Content area (stacked widget)
        self.stackedWidget = QtWidgets.QStackedWidget()
        self.stackedWidget.setObjectName("stackedWidget")
        
        # --- Loading pages from separate files ---

        # IMPORTANT: Pass QStackedWidget reference to HomePage so it can add the main application page after login.
        self.home_page = HomePage(main_window=self.stackedWidget)
        self.developers_page = DevelopersPage()
        self.contact_page = ContactPage()
        self.support_page = SuportPage()
        self.abtus_page = AbtusPage()
        self.exit_page = ExitPage(self.stackedWidget)  # Correct instantiation
        # IMPORTANT: Pass MainWindow reference to HomePage so it can close the main window.
        self.home_page = HomePage(main_window=MainWindow)           # instance from pages/home.py
        self.developers_page = DevelopersPage()  # instance from pages/developers.py
        self.contact_page = ContactPage()       # instance from pages/contact.py
        self.support_page = SuportPage()        # instance from pages/support.py
        self.abtus_page = AboutUsPage()           # instance from pages/abtus.py
        
        # Add the pages to the stacked widget in the desired order
        self.stackedWidget.addWidget(self.home_page)         # index 0
        self.stackedWidget.addWidget(self.developers_page)     # index 1
        self.stackedWidget.addWidget(self.contact_page)        # index 2
        self.stackedWidget.addWidget(self.support_page)        # index 3
        self.stackedWidget.addWidget(self.abtus_page)          # index 4
        self.stackedWidget.addWidget(self.exit_page)           # index 5
        
        self.main_vertical_layout.addWidget(self.stackedWidget)
        
        # Add main content to main layout
        self.main_horizontal_layout.addWidget(self.main_widget)
        
        # Set central widget
        MainWindow.setCentralWidget(self.centralwidget)
        
        # Set default page (adjust index as needed)
        self.stackedWidget.setCurrentIndex(0)
        
        # --- Connect signals ---
        # Toggle sidebar between icon-only and full modes
        self.sidebar_btn.toggled.connect(self.toggle_sidebar)
        
        # Sync sidebar buttons
        self.home_btn.toggled.connect(lambda checked: self.home_btn2.setChecked(checked) if checked else None)
        self.developers_btn.toggled.connect(lambda checked: self.developers_btn2.setChecked(checked) if checked else None)
        self.contact_btn.toggled.connect(lambda checked: self.contact_btn2.setChecked(checked) if checked else None)
        self.support_btn.toggled.connect(lambda checked: self.support_btn2.setChecked(checked) if checked else None)
        self.abtus_btn.toggled.connect(lambda checked: self.abtus_btn2.setChecked(checked) if checked else None)
        
        self.home_btn2.toggled.connect(lambda checked: self.home_btn.setChecked(checked) if checked else None)
        self.developers_btn2.toggled.connect(lambda checked: self.developers_btn.setChecked(checked) if checked else None)
        self.contact_btn2.toggled.connect(lambda checked: self.contact_btn.setChecked(checked) if checked else None)
        self.support_btn2.toggled.connect(lambda checked: self.support_btn.setChecked(checked) if checked else None)
        self.abtus_btn2.toggled.connect(lambda checked: self.abtus_btn.setChecked(checked) if checked else None)
        
        # --- Connect page navigation ---
        # Home buttons -> Home Page (index 0)
        self.home_btn.toggled.connect(lambda checked: self.stackedWidget.setCurrentIndex(0) if checked else None)
        self.home_btn2.toggled.connect(lambda checked: self.stackedWidget.setCurrentIndex(0) if checked else None)
        
        # Developers buttons -> Developers Page (index 1)
        self.developers_btn.toggled.connect(lambda checked: self.stackedWidget.setCurrentIndex(1) if checked else None)
        self.developers_btn2.toggled.connect(lambda checked: self.stackedWidget.setCurrentIndex(1) if checked else None)
        
        # Contact buttons -> Contact Page (index 2)
        self.contact_btn.toggled.connect(lambda checked: self.stackedWidget.setCurrentIndex(2) if checked else None)
        self.contact_btn2.toggled.connect(lambda checked: self.stackedWidget.setCurrentIndex(2) if checked else None)
        
        # Support buttons -> Support Page (index 3)
        self.support_btn.toggled.connect(lambda checked: self.stackedWidget.setCurrentIndex(3) if checked else None)
        self.support_btn2.toggled.connect(lambda checked: self.stackedWidget.setCurrentIndex(3) if checked else None)
        
        # Abt us buttons -> About Us Page (index 4)
        self.abtus_btn.toggled.connect(lambda checked: self.stackedWidget.setCurrentIndex(4) if checked else None)
        self.abtus_btn2.toggled.connect(lambda checked: self.stackedWidget.setCurrentIndex(4) if checked else None)
        
        # Exit buttons -> Exit Page (index 5)
        self.exit_btn.toggled.connect(lambda checked: self.stackedWidget.setCurrentIndex(5) if checked else None)
        self.exit_btn2.toggled.connect(lambda checked: self.stackedWidget.setCurrentIndex(5) if checked else None)
        
        # Set initial button state
        self.home_btn.setChecked(True)
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
    def toggle_sidebar(self, checked):
        """Toggle between icon-only and full sidebar"""
        if checked:
            # Show icon-only sidebar
            self.sidebar_stacked_layout.setCurrentIndex(0)
            self.sidebar_container.setMaximumWidth(70)
        else:
            # Show full sidebar
            self.sidebar_stacked_layout.setCurrentIndex(1)
            self.sidebar_container.setMaximumWidth(190)


import src_icons_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # Load QSS file
    with open("style.qss", "r") as file:
        qss = file.read()
        app.setStyleSheet(qss)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
