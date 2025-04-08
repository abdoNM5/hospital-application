from PyQt5 import QtWidgets, QtCore, QtGui
import sys
import datetime
import requests
import json

class AddPatientDialog(QtWidgets.QDialog):
    """Dialog for adding a new patient to the database."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Patient")
        self.setMinimumSize(600, 650)  # Increased height for additional fields
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        # Set window properties
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f7ff;
                border: 1px solid #3498db;
                border-radius: 10px;
            }
            QLabel {
                font-size: 14px;
                color: #2c3e50;
            }
            QLineEdit, QDateEdit, QTextEdit, QDateTimeEdit, QComboBox {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus, QDateEdit:focus, QTextEdit:focus, QDateTimeEdit:focus, QComboBox:focus {
                border: 2px solid #3498db;
            }
            QPushButton {
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }
            QGroupBox {
                font-weight: bold;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                margin-top: 12px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(15)
        
        # Title with icon
        title_layout = QtWidgets.QHBoxLayout()
        icon_label = QtWidgets.QLabel("👤+")
        icon_label.setStyleSheet("font-size: 24px;")
        title_label = QtWidgets.QLabel("Add New Patient")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2980b9;")
        
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        main_layout.addLayout(title_layout)
        
        # Separator line
        line = QtWidgets.QFrame()
        line.setFrameShape(QtWidgets.QFrame.HLine)
        line.setFrameShadow(QtWidgets.QFrame.Sunken)
        line.setStyleSheet("background-color: #3498db;")
        main_layout.addWidget(line)
        
        # Create a form layout for patient details
        form_layout = QtWidgets.QFormLayout()
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        form_layout.setFormAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        form_layout.setSpacing(15)
        
        # Patient Name field
        name_label = QtWidgets.QLabel("Name:")
        name_label.setStyleSheet("font-weight: bold;")
        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("Enter patient's name")
        form_layout.addRow(name_label, self.name_input)
        
        # Birth Date field
        birth_date_label = QtWidgets.QLabel("Birth Date:")
        birth_date_label.setStyleSheet("font-weight: bold;")
        self.birth_date_input = QtWidgets.QDateEdit(calendarPopup=True)
        self.birth_date_input.setDisplayFormat("yyyy-MM-dd")
        self.birth_date_input.setDate(QtCore.QDate.currentDate().addYears(-30))  # Default to 30 years ago
        self.birth_date_input.setMaximumDate(QtCore.QDate.currentDate())
        form_layout.addRow(birth_date_label, self.birth_date_input)
        
        # Admission Date field
        admission_date_label = QtWidgets.QLabel("Admission Date:")
        admission_date_label.setStyleSheet("font-weight: bold;")
        self.admission_date_input = QtWidgets.QDateEdit(calendarPopup=True)
        self.admission_date_input.setDisplayFormat("yyyy-MM-dd")
        self.admission_date_input.setDate(QtCore.QDate.currentDate())  # Default to today
        form_layout.addRow(admission_date_label, self.admission_date_input)
        
        # Status field
        status_label = QtWidgets.QLabel("Status:")
        status_label.setStyleSheet("font-weight: bold;")
        self.status_input = QtWidgets.QComboBox()
        self.status_input.addItems(['STABLE', 'CRITICAL', 'URGENT', 'GOOD', 'RECOVERING'])
        form_layout.addRow(status_label, self.status_input)
        
        # Notes field
        notes_label = QtWidgets.QLabel("Notes:")
        notes_label.setStyleSheet("font-weight: bold;")
        self.notes_input = QtWidgets.QTextEdit()
        self.notes_input.setPlaceholderText("Enter any notes about the patient")
        self.notes_input.setMaximumHeight(100)
        form_layout.addRow(notes_label, self.notes_input)
        
        # Add form layout to main layout
        main_layout.addLayout(form_layout)
        
        # Disease group box
        disease_group = QtWidgets.QGroupBox("Disease")
        disease_layout = QtWidgets.QVBoxLayout(disease_group)
        
        self.disease_input = QtWidgets.QLineEdit()
        self.disease_input.setPlaceholderText("Enter patient's disease")
        disease_layout.addWidget(self.disease_input)
        
        main_layout.addWidget(disease_group)
        
        # Symptoms group box
        symptoms_group = QtWidgets.QGroupBox("Symptoms")
        symptoms_layout = QtWidgets.QVBoxLayout(symptoms_group)
        
        # Symptoms input layout
        self.symptoms_list = QtWidgets.QListWidget()
        self.symptoms_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                background-color: white;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #ecf0f1;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        
        symptoms_input_layout = QtWidgets.QHBoxLayout()
        self.symptom_input = QtWidgets.QLineEdit()
        self.symptom_input.setPlaceholderText("Enter a symptom")
        
        self.severity_input = QtWidgets.QComboBox()
        self.severity_input.addItems(['Mild', 'Moderate', 'Severe', 'Critical'])
        
        self.add_symptom_btn = QtWidgets.QPushButton("Add")
        self.add_symptom_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        
        self.remove_symptom_btn = QtWidgets.QPushButton("Remove")
        self.remove_symptom_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        
        symptoms_input_layout.addWidget(self.symptom_input)
        symptoms_input_layout.addWidget(self.severity_input)
        symptoms_input_layout.addWidget(self.add_symptom_btn)
        symptoms_input_layout.addWidget(self.remove_symptom_btn)
        
        symptoms_layout.addLayout(symptoms_input_layout)
        symptoms_layout.addWidget(self.symptoms_list)
        
        main_layout.addWidget(symptoms_group)
        
        # Button layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(15)
        
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                min-height: 35px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.cancel_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogCancelButton))
        
        self.save_button = QtWidgets.QPushButton("Save Patient")
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                min-height: 35px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.save_button.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogSaveButton))
        self.save_button.setDefault(True)
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)
        
        main_layout.addLayout(button_layout)
    
    def connect_signals(self):
        """Connect UI element signals to slots."""
        self.cancel_button.clicked.connect(self.reject)
        self.save_button.clicked.connect(self.save_patient)
        self.add_symptom_btn.clicked.connect(self.add_symptom)
        self.remove_symptom_btn.clicked.connect(self.remove_symptom)
        self.symptom_input.returnPressed.connect(self.add_symptom)
    
    def add_symptom(self):
        """Add a symptom with severity to the list."""
        symptom_text = self.symptom_input.text().strip()
        if symptom_text:
            severity = self.severity_input.currentText()
            list_item = QtWidgets.QListWidgetItem(f"{symptom_text} - {severity}")
            # Store both symptom and severity
            list_item.setData(QtCore.Qt.UserRole, (symptom_text, severity))
            self.symptoms_list.addItem(list_item)
            self.symptom_input.clear()
            self.symptom_input.setFocus()
    
    def remove_symptom(self):
        """Remove the selected symptom from the list."""
        selected_items = self.symptoms_list.selectedItems()
        if selected_items:
            for item in selected_items:
                self.symptoms_list.takeItem(self.symptoms_list.row(item))
    
    def save_patient(self):
        # Validate inputs
        if not self.validate_inputs():
            return
        
        # Get values from form
        patient_name = self.name_input.text().strip()
        disease_name = self.disease_input.text().strip()
        birth_date = self.birth_date_input.date().toString("yyyy-MM-dd")
        admission_date = self.admission_date_input.date().toString("yyyy-MM-dd")
        status = self.status_input.currentText()
        notes = self.notes_input.toPlainText().strip()
        
        # Get all symptoms with severity
        symptoms = []
        for i in range(self.symptoms_list.count()):
            item = self.symptoms_list.item(i)
            symptom_data = item.data(QtCore.Qt.UserRole)
            symptoms.append(symptom_data)
        
        try:
            # API endpoint URL - adjust to your server location
            api_url = "http://localhost/patient_api/add_patient.php"
            
            # Prepare payload
            payload = {
                'name': patient_name,
                'disease_name': disease_name,
                'birth_date': birth_date,
                'admission_date': admission_date,
                'status': status,
                'notes': notes,
                'symptoms': symptoms
            }
            
            # Print debug info
            print(f"Sending request to: {api_url}")
            print(f"Payload: {json.dumps(payload, indent=2)}")
            
            # Send POST request to PHP API
            response = requests.post(api_url, json=payload)
            
            # Print response for debugging
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.text}")
            
            # Check response
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    # Show success message
                    QtWidgets.QMessageBox.information(
                        self, "Success", 
                        f"Patient '{patient_name}' has been added successfully!"
                    )
                    # Close the dialog with Accept result
                    self.accept()
                else:
                    # Show error message from API
                    QtWidgets.QMessageBox.critical(
                        self, "API Error", 
                        f"Error: {result.get('message', 'Unknown error')}"
                    )
            else:
                # Show error message for bad response
                QtWidgets.QMessageBox.critical(
                    self, "API Error", 
                    f"Error connecting to API: Status code {response.status_code}\n{response.text}"
                )
                
        except Exception as e:
            print(f"Error saving patient: {e}")
            QtWidgets.QMessageBox.critical(
                self, "Error", 
                f"Error sending data to server: {str(e)}"
            )
    
    def validate_inputs(self):
        """Validate the form inputs."""
        # Check if patient name is provided
        if not self.name_input.text().strip():
            QtWidgets.QMessageBox.warning(
                self, "Input Error", 
                "Please enter the patient's name."
            )
            self.name_input.setFocus()
            return False
        
        # Check if disease is provided
        if not self.disease_input.text().strip():
            QtWidgets.QMessageBox.warning(
                self, "Input Error", 
                "Please enter the patient's disease."
            )
            self.disease_input.setFocus()
            return False
        
        # All validations passed
        return True


# Test code to run this module directly
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = AddPatientDialog()
    dialog.show()
    sys.exit(app.exec_())