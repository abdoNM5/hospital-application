from PyQt5 import QtWidgets, QtCore, QtGui
import oracledb
import os
import sys

class PatientDetailsFrame(QtWidgets.QFrame):
    """Frame for displaying detailed patient information with stylish design."""
    def __init__(self, patient_data=None, parent=None):
        super().__init__(parent)
        self.patient_data = patient_data
        self.setup_ui()
        
    def setup_ui(self):
        # Set frame properties
        self.setMinimumSize(700, 500)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.9); 
                border-radius: 15px;
                border: 2px solid #3498db;
            }
            QLabel {
                color: #2c3e50;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel#titleLabel {
                color: #2980b9;
                font-size: 24px;
                font-weight: bold;
            }
            QLabel#infoLabel {
                font-size: 18px;
                margin: 10px;
                padding: 5px;
            }
            QLabel#symptomLabel {
                font-size: 16px;
                color: #e74c3c;
                font-weight: bold;
            }
        """)
        
        # *** BACKGROUND IMAGE LOCATION - START ***
        # Set background image from resources folder
        bg_image_path = r"resources\appbg.png"
        if os.path.exists(bg_image_path):
            palette = self.palette()
            pixmap = QtGui.QPixmap(bg_image_path)
            brush = QtGui.QBrush(pixmap)
            palette.setBrush(QtGui.QPalette.Window, brush)
            self.setPalette(palette)
            self.setAutoFillBackground(True)
        else:
            # Fallback to gradient if image not found
            palette = self.palette()
            gradient = QtGui.QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0.0, QtGui.QColor(224, 242, 255))
            gradient.setColorAt(1.0, QtGui.QColor(172, 220, 255))
            palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(gradient))
            self.setPalette(palette)
            self.setAutoFillBackground(True)
        # *** BACKGROUND IMAGE LOCATION - END ***
        
        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Title
        title_label = QtWidgets.QLabel("Patient Information")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Line separator
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setStyleSheet("background-color: #3498db;")
        line.setFixedHeight(2)
        main_layout.addWidget(line)
        
        # Create scrollable area for the information
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        scroll_area.setStyleSheet("background: transparent;")
        
        scroll_content = QtWidgets.QWidget()
        scroll_layout = QtWidgets.QVBoxLayout(scroll_content)
        
        # Patient information grid
        info_grid = QtWidgets.QGridLayout()
        info_grid.setSpacing(15)
        info_grid.setColumnStretch(0, 1)  # Field name column
        info_grid.setColumnStretch(1, 3)  # Value column - give it more space
        
        # Information labels
        if self.patient_data:
            # Create label pairs (field name : value)
            fields = [
                ("Patient ID:", str(self.patient_data[0])),
                ("Full Name:", self.patient_data[1]),
                ("Birth Date:", self.patient_data[2]),
                ("Status:", self.patient_data[3]),
                ("Admission Date:", self.patient_data[4])
            ]
            
            for row, (field_name, value) in enumerate(fields):
                # Field name
                field_label = QtWidgets.QLabel(field_name)
                field_label.setObjectName("infoLabel")
                field_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                field_label.setStyleSheet("font-weight: bold;")
                
                # Field value
                value_label = QtWidgets.QLabel(value)
                value_label.setObjectName("infoLabel")
                value_label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                value_label.setWordWrap(True)
                
                # Add to grid
                info_grid.addWidget(field_label, row, 0)
                info_grid.addWidget(value_label, row, 1)
            
            # Notes section (special handling for possibly longer text)
            notes_title = QtWidgets.QLabel("Notes:")
            notes_title.setObjectName("symptomLabel")
            notes_title.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
            
            notes_value = QtWidgets.QTextEdit()
            notes_value.setReadOnly(True)
            notes_value.setText(self.patient_data[5] if len(self.patient_data) > 5 else "No notes available")
            notes_value.setStyleSheet("""
                QTextEdit {
                    background-color: transparent;
                    border: none;
                    font-size: 16px;
                    color: #2c3e50;
                    font-family: 'Segoe UI', Arial, sans-serif;
                }
            """)
            notes_value.setMinimumHeight(100)
            
            info_grid.addWidget(notes_title, len(fields), 0)
            info_grid.addWidget(notes_value, len(fields), 1)
            
            # Display disease and symptoms information
            disease_title = QtWidgets.QLabel("Disease:")
            disease_title.setObjectName("symptomLabel")
            disease_title.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
            
            disease_value = QtWidgets.QTextEdit()
            disease_value.setReadOnly(True)
            disease_value.setText(self.patient_data[6] if len(self.patient_data) > 6 else "No disease information available")
            disease_value.setStyleSheet("""
                QTextEdit {
                    background-color: transparent;
                    border: none;
                    font-size: 16px;
                    color: #2c3e50;
                    font-family: 'Segoe UI', Arial, sans-serif;
                }
            """)
            disease_value.setMinimumHeight(80)
            
            info_grid.addWidget(disease_title, len(fields) + 1, 0)
            info_grid.addWidget(disease_value, len(fields) + 1, 1)
            
            # Symptoms section
            symptoms_title = QtWidgets.QLabel("Symptoms:")
            symptoms_title.setObjectName("symptomLabel")
            symptoms_title.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)
            
            symptoms_value = QtWidgets.QTextEdit()
            symptoms_value.setReadOnly(True)
            symptoms_value.setText(self.patient_data[7] if len(self.patient_data) > 7 else "No symptoms recorded")
            symptoms_value.setStyleSheet("""
                QTextEdit {
                    background-color: transparent;
                    border: none;
                    font-size: 16px;
                    color: #2c3e50;
                    font-family: 'Segoe UI', Arial, sans-serif;
                }
            """)
            symptoms_value.setMinimumHeight(100)
            
            info_grid.addWidget(symptoms_title, len(fields) + 2, 0)
            info_grid.addWidget(symptoms_value, len(fields) + 2, 1)
        
        info_frame = QtWidgets.QFrame()
        info_frame.setLayout(info_grid)
        info_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        scroll_layout.addWidget(info_frame)
        scroll_area.setWidget(scroll_content)
        
        main_layout.addWidget(scroll_area)
        
        # Back button
        self.back_button = QtWidgets.QPushButton("Back to Patient List")
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 16px;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.back_button.setFixedHeight(40)
        
        main_layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignCenter)


class PatientNotFoundFrame(QtWidgets.QFrame):
    """Frame displayed when no patient is found with the searched name."""
    def __init__(self, searched_name="", parent=None):
        super().__init__(parent)
        self.searched_name = searched_name
        self.setup_ui()
        
    def setup_ui(self):
        # Set frame properties
        self.setMinimumSize(500, 300)
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
                border: 2px solid #e74c3c;
            }
            QLabel#titleLabel {
                color: #e74c3c;
                font-size: 22px;
                font-weight: bold;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel#messageLabel {
                color: #2c3e50;
                font-size: 16px;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        
        # Background setup (using a gradient since we can't load external images)
        palette = self.palette()
        gradient = QtGui.QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QtGui.QColor(255, 240, 240))
        gradient.setColorAt(1.0, QtGui.QColor(255, 220, 220))
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)
        
        # Not found icon (using text as placeholder since we can't load external images)
        icon_label = QtWidgets.QLabel("🔍❌")
        icon_label.setAlignment(QtCore.Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 48px;")
        main_layout.addWidget(icon_label)
        
        # Title
        title_label = QtWidgets.QLabel("Patient Not Found")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(QtCore.Qt.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Message with better formatting
        message_container = QtWidgets.QWidget()
        message_layout = QtWidgets.QVBoxLayout(message_container)
        message_layout.setContentsMargins(20, 10, 20, 10)
        
        message_label = QtWidgets.QLabel(f"No patient found with the name:")
        message_label.setObjectName("messageLabel")
        message_label.setAlignment(QtCore.Qt.AlignCenter)
        
        # Display the search term more prominently
        search_term = QtWidgets.QLabel(f"'{self.searched_name}'")
        search_term.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #e74c3c;
            margin: 10px;
        """)
        search_term.setAlignment(QtCore.Qt.AlignCenter)
        search_term.setWordWrap(True)
        
        message_layout.addWidget(message_label)
        message_layout.addWidget(search_term)
        
        main_layout.addWidget(message_container)
        
        # Back button
        self.back_button = QtWidgets.QPushButton("Back to Patient List")
        self.back_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                font-size: 16px;
                border-radius: 8px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.back_button.setFixedHeight(40)
        
        main_layout.addWidget(self.back_button, alignment=QtCore.Qt.AlignCenter)


class SearchDialog(QtWidgets.QDialog):
    """Dialog for searching patients by name."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Search Patient")
        self.setFixedSize(450, 220)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f7ff;
                border: 1px solid #3498db;
                border-radius: 10px;
            }
            QLabel {
                font-size: 15px;
                color: #2c3e50;
                font-weight: bold;
            }
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 10px;
                font-size: 15px;
                background-color: white;
                min-height: 20px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
            QPushButton {
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 15px;
                font-weight: bold;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)
        
        # Title with icon
        title_layout = QtWidgets.QHBoxLayout()
        icon_label = QtWidgets.QLabel("🔍")
        icon_label.setStyleSheet("font-size: 24px;")
        title_label = QtWidgets.QLabel("Patient Search")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2980b9;")
        
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        layout.addLayout(title_layout)
        
        # Separator line
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setStyleSheet("background-color: #3498db;")
        layout.addWidget(line)
        
        # Search instruction
        search_label = QtWidgets.QLabel("Enter patient's full name:")
        layout.addWidget(search_label)
        
        # Search input with icon - improved
        input_layout = QtWidgets.QHBoxLayout()
        input_layout.setSpacing(10)
        
        search_icon = QtWidgets.QLabel()
        search_icon.setPixmap(self.style().standardIcon(QtWidgets.QStyle.SP_FileDialogContentsView).pixmap(24, 24))
        search_icon.setFixedWidth(24)
        
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("e.g. John Smith")
        self.search_input.setMinimumHeight(35)
        
        input_layout.addWidget(search_icon)
        input_layout.addWidget(self.search_input)
        layout.addLayout(input_layout)
        
        # Add some space
        layout.addSpacing(5)
        
        # Buttons in a nice layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.cancel_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogCancelButton))
        self.cancel_button.clicked.connect(self.reject)
        
        self.search_button = QtWidgets.QPushButton("Search")
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                min-height: 35px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.search_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_FileDialogContentsView))
        self.search_button.clicked.connect(self.accept)
        self.search_button.setDefault(True)
        
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.search_button)
        
        layout.addLayout(button_layout)
        
        # Set focus to the search input
        self.search_input.setFocus()
        
        # Add shadow effect to the dialog
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QtGui.QColor(0, 0, 0, 60))
        shadow.setOffset(2, 2)
        self.setGraphicsEffect(shadow)
    
    def get_search_text(self):
        return self.search_input.text().strip()


class PatientWidget(QtWidgets.QWidget):
    def __init__(self, worker_id=None, full_name=None, role=None, main_window=None, parent=None):
        super().__init__(parent)
        self.worker_id = worker_id
        self.full_name = full_name
        self.role = role
        self.main_window = main_window
        self.current_frame = None
        
        # Initialize UI components
        self.setup_ui()
        
        # Load data from database
        self.load_data_from_db()
        
        # Connect button signals
        self.connect_signals()
    
    def setup_ui(self):
        # Main vertical layout for the widget
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(10)
        
        # Content stacked widget to switch between views
        self.content_stack = QtWidgets.QStackedWidget()
        
        # Create main content widget
        self.main_content = QtWidgets.QWidget()
        main_content_layout = QtWidgets.QVBoxLayout(self.main_content)
        main_content_layout.setContentsMargins(0, 0, 0, 0)
        main_content_layout.setSpacing(10)
        
        # Horizontal layout for the two buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(20)
        
        # "Add Patient" button (big button on the left)
        self.add_button = QtWidgets.QPushButton("Add Patient")
        self.add_button.setFixedHeight(50)
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 18px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        button_layout.addWidget(self.add_button, stretch=1)
        
        # Search bar and button layout
        search_layout = QtWidgets.QHBoxLayout()
        search_layout.setSpacing(10)
        
        # "Search Patient" button on the right
        self.search_button = QtWidgets.QPushButton("Search Patient")
        self.search_button.setFixedHeight(50)
        self.search_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_FileDialogContentsView))
        self.search_button.setIconSize(QtCore.QSize(24, 24))
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D4;
                color: white;
                font-size: 18px;
                border-radius: 10px;
                padding-left: 15px; 
                padding-right: 15px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """)
        
        button_layout.addWidget(self.search_button, stretch=1)
        self.adjustify_button = QtWidgets.QPushButton("Adjustify Patient")
        self.adjustify_button.setFixedHeight(50)
        self.adjustify_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_FileDialogDetailedView))
        self.adjustify_button.setIconSize(QtCore.QSize(24, 24))
        self.adjustify_button.setStyleSheet("""
        QPushButton {
            background-color: #FFA500;
            color: white;
            font-size: 18px;
            border-radius: 10px;
            padding-left: 15px;
            padding-right: 15px;
        }
        QPushButton:hover {
            background-color: #CC8400;
        }
        QPushButton:disabled {
            background-color: #CCCCCC;
            color: #666666;
        }
    """)
        button_layout.addWidget(self.adjustify_button, stretch=1)
        main_content_layout.addLayout(button_layout)
        
        # Table to display patient data
        self.patient_table = QtWidgets.QTableWidget()
        self.patient_table.setColumnCount(6)  # Updated column count
        self.patient_table.setHorizontalHeaderLabels([
            "Patient ID", "Patient Name", "Birth Date", "Status", 
            "Admission Date", "Notes"
        ])
        self.patient_table.horizontalHeader().setStretchLastSection(True)
        self.patient_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.patient_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.patient_table.setStyleSheet("""
            QTableWidget {
                font-size: 14px;
                border: 1px solid #dcdcdc;
                gridline-color: #e0e0e0;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 6px;
                font-weight: bold;
                border: 1px solid #dcdcdc;
            }
            QTableWidget::item:selected {
                background-color: #cce8ff;
            }
        """)

        # Adjust column widths
        self.patient_table.setColumnWidth(0, 80)      # Patient ID
        self.patient_table.setColumnWidth(1, 150)     # Patient Name
        self.patient_table.setColumnWidth(2, 100)     # Birth Date
        self.patient_table.setColumnWidth(3, 100)     # Status
        self.patient_table.setColumnWidth(4, 120)     # Admission Date
        # Notes column will stretch to fill remaining space
        self.patient_table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        main_content_layout.addWidget(self.patient_table, stretch=1)
        
        # Add main content to stack
        self.content_stack.addWidget(self.main_content)
        self.main_layout.addWidget(self.content_stack)
    
    def connect_signals(self):
        """Connect UI element signals to slots."""
        self.search_button.clicked.connect(self.show_search_dialog)
        self.add_button.clicked.connect(self.show_add_patient)
        self.adjustify_button.clicked.connect(self.adjustify_patient)
        self.patient_table.doubleClicked.connect(self.show_patient_details)
    
    def show_patient_details(self, index):
        """Show detailed information for the selected patient."""
        row = index.row()
        patient_id = int(self.patient_table.item(row, 0).text())
        self.fetch_and_display_patient_detail(patient_id)
        
    def fetch_and_display_patient_detail(self, patient_id):
        """Fetch detailed patient information and display it."""
        connection = None
        cursor = None
        try:
            # Connect to database
            connection = oracledb.connect(
                user="system", 
                password="Abdo2004@", 
                dsn="localhost:1521/FREE"
            )
            cursor = connection.cursor()

            # Query to find patient by ID with all related information
            query = """
            SELECT 
                p.patient_id, 
                p.name, 
                TO_CHAR(p.birth_date, 'YYYY-MM-DD') AS birth_date,
                p.status,
                TO_CHAR(p.admission_date, 'YYYY-MM-DD') AS admission_date,
                p.notes,
                LISTAGG(d.disease_name, ', ') WITHIN GROUP (ORDER BY d.disease_name) AS diseases,
                (SELECT LISTAGG(s.symptom_name || ' (' || s.severity || ')', ', ') 
                 WITHIN GROUP (ORDER BY s.symptom_name)
                 FROM symptoms s 
                 WHERE s.patient_id = p.patient_id) AS symptoms
            FROM 
                patient p
            LEFT JOIN 
                disease d ON p.patient_id = d.patient_id
            WHERE 
                p.patient_id = :id
            GROUP BY 
                p.patient_id, p.name, p.birth_date, p.status, p.admission_date, p.notes
            """

            cursor.execute(query, id=patient_id)
            result = cursor.fetchone()
            
            # Remove current detail frame if it exists
            if self.current_frame is not None:
                self.content_stack.removeWidget(self.current_frame)
                self.current_frame.deleteLater()
                self.current_frame = None
            
            if result:
                # Patient found - show details
                self.current_frame = PatientDetailsFrame(result, self)
                self.current_frame.back_button.clicked.connect(self.return_to_main_view)
                self.content_stack.addWidget(self.current_frame)
                self.content_stack.setCurrentWidget(self.current_frame)
            else:
                # Patient not found - show error
                QtWidgets.QMessageBox.warning(self, "Error", f"Patient with ID {patient_id} not found.")

        except Exception as e:
            print(f"Error fetching patient details: {e}")
            QtWidgets.QMessageBox.critical(self, "Database Error", f"Error retrieving patient details: {str(e)}")
        finally:
            if cursor:
                try:
                    cursor.close()
                except Exception:
                    pass
            if connection:
                try:
                    connection.close()
                except Exception:
                    pass
    
    def show_search_dialog(self):
        """Show search dialog and process the search query."""
        dialog = SearchDialog(self)
        result = dialog.exec_()
        
        if result == QtWidgets.QDialog.Accepted:
            search_text = dialog.get_search_text()
            if search_text:
                self.search_patient(search_text)
    
    def search_patient(self, patient_name):
        """Search for patient by name and display results."""
        connection = None
        cursor = None
        try:
            # Connect to database
            connection = oracledb.connect(
                user="system", 
                password="Abdo2004@", 
                dsn="localhost:1521/FREE"
            )
            cursor = connection.cursor()

            # Query to find patient by name
            query = """
            SELECT 
                p.patient_id, 
                p.name, 
                TO_CHAR(p.birth_date, 'YYYY-MM-DD') AS birth_date,
                p.status,
                TO_CHAR(p.admission_date, 'YYYY-MM-DD') AS admission_date,
                p.notes,
                LISTAGG(d.disease_name, ', ') WITHIN GROUP (ORDER BY d.disease_name) AS diseases,
                (SELECT LISTAGG(s.symptom_name || ' (' || s.severity || ')', ', ') 
                 WITHIN GROUP (ORDER BY s.symptom_name)
                 FROM symptoms s 
                 WHERE s.patient_id = p.patient_id) AS symptoms
            FROM 
                patient p
            LEFT JOIN 
                disease d ON p.patient_id = d.patient_id
            WHERE 
                UPPER(p.name) = UPPER(:name)
            GROUP BY 
                p.patient_id, p.name, p.birth_date, p.status, p.admission_date, p.notes
            """

            cursor.execute(query, name=patient_name)
            result = cursor.fetchone()
            
            # Remove current detail frame if it exists
            if self.current_frame is not None:
                self.content_stack.removeWidget(self.current_frame)
                self.current_frame.deleteLater()
                self.current_frame = None
            
            if result:
                # Patient found - show details
                self.current_frame = PatientDetailsFrame(result, self)
                self.current_frame.back_button.clicked.connect(self.return_to_main_view)
                self.content_stack.addWidget(self.current_frame)
                self.content_stack.setCurrentWidget(self.current_frame)
            else:
                # Patient not found - show error
                self.current_frame = PatientNotFoundFrame(patient_name, self)
                self.current_frame.back_button.clicked.connect(self.return_to_main_view)
                self.content_stack.addWidget(self.current_frame)
                self.content_stack.setCurrentWidget(self.current_frame)

        except Exception as e:
            print(f"Error searching for patient: {e}")
            QtWidgets.QMessageBox.critical(self, "Database Error", f"Error connecting to database: {str(e)}")
        finally:
            if cursor:
                try:
                    cursor.close
                except Exception:
                    pass
            if connection:
                try:
                    connection.close()
                except Exception:
                    pass
    def adjustify_patient(self):
    
     selected_row = self.patient_table.currentRow()
    
     if selected_row == -1:
        QtWidgets.QMessageBox.warning(
            self,
            "No Selection",
            "Please select a patient to adjustify first.",
            QtWidgets.QMessageBox.Ok
        )
        return
    
     patient_id = int(self.patient_table.item(selected_row, 0).text())
     patient_name = self.patient_table.item(selected_row, 1).text()
    
     try:
        from pages.adjustify_patient import AdjustPatientDialog
        dialog = AdjustPatientDialog(patient_id, patient_name, self)
        
        # Set the dialog to be modal and centered
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        dialog.move(
            self.geometry().center() - dialog.rect().center()
        )
        
        result = dialog.exec_()
        
        if result == QtWidgets.QDialog.Accepted:
            self.load_data_from_db()
            QtWidgets.QMessageBox.information(
                self,
                "Success",
                f"Patient {patient_name} has been adjustified!",
                QtWidgets.QMessageBox.Ok
            )
            
     except ImportError as e:
        QtWidgets.QMessageBox.critical(
            self, 
            "Module Error", 
            f"Could not find the Adjust Patient module:\n{str(e)}"
        )
     except Exception as e:
        QtWidgets.QMessageBox.critical(
            self, 
            "Error", 
            f"Could not open Adjust Patient module:\n{str(e)}"
        )
    def save_adjustment(self):
   
     connection = None
     cursor = None
     try:
        # Establish database connection
        connection = oracledb.connect(
            user="system",
            password="Abdo2004@",
            dsn="localhost:1521/FREE"
        )
        cursor = connection.cursor()

        # Start transaction
        connection.begin()

        # 1. Update basic patient information
        update_patient = """
        UPDATE patient
        SET status = :status,
            notes = :notes,
            last_updated = SYSDATE
        WHERE patient_id = :id
        """
        cursor.execute(update_patient, {
            'status': self.status_combo.currentText(),
            'notes': self.notes_edit.toPlainText(),
            'id': self.patient_id
        })

        # 2. Handle diseases (full replacement)
        diseases = [d.strip() for d in self.disease_edit.text().split(',') if d.strip()]
        
        # Delete existing diseases
        cursor.execute("DELETE FROM disease WHERE patient_id = :id", {'id': self.patient_id})
        
        # Insert new diseases
        for disease in diseases:
            cursor.execute(
                "INSERT INTO disease (patient_id, disease_name) VALUES (:id, :disease)",
                {'id': self.patient_id, 'disease': disease}
            )

        # 3. Handle symptoms (full replacement)
        symptoms_text = self.symptoms_edit.toPlainText()
        symptoms = []
        
        # Parse symptoms with severity (format: "Symptom (Severity)")
        for line in symptoms_text.split('\n'):
            line = line.strip()
            if not line:
                continue
            if '(' in line and ')' in line:
                name = line[:line.index('(')].strip()
                severity = line[line.index('(')+1:line.index(')')].strip()
            else:
                name = line
                severity = 'Medium'  # Default severity
            
            symptoms.append((name, severity))
        
        # Delete existing symptoms
        cursor.execute("DELETE FROM symptoms WHERE patient_id = :id", {'id': self.patient_id})
        
        # Insert new symptoms
        for symptom, severity in symptoms:
            cursor.execute(
                """INSERT INTO symptoms (patient_id, symptom_name, severity) 
                VALUES (:id, :symptom, :severity)""",
                {'id': self.patient_id, 'symptom': symptom, 'severity': severity}
            )

        # Commit transaction
        connection.commit()
        
        # Log successful update
        print(f"Successfully updated patient ID {self.patient_id}")
        return True

     except oracledb.DatabaseError as e:
        error, = e.args
        print(f"Oracle Error {error.code}: {error.message}")
        if connection:
            connection.rollback()
        QtWidgets.QMessageBox.critical(
            self,
            "Database Error",
            f"Failed to save adjustments:\nError {error.code}: {error.message}"
        )
        return False

     except Exception as e:
        print(f"Unexpected error saving adjustments: {str(e)}")
        if connection:
            connection.rollback()
        QtWidgets.QMessageBox.critical(
            self,
            "Error",
            f"An unexpected error occurred:\n{str(e)}"
        )
        return False

     finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    def return_to_main_view(self):
        """Return to the main patient list view and refresh data."""
        self.content_stack.setCurrentWidget(self.main_content)
        self.load_data_from_db()  # Refresh data when returning to main view
    
    def load_data_from_db(self):
        """Load patient data from the database with all required fields."""
        connection = None
        cursor = None
        try:
            # Connect to database
            connection = oracledb.connect(
                user="system", 
                password="Abdo2004@", 
                dsn="localhost:1521/FREE"
            )
            cursor = connection.cursor()

            # Updated query to match your table structure
            query = """
            SELECT 
                p.patient_id, 
                p.name, 
                TO_CHAR(p.birth_date, 'YYYY-MM-DD') AS birth_date,
                p.status,
                TO_CHAR(p.admission_date, 'YYYY-MM-DD') AS admission_date,
                p.notes,
                COALESCE(LISTAGG(s.symptom_name, ', ') WITHIN GROUP (ORDER BY s.symptom_name), 'No symptoms') AS symptoms
            FROM 
                patient p
            LEFT JOIN 
                symptoms s ON p.patient_id = s.patient_id
            GROUP BY 
                p.patient_id, p.name, p.birth_date, p.status, p.admission_date, p.notes
            ORDER BY 
                p.patient_id
            """

            cursor.execute(query)
            data = cursor.fetchall()
            
            # Configure table if not already configured
            if self.patient_table.columnCount() == 0:
                self.patient_table.setColumnCount(6)
                self.patient_table.setHorizontalHeaderLabels([
                    "Patient ID", "Patient Name", "Birth Date", 
                    "Status", "Admission Date", "Notes"
                ])
                # Set column widths
                self.patient_table.setColumnWidth(0, 80)   # ID
                self.patient_table.setColumnWidth(1, 200)  # Name
                self.patient_table.setColumnWidth(2, 100)  # Birth Date
                self.patient_table.setColumnWidth(3, 100)  # Status
                self.patient_table.setColumnWidth(4, 120)  # Admission Date
                # Notes column will auto-expand

            self.patient_table.setRowCount(len(data))

            for row_index, row_data in enumerate(data):
                for col_index, value in enumerate(row_data[:6]):  # Only show first 6 columns in table
                    item = QtWidgets.QTableWidgetItem(str(value if value is not None else ""))
                    
                    # Center align all columns except notes
                    if col_index != 5:
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                    else:
                        item.setTextAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
                    
                    self.patient_table.setItem(row_index, col_index, item)

            # Resize rows to fit content
            self.patient_table.resizeRowsToContents()

        except oracledb.DatabaseError as e:
            error, = e.args
            print(f"Oracle Database Error {error.code}: {error.message}")
            QtWidgets.QMessageBox.critical(
                self, 
                "Database Error", 
                f"Could not load patient data:\nError {error.code}: {error.message}"
            )
        except Exception as e:
            print(f"Error loading data from database: {e}")
            QtWidgets.QMessageBox.critical(
                self, 
                "Error", 
                f"An unexpected error occurred:\n{str(e)}"
            )
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def show_add_patient(self):
        """Show the Add Patient dialog and refresh data if a patient was added."""
        try:
            # Import the AddPatient module
            from pages.addpatient import AddPatientDialog
            
            # Create and show the dialog
            dialog = AddPatientDialog(self)
            result = dialog.exec_()
            
            # Refresh table if patient was added
            if result == QtWidgets.QDialog.Accepted:
                self.load_data_from_db()
                QtWidgets.QMessageBox.information(
                    self,
                    "Success",
                    "Patient added successfully!",
                    QtWidgets.QMessageBox.Ok
                )
                
        except ImportError:
            QtWidgets.QMessageBox.critical(
                self, 
                "Module Error", 
                "Could not find the Add Patient module."
            )
        except Exception as e:
            print(f"Error launching Add Patient module: {e}")
            QtWidgets.QMessageBox.critical(
                self, 
                "Error", 
                f"Could not open Add Patient module:\n{str(e)}"
            )


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    # Set application style and font
    app.setStyle("Fusion")
    
    # Create a more sophisticated palette
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(240, 240, 240))
    palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(0, 0, 0))
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 255, 255))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(240, 240, 240))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtGui.QColor(255, 255, 220))
    palette.setColor(QtGui.QPalette.ToolTipText, QtGui.QColor(0, 0, 0))
    palette.setColor(QtGui.QPalette.Text, QtGui.QColor(0, 0, 0))
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(240, 240, 240))
    palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(0, 0, 0))
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(76, 163, 224))
    palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(255, 255, 255))
    app.setPalette(palette)
    
    # Set application font
    font = QtGui.QFont("Segoe UI", 10)
    app.setFont(font)
    
    # Create and show main widget
    widget = PatientWidget()
    widget.resize(1200, 800)  # Slightly larger default size
    widget.setWindowTitle("Hospital Patient Management System")
    
    # Add window icon if available
    try:
        icon_path = "resources/app_icon.png"
        if os.path.exists(icon_path):
            widget.setWindowIcon(QtGui.QIcon(icon_path))
    except Exception as e:
        print(f"Could not load window icon: {e}")
    
    widget.show()
    sys.exit(app.exec_())