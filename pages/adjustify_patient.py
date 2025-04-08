from PyQt5 import QtWidgets, QtCore, QtGui
import oracledb

class AdjustPatientDialog(QtWidgets.QDialog):
    def __init__(self, patient_id, patient_name, parent=None):
        super().__init__(parent)
        self.patient_id = patient_id
        self.patient_name = patient_name
        self.setWindowTitle(f"Adjustify Patient - {patient_name}")
        self.setFixedSize(600, 700)
        self.setup_ui()
        
    def setup_ui(self):
        # Main layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Title
        title_label = QtWidgets.QLabel(f"Adjusting Patient: {self.patient_name} (ID: {self.patient_id})")
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
        """)
        main_layout.addWidget(title_label)
        
        # Form layout for patient details
        form_layout = QtWidgets.QFormLayout()
        form_layout.setVerticalSpacing(15)
        form_layout.setHorizontalSpacing(20)
        
        # Current details section
        current_label = QtWidgets.QLabel("Current Details")
        current_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #3498db;")
        main_layout.addWidget(current_label)
        
        # Load current patient data
        self.current_data = self.load_patient_data()
        
        # Display current details (read-only)
        self.current_details = QtWidgets.QTextEdit()
        self.current_details.setReadOnly(True)
        self.current_details.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        self.current_details.setHtml(self.format_current_data())
        main_layout.addWidget(self.current_details)
        
        # Adjustments section
        adjust_label = QtWidgets.QLabel("Adjustments")
        adjust_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #e67e22;")
        main_layout.addWidget(adjust_label)
        
        # Adjustment fields
        self.status_combo = QtWidgets.QComboBox()
        self.status_combo.addItems(["Active", "Discharged", "Transferred", "Deceased"])
        
        self.notes_edit = QtWidgets.QTextEdit()
        self.notes_edit.setPlaceholderText("Enter adjustment notes...")
        self.notes_edit.setMaximumHeight(100)
        
        self.symptoms_edit = QtWidgets.QTextEdit()
        self.symptoms_edit.setPlaceholderText("Enter updated symptoms...")
        self.symptoms_edit.setMaximumHeight(100)
        
        form_layout.addRow("New Status:", self.status_combo)
        form_layout.addRow("Additional Notes:", self.notes_edit)
        form_layout.addRow("Symptoms Update:", self.symptoms_edit)
        
        main_layout.addLayout(form_layout)
        
        # Save Changes button
        self.save_button = QtWidgets.QPushButton("Save Changes")
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
            QPushButton:pressed {
                background-color: #d35400;
            }
        """)
        self.save_button.clicked.connect(self.save_changes)
        main_layout.addWidget(self.save_button, alignment=QtCore.Qt.AlignCenter)
        
        # Button box
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        
        # Style the buttons
        button_box.setStyleSheet("""
            QPushButton {
                min-width: 100px;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:first-child {
                background-color: #2ecc71;
                color: white;
            }
            QPushButton:first-child:hover {
                background-color: #27ae60;
            }
            QPushButton:last-child {
                background-color: #e74c3c;
                color: white;
            }
            QPushButton:last-child:hover {
                background-color: #c0392b;
            }
        """)
        
        main_layout.addWidget(button_box)
        self.setLayout(main_layout)
        
        # Load initial values
        self.load_initial_values()
    
    def load_patient_data(self):
        """Load current patient data from database."""
        connection = None
        cursor = None
        try:
            connection = oracledb.connect(
                user="system", 
                password="Abdo2004@", 
                dsn="localhost:1521/FREE"
            )
            cursor = connection.cursor()
            
            query = """
            SELECT 
                p.patient_id, p.name, p.status, p.notes,
                TO_CHAR(p.birth_date, 'YYYY-MM-DD') AS birth_date,
                TO_CHAR(p.admission_date, 'YYYY-MM-DD') AS admission_date,
                LISTAGG(d.disease_name, ', ') WITHIN GROUP (ORDER BY d.disease_name) AS diseases,
                LISTAGG(s.symptom_name || ' (' || s.severity || ')', ', ') WITHIN GROUP (ORDER BY s.symptom_name) AS symptoms
            FROM 
                patient p
            LEFT JOIN disease d ON p.patient_id = d.patient_id
            LEFT JOIN symptoms s ON p.patient_id = s.patient_id
            WHERE 
                p.patient_id = :id
            GROUP BY 
                p.patient_id, p.name, p.status, p.notes, p.birth_date, p.admission_date
            """
            
            cursor.execute(query, id=self.patient_id)
            return cursor.fetchone()
            
        except Exception as e:
            print(f"Error loading patient data: {e}")
            QtWidgets.QMessageBox.critical(
                self,
                "Database Error",
                f"Could not load patient data:\n{str(e)}"
            )
            return None
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
    
    def format_current_data(self):
        """Format current patient data for display."""
        if not self.current_data:
            return "<i>No patient data available</i>"
        
        html = f"""
        <table width="100%" cellpadding="5">
            <tr>
                <td width="30%"><b>Patient ID:</b></td>
                <td>{self.current_data[0]}</td>
            </tr>
            <tr>
                <td><b>Name:</b></td>
                <td>{self.current_data[1]}</td>
            </tr>
            <tr>
                <td><b>Status:</b></td>
                <td>{self.current_data[2]}</td>
            </tr>
            <tr>
                <td><b>Birth Date:</b></td>
                <td>{self.current_data[4]}</td>
            </tr>
            <tr>
                <td><b>Admission Date:</b></td>
                <td>{self.current_data[5]}</td>
            </tr>
            <tr>
                <td><b>Current Notes:</b></td>
                <td>{self.current_data[3] or 'No notes'}</td>
            </tr>
            <tr>
                <td><b>Diseases:</b></td>
                <td>{self.current_data[6] or 'No diseases recorded'}</td>
            </tr>
            <tr>
                <td><b>Symptoms:</b></td>
                <td>{self.current_data[7] or 'No symptoms recorded'}</td>
            </tr>
        </table>
        """
        return html
    
    def load_initial_values(self):
        """Load current values into form fields."""
        if self.current_data:
            current_status = self.current_data[2]
            index = self.status_combo.findText(current_status)
            if index >= 0:
                self.status_combo.setCurrentIndex(index)
            
            # You could also pre-fill other fields if needed
            # self.notes_edit.setPlainText(self.current_data[3] or "")
    
    def get_adjustments(self):
        """Return the adjustment data entered by the user."""
        return {
            'patient_id': self.patient_id,
            'new_status': self.status_combo.currentText(),
            'additional_notes': self.notes_edit.toPlainText(),
            'symptoms_update': self.symptoms_edit.toPlainText()
        }
    
    def save_changes(self):
        """Save changes to the database."""
        adjustments = self.get_adjustments()
        
        connection = None
        cursor = None
        try:
            connection = oracledb.connect(
                user="system", 
                password="Abdo2004@", 
                dsn="localhost:1521/FREE"
            )
            cursor = connection.cursor()
            
            # Start transaction
            connection.begin()
            
            # Update patient status and append notes if provided
            new_notes = self.current_data[3] or ""
            if adjustments['additional_notes']:
                if new_notes:
                    new_notes += "\n\n"
                new_notes += f"[{QtCore.QDateTime.currentDateTime().toString('yyyy-MM-dd hh:mm')}] {adjustments['additional_notes']}"
            
            # Update patient record
            update_query = """
            UPDATE patient
            SET status = :status, 
                notes = :notes
            WHERE patient_id = :patient_id
            """
            
            cursor.execute(
                update_query, 
                status=adjustments['new_status'],
                notes=new_notes,
                patient_id=adjustments['patient_id']
            )
            
            # Process symptoms update if provided
            if adjustments['symptoms_update'].strip():
                # Parse symptoms from input (assuming format: symptom name, severity)
                # This is a simple implementation; you might want to improve it based on your needs
                symptom_lines = adjustments['symptoms_update'].strip().split('\n')
                
                for line in symptom_lines:
                    if ':' in line:
                        symptom_name, severity = line.split(':', 1)
                        symptom_name = symptom_name.strip()
                        severity = severity.strip()
                        
                        # Check if symptom already exists for this patient
                        check_query = """
                        SELECT COUNT(*) FROM symptoms 
                        WHERE patient_id = :patient_id AND symptom_name = :symptom_name
                        """
                        cursor.execute(check_query, patient_id=adjustments['patient_id'], symptom_name=symptom_name)
                        count = cursor.fetchone()[0]
                        
                        if count > 0:
                            # Update existing symptom
                            symptom_update = """
                            UPDATE symptoms
                            SET severity = :severity
                            WHERE patient_id = :patient_id AND symptom_name = :symptom_name
                            """
                            cursor.execute(
                                symptom_update,
                                severity=severity,
                                patient_id=adjustments['patient_id'],
                                symptom_name=symptom_name
                            )
                        else:
                            # Insert new symptom
                            symptom_insert = """
                            INSERT INTO symptoms (patient_id, symptom_name, severity)
                            VALUES (:patient_id, :symptom_name, :severity)
                            """
                            cursor.execute(
                                symptom_insert,
                                patient_id=adjustments['patient_id'],
                                symptom_name=symptom_name,
                                severity=severity
                            )
            
            # Commit the transaction
            connection.commit()
            
            QtWidgets.QMessageBox.information(
                self,
                "Success",
                "Patient data has been successfully updated."
            )
            
            # Refresh the displayed data
            self.current_data = self.load_patient_data()
            self.current_details.setHtml(self.format_current_data())
            
        except Exception as e:
            # Rollback in case of error
            if connection:
                connection.rollback()
            
            print(f"Error saving changes: {e}")
            QtWidgets.QMessageBox.critical(
                self,
                "Database Error",
                f"Could not save changes:\n{str(e)}"
            )
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()