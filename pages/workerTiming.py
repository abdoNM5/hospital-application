import sys
import oracledb
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QTableWidget, QTableWidgetItem, QComboBox,
                             QDateEdit, QTabWidget, QFrame, QHeaderView, QScrollArea, QMessageBox)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen
from PyQt5.QtChart import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from datetime import date, timedelta

# Database Configuration
DB_USERNAME = "system"
DB_PASSWORD = "s2004b22"
DB_DSN = "192.168.21.1:1521/FREE"

def connect_db():
    """Establishes a connection to the Oracle database."""
    try:
        connection = oracledb.connect(user=DB_USERNAME, password=DB_PASSWORD, dsn=DB_DSN)
        print("Database connection successful!")
        return connection
    except oracledb.Error as error:
        print(f"Error connecting to Oracle Database: {error}")
        QMessageBox.critical(None, "Database Connection Error",
                           f"Could not connect to the Oracle database.\nError: {error}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        QMessageBox.critical(None, "Connection Error", f"An unexpected error occurred.\nError: {e}")
        return None

class WorkerTimingSpace(QWidget):
    def __init__(self, worker_id=None, full_name=None, role=None, main_window=None, parent=None):
        super().__init__(parent)
        self.db_connection = connect_db()
        # Store user role for permission checks
        self.worker_id = worker_id
        self.worker_name = full_name
        self.worker_role = role
        self.main_window = main_window
        self.init_ui()
        if self.db_connection:
            self.populate_department_combo()
            self.load_initial_data()
    def go_back_to_workspaces(self):
        """Return to the workspaces/home page."""
        from pages.home import MainWindow
        if self.main_window:
            # Find the HomePage widget in the stacked widget
            for index in range(self.main_window.count()):
                widget = self.main_window.widget(index)
                if isinstance(widget, MainWindow):  # This checks for MainWindow class
                    self.main_window.setCurrentWidget(widget)
                    break        

    def load_initial_data(self):
        """Loads data into all views when the app starts or filters change."""
        print("Loading initial data...")
        self.load_schedule_data()
        self.load_performance_data()
        self.load_time_off_data()

    def init_ui(self):
        """Sets up the user interface widgets and layouts."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Header Section
        header_layout = QHBoxLayout()
        title_label = QLabel("Employee Timing Management")
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        # Filter Section
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        self.department_combo = QComboBox()
        self.department_combo.setStyleSheet("padding: 5px; border-radius: 4px; background-color: white; min-width: 150px;")
        self.department_combo.addItem("Loading Departments...")
        
        self.date_label = QLabel("Date Range:")
        self.date_label.setStyleSheet("font-weight: bold;")
        
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-QDate.currentDate().dayOfWeek() + 1))
        self.start_date.setCalendarPopup(True)
        self.start_date.setStyleSheet("padding: 5px; border-radius: 4px; background-color: white;")
        
        self.end_date = QDateEdit()
        self.end_date.setDate(self.start_date.date().addDays(6))
        self.end_date.setCalendarPopup(True)
        self.end_date.setStyleSheet("padding: 5px; border-radius: 4px; background-color: white;")
        
        apply_btn = QPushButton("Apply Filters")
        apply_btn.setStyleSheet("""
            QPushButton { 
                background-color: #4A86E8; 
                color: white; 
                border: none; 
                padding: 8px 16px; 
                border-radius: 4px; 
            } 
            QPushButton:hover { 
                background-color: #3D76C9; 
            }
        """)
        apply_btn.clicked.connect(self.apply_filters)

        filter_layout.addWidget(QLabel("Department:"))
        filter_layout.addWidget(self.department_combo)
        filter_layout.addWidget(self.date_label)
        filter_layout.addWidget(self.start_date)
        filter_layout.addWidget(QLabel("to"))
        filter_layout.addWidget(self.end_date)
        filter_layout.addWidget(apply_btn)
        header_layout.addLayout(filter_layout)

        # Tabbed Views
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #D0D0D0; border-radius: 4px; background-color: white; }
            QTabBar::tab { background-color: #F0F0F0; padding: 8px 16px; border: 1px solid #D0D0D0; border-bottom: none; 
                           border-top-left-radius: 4px; border-top-right-radius: 4px; margin-right: 2px; }
            QTabBar::tab:selected { background-color: white; border-bottom: none; }
            QTabBar::tab:!selected:hover { background-color: #E0E0E0; }
        """)
        
        self.schedule_widget = self.create_schedule_view()
        self.tabs.addTab(self.schedule_widget, "Schedule View")
        
        self.performance_widget = self.create_performance_view()
        self.tabs.addTab(self.performance_widget, "Performance Metrics")
        
        self.time_off_widget = self.create_time_off_view()
        self.tabs.addTab(self.time_off_widget, "Time Off Management")

        # Bottom Action Buttons (now empty since we removed the back button)
        action_layout = QHBoxLayout()
        action_layout.addStretch()  # Just keeps the layout balanced

            # Add Back to Workspaces button here
        back_btn = QPushButton("Back to Workspaces")
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        back_btn.clicked.connect(self.go_back_to_workspaces)
        action_layout.addWidget(back_btn)
        action_layout.addStretch()  # Push the button to the left


        # Assemble Main Layout
        main_layout.addLayout(header_layout)
        main_layout.addWidget(self.tabs)
        main_layout.addLayout(action_layout)

    def apply_filters(self):
        """Reloads data based on the current filter settings."""
        print("Applying filters...")
        if not self.db_connection:
            QMessageBox.warning(self, "No Connection", "Database is not connected. Cannot apply filters.")
            return
        self.load_initial_data()

    def populate_department_combo(self):
        if not self.db_connection: 
            return
        
        cursor = None
        try:
            cursor = self.db_connection.cursor()
            query = "SELECT DISTINCT DEPARTEMENT FROM EMPLOYEES WHERE DEPARTEMENT IS NOT NULL ORDER BY DEPARTEMENT"
            cursor.execute(query)
            departments = cursor.fetchall()
            self.department_combo.clear()
            self.department_combo.addItem("All Departments")
            for dept in departments: 
                self.department_combo.addItem(dept[0])
        except oracledb.Error as error:
            print(f"Error populating departments: {error}")
            QMessageBox.warning(self, "DB Error", f"Could not load departments.\nError: {error}")
            self.department_combo.clear()
            self.department_combo.addItem("Error loading")
        except Exception as e: 
            print(f"Unexpected error populating departments: {e}")
        finally:
            if cursor: 
                cursor.close()

    def create_schedule_view(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        nav_layout = QHBoxLayout()
        # prev_week_btn = QPushButton("← Previous Week")
        # next_week_btn = QPushButton("Next Week →")
        
        self.week_label = QLabel("Week of ...")
        self.week_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        self.update_week_label()
        
        # nav_layout.addWidget(prev_week_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.week_label)
        nav_layout.addStretch()
        # nav_layout.addWidget(next_week_btn)
        
        self.schedule_table = QTableWidget()
        self.schedule_table.setColumnCount(9)
        self.schedule_table.setHorizontalHeaderLabels(["ID", "Employee", "Monday", "Tuesday", "Wednesday", 
                                                     "Thursday", "Friday", "Saturday", "Sunday"])
        self.schedule_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.schedule_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.schedule_table.verticalHeader().setVisible(False)
        self.schedule_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.schedule_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.schedule_table.setStyleSheet("""
            QTableWidget { 
                border: 1px solid #D0D0D0; 
                gridline-color: #E0E0E0; 
            } 
            QHeaderView::section { 
                background-color: #F0F0F0; 
                padding: 5px; 
                border: 1px solid #D0D0D0; 
                font-weight: bold; 
            } 
            QTableWidget::item { 
                padding: 3px; 
            }
        """)
        
        legend_layout = QHBoxLayout()
        legend_label = QLabel("Legend:")
        legend_layout.addWidget(legend_label)
        
        legend_items = [
            ("Morning", QColor(217, 234, 255)),
            ("Afternoon", QColor(255, 252, 214)),
            ("Night", QColor(234, 216, 255)),
            ("Day Off", QColor(240, 240, 240))
        ]
        
        for text, color in legend_items:
            frame = QFrame()
            frame.setFixedSize(18, 18)
            frame.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #B0B0B0; border-radius: 3px;")
            
            label = QLabel(f" {text}")
            item_layout = QHBoxLayout()
            item_layout.setSpacing(5)
            item_layout.addWidget(frame)
            item_layout.addWidget(label)
            
            legend_layout.addLayout(item_layout)
            legend_layout.addSpacing(15)
        
        legend_layout.addStretch()
        
        layout.addLayout(nav_layout)
        layout.addWidget(self.schedule_table)
        layout.addLayout(legend_layout)
        
        return widget

    def create_performance_view(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        stats_layout = QHBoxLayout()
        self.stats_cards = {}
        
        card_data = [
            ("Total Hours Worked", "#4A86E8"),
            ("Overtime Hours", "#E74C3C"),
            ("Avg Punctuality", "#2ECC71"),
            ("Staff Coverage", "#F1C40F")
        ]
        
        for title, color in card_data:
            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)
            card.setStyleSheet(f"""
                QFrame {{ 
                    border: 1px solid {color}; 
                    border-radius: 8px; 
                    background-color: white; 
                    padding: 10px; 
                }}
            """)
            
            card_layout = QVBoxLayout(card)
            title_label = QLabel(title)
            title_label.setStyleSheet("font-size: 14px; color: #555;")
            
            value_label = QLabel("N/A")
            value_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {color};")
            
            card_layout.addWidget(title_label, alignment=Qt.AlignCenter)
            card_layout.addWidget(value_label, alignment=Qt.AlignCenter)
            stats_layout.addWidget(card)
            self.stats_cards[title] = value_label
        
        chart_layout = QHBoxLayout()
        
        self.hours_chart_view = self.create_bar_chart("Hours by Department", [], [])
        self.punctuality_chart_view = self.create_bar_chart("Staff Punctuality (%)", [], [])
        
        chart_layout.addWidget(self.hours_chart_view)
        chart_layout.addWidget(self.punctuality_chart_view)
        
        self.performance_table = QTableWidget()
        self.performance_table.setColumnCount(5)
        self.performance_table.setHorizontalHeaderLabels([
            "Employee", "Hours Worked", "Overtime", "Punctuality", "Perf. Score"
        ])
        self.performance_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.performance_table.verticalHeader().setVisible(False)
        self.performance_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.performance_table.setStyleSheet("""
            QTableWidget { 
                border: 1px solid #D0D0D0; 
                gridline-color: #E0E0E0; 
            } 
            QHeaderView::section { 
                background-color: #F0F0F0; 
                padding: 5px; 
                border: 1px solid #D0D0D0; 
                font-weight: bold; 
            } 
            QTableWidget::item { 
                padding: 3px; 
            }
        """)
        
        layout.addLayout(stats_layout)
        layout.addLayout(chart_layout)
        layout.addWidget(QLabel("Individual Performance Metrics:"))
        layout.addWidget(self.performance_table)
        
        return widget

    def create_time_off_view(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        status_layout = QHBoxLayout()
        self.status_cards = {}
        
        status_data = [
            ("Pending Requests", "#F39C12"),
            ("Approved Time Off", "#2ECC71"),
            ("Denied Requests", "#E74C3C"),
            ("Available Coverage", "#3498DB")
        ]
        
        for title, color in status_data:
            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)
            card.setStyleSheet(f"""
                QFrame {{ 
                    border: 1px solid {color}; 
                    border-radius: 8px; 
                    background-color: white; 
                    padding: 10px; 
                }}
            """)
            
            card_layout = QVBoxLayout(card)
            title_label = QLabel(title)
            title_label.setStyleSheet("font-size: 14px; color: #555;")
            
            value_label = QLabel("N/A")
            value_label.setStyleSheet(f"font-size: 28px; font-weight: bold; color: {color};")
            
            card_layout.addWidget(title_label, alignment=Qt.AlignCenter)
            card_layout.addWidget(value_label, alignment=Qt.AlignCenter)
            status_layout.addWidget(card)
            self.status_cards[title] = value_label
        
        self.time_off_table = QTableWidget()
        self.time_off_table.setColumnCount(7)
        self.time_off_table.setHorizontalHeaderLabels([
            "Employee", "Request Type", "Start Date", "End Date", "Duration", "Status", "Action"
        ])
        self.time_off_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.time_off_table.verticalHeader().setVisible(False)
        self.time_off_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.time_off_table.setStyleSheet("""
            QTableWidget { 
                border: 1px solid #D0D0D0; 
                gridline-color: #E0E0E0; 
            } 
            QHeaderView::section { 
                background-color: #F0F0F0; 
                padding: 5px; 
                border: 1px solid #D0D0D0; 
                font-weight: bold; 
            } 
            QTableWidget::item { 
                padding: 3px; 
            }
        """)
        self.time_off_table.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeToContents)
        
        form_frame = QFrame()
        form_frame.setFrameShape(QFrame.StyledPanel)
        form_frame.setStyleSheet("""
            QFrame { 
                border: 1px solid #D0D0D0; 
                border-radius: 8px; 
                background-color: #F9F9F9; 
                padding: 10px; 
            }
        """)
        
        form_layout = QVBoxLayout(form_frame)
        form_title = QLabel("Submit New Time Off Request")
        form_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        
        form_inputs = QHBoxLayout()
        
        employee_label = QLabel(f"{self.worker_name} (ID: {self.worker_id})")
        employee_label.setStyleSheet("font-weight: bold; padding: 5px; background-color: #f0f0f0; border: 1px solid #ddd; border-radius: 3px;")

        self.req_type_combo = QComboBox()
        self.req_type_combo.addItems(["Select Type", "Vacation", "Sick Leave", "Personal", "Medical", "Other"])
        
        self.req_start_date = QDateEdit()
        self.req_start_date.setDate(QDate.currentDate().addDays(1))
        self.req_start_date.setCalendarPopup(True)
        
        self.req_end_date = QDateEdit()
        self.req_end_date.setDate(QDate.currentDate().addDays(1))
        self.req_end_date.setCalendarPopup(True)
        
        submit_req_btn = QPushButton("Submit Request")
        submit_req_btn.setStyleSheet("""
            QPushButton { 
                background-color: #4A86E8; 
                color: white; 
                border: none; 
                padding: 8px 16px; 
                border-radius: 4px; 
            } 
            QPushButton:hover { 
                background-color: #3D76C9; 
            }
        """)
        submit_req_btn.clicked.connect(self.submit_time_off_request)
        
        form_inputs.addWidget(QLabel("Employee:"))
        form_inputs.addWidget(employee_label, 1)
        form_inputs.addWidget(QLabel("Type:"))
        form_inputs.addWidget(self.req_type_combo, 1)
        form_inputs.addWidget(QLabel("Start:"))
        form_inputs.addWidget(self.req_start_date)
        form_inputs.addWidget(QLabel("End:"))
        form_inputs.addWidget(self.req_end_date)
        form_inputs.addStretch()
        form_inputs.addWidget(submit_req_btn)
        
        form_layout.addWidget(form_title)
        form_layout.addLayout(form_inputs)
        
        layout.addLayout(status_layout)
        layout.addWidget(QLabel("Time Off Requests:"))
        layout.addWidget(self.time_off_table)
        layout.addWidget(form_frame)
        
        return widget

    def load_schedule_data(self):
        if not self.db_connection: 
            print("DB connection lost.")
            self.schedule_table.setRowCount(0)
            return
        
        cursor = None
        try:
            self.schedule_table.setRowCount(0)
            self.update_week_label()
            
            cursor = self.db_connection.cursor()
            selected_dept = self.department_combo.currentText()
            
            query = """
                SELECT 
                    WORKER_ID, 
                    FULL_NAME, 
                    SCHEDULED_DAYS
                FROM EMPLOYEES
                {where_clause}
                ORDER BY FULL_NAME
            """.format(
                where_clause="WHERE DEPARTEMENT = :dept" if selected_dept != "All Departments" else ""
            )
            
            params = {}
            if selected_dept != "All Departments":
                params['dept'] = selected_dept
                
            cursor.execute(query, params)
            employees = cursor.fetchall()
            
            if not employees:
                print("No employees found.")
                return

            self.schedule_table.setRowCount(len(employees))
            
            for row, (worker_id, full_name, scheduled_days) in enumerate(employees):
                self.schedule_table.setItem(row, 0, QTableWidgetItem(str(worker_id)))
                self.schedule_table.setItem(row, 1, QTableWidgetItem(full_name))
                
                # Parse the scheduled_days string (format: "M:8a-4p;T:8a-4p;...")
                schedule_map = {}
                if scheduled_days:
                    for day_schedule in scheduled_days.split(';'):
                        if ':' in day_schedule:
                            day, schedule = day_schedule.split(':')
                            schedule_map[day] = schedule
                
                # Populate each day's schedule
                days = ['M', 'T', 'W', 'Th', 'F', 'Sa', 'Su']
                for col_day_idx, day in enumerate(days, start=2):
                    schedule = schedule_map.get(day, "OFF")
                    item = QTableWidgetItem(schedule)
                    item.setTextAlignment(Qt.AlignCenter)
                    
                    # Color coding based on shift type
                    if "OFF" in schedule:
                        item.setBackground(QColor(240, 240, 240))
                    elif "7a" in schedule or "8a" in schedule:
                        item.setBackground(QColor(217, 234, 255))
                    elif "12p" in schedule:
                        item.setBackground(QColor(255, 252, 214))
                    elif "7p" in schedule:
                        item.setBackground(QColor(234, 216, 255))
                        
                    self.schedule_table.setItem(row, col_day_idx, item)
                    
            print(f"Schedule table populated with {len(employees)} employees.")
            
        except oracledb.Error as error:
            print(f"Oracle Error fetching schedule data: {error}")
            QMessageBox.warning(self, "DB Query Error", 
                              f"Could not fetch schedule data.\nError: {error}")
        except Exception as e:
            print(f"Unexpected error loading schedule data: {e}")
            QMessageBox.critical(self, "Error", f"Error loading schedule: {e}")
        finally:
            if cursor: 
                cursor.close()

    def load_performance_data(self):
        if not self.db_connection:
            print("DB connection lost.")
            return
            
        cursor = None
        try:
            selected_dept = self.department_combo.currentText()
            
            # Query performance data from EMPLOYEES table
            query = """
                SELECT 
                    FULL_NAME,
                    HOURS_WORKED,
                    OVERTIME_HOURS,
                    PUNCTUALITY_SCORE,
                    PERFORMANCE_SCORE
                FROM EMPLOYEES
                {where_clause}
                ORDER BY PERFORMANCE_SCORE DESC
            """.format(
                where_clause="WHERE DEPARTEMENT = :dept" if selected_dept != "All Departments" else ""
            )
            
            params = {}
            if selected_dept != "All Departments":
                params['dept'] = selected_dept
                
            cursor = self.db_connection.cursor()
            cursor.execute(query, params)
            performance_data = cursor.fetchall()
            
            # Update stats cards with aggregated data
            stats_query = """
                SELECT 
                    ROUND(AVG(HOURS_WORKED), 2),
                    ROUND(AVG(OVERTIME_HOURS), 2),
                    ROUND(AVG(PUNCTUALITY_SCORE), 1),
                    COUNT(*) as staff_count
                FROM EMPLOYEES
                {where_clause}
            """.format(
                where_clause="WHERE DEPARTEMENT = :dept" if selected_dept != "All Departments" else ""
            )
            
            cursor.execute(stats_query, params)
            avg_hours, avg_overtime, avg_punctuality, staff_count = cursor.fetchone()
            
            self.stats_cards["Total Hours Worked"].setText(f"{avg_hours}")
            self.stats_cards["Overtime Hours"].setText(f"{avg_overtime}")
            self.stats_cards["Avg Punctuality"].setText(f"{avg_punctuality}%")
            self.stats_cards["Staff Coverage"].setText(f"{staff_count}")
            
            # Update charts with department data
            dept_query = """
                SELECT 
                    DEPARTEMENT,
                    ROUND(AVG(HOURS_WORKED), 2),
                    ROUND(AVG(PUNCTUALITY_SCORE), 1)
                FROM EMPLOYEES
                WHERE DEPARTEMENT IS NOT NULL
                GROUP BY DEPARTEMENT
            """
            
            cursor.execute(dept_query)
            dept_data = cursor.fetchall()
            
            hours_cats = [dept[0] for dept in dept_data]
            hours_vals = [dept[1] for dept in dept_data]
            punct_vals = [dept[2] for dept in dept_data]
            
            hours_qchart = self._generate_qchart("Hours by Department", hours_cats, hours_vals)
            self.hours_chart_view.setChart(hours_qchart)
            
            punct_qchart = self._generate_qchart("Staff Punctuality (%)", hours_cats, punct_vals)
            self.punctuality_chart_view.setChart(punct_qchart)
            
            # Populate performance table
            self.performance_table.setRowCount(len(performance_data))
            for row, (name, hours, overtime, punctuality, perf_score) in enumerate(performance_data):
                self.performance_table.setItem(row, 0, QTableWidgetItem(name))
                self.performance_table.setItem(row, 1, QTableWidgetItem(f"{hours}"))
                self.performance_table.setItem(row, 2, QTableWidgetItem(f"{overtime}"))
                self.performance_table.setItem(row, 3, QTableWidgetItem(f"{punctuality}%"))
                self.performance_table.setItem(row, 4, QTableWidgetItem(f"{perf_score}%"))
                
        except Exception as e:
            print(f"Error loading performance data: {e}")
            QMessageBox.critical(self, "Error", f"Error loading performance data: {e}")
        finally:
            if cursor:
                cursor.close()

    def load_time_off_data(self):
        if not self.db_connection:
            print("DB connection lost.")
            return
            
        cursor = None
        try:
            selected_dept = self.department_combo.currentText()
            
            # Query time off data from EMPLOYEES table
            query = """
                SELECT 
                    e.FULL_NAME,
                    e.TIME_OFF_TYPE,
                    TO_CHAR(e.TIME_OFF_START_DATE, 'YYYY-MM-DD'),
                    TO_CHAR(e.TIME_OFF_END_DATE, 'YYYY-MM-DD'),
                    e.TIME_OFF_DURATION,
                    e.TIME_OFF_STATUS,
                    e.WORKER_ID
                FROM EMPLOYEES e
                WHERE e.TIME_OFF_STATUS IS NOT NULL
                {dept_filter}
                ORDER BY e.TIME_OFF_START_DATE
            """.format(
                dept_filter="AND e.DEPARTEMENT = :dept" if selected_dept != "All Departments" else ""
            )
            
            params = {}
            if selected_dept != "All Departments":
                params['dept'] = selected_dept
                
            cursor = self.db_connection.cursor()
            cursor.execute(query, params)
            time_off_data = cursor.fetchall()
            
            # Update status cards
            status_query = """
                SELECT 
                    SUM(CASE WHEN TIME_OFF_STATUS = 'Pending' THEN 1 ELSE 0 END),
                    SUM(CASE WHEN TIME_OFF_STATUS = 'Approved' THEN 1 ELSE 0 END),
                    SUM(CASE WHEN TIME_OFF_STATUS = 'Denied' THEN 1 ELSE 0 END),
                    COUNT(*) as total_employees
                FROM EMPLOYEES
                {where_clause}
            """.format(
                where_clause="WHERE DEPARTEMENT = :dept" if selected_dept != "All Departments" else ""
            )
            
            cursor.execute(status_query, params)
            pending, approved, denied, total_employees = cursor.fetchone()
            
            self.status_cards["Pending Requests"].setText(f"{pending}")
            self.status_cards["Approved Time Off"].setText(f"{approved}")
            self.status_cards["Denied Requests"].setText(f"{denied}")
            self.status_cards["Available Coverage"].setText(f"{total_employees - approved}")
            
            # Populate time off table
            self.time_off_table.setRowCount(len(time_off_data))
            for row, (name, req_type, start_date, end_date, duration, status, worker_id) in enumerate(time_off_data):
                self.time_off_table.setItem(row, 0, QTableWidgetItem(name))
                self.time_off_table.setItem(row, 1, QTableWidgetItem(req_type))
                self.time_off_table.setItem(row, 2, QTableWidgetItem(start_date))
                self.time_off_table.setItem(row, 3, QTableWidgetItem(end_date))
                self.time_off_table.setItem(row, 4, QTableWidgetItem(f"{duration} days"))
                self.time_off_table.setItem(row, 5, QTableWidgetItem(status))
                
                # Add action buttons for pending requests - ONLY FOR DOCTORS
                if status == "Pending" and self.worker_role == "Doctor":
                    btn_widget = QWidget()
                    btn_layout = QHBoxLayout(btn_widget)
                    
                    approve_btn = QPushButton("Approve")
                    approve_btn.setStyleSheet("background-color: #2ecc71; color: white;")
                    approve_btn.clicked.connect(lambda _, wid=worker_id: self.update_time_off_status(wid, "Approved"))
                    
                    deny_btn = QPushButton("Deny")
                    deny_btn.setStyleSheet("background-color: #e74c3c; color: white;")
                    deny_btn.clicked.connect(lambda _, wid=worker_id: self.update_time_off_status(wid, "Denied"))
                    
                    btn_layout.addWidget(approve_btn)
                    btn_layout.addWidget(deny_btn)
                    btn_layout.setContentsMargins(0, 0, 0, 0)
                    
                    self.time_off_table.setCellWidget(row, 6, btn_widget)
                else:
                    if status == "Pending" and self.worker_role != "Doctor":
                        self.time_off_table.setItem(row, 6, QTableWidgetItem("Permission denied"))
                    else:
                        self.time_off_table.setItem(row, 6, QTableWidgetItem("No action"))
                    
        except Exception as e:
            print(f"Error loading time off data: {e}")
            QMessageBox.critical(self, "Error", f"Error loading time off data: {e}")
        finally:
            if cursor:
                cursor.close()

    def update_time_off_status(self, worker_id, new_status):
        """Update time off status in the database"""
        cursor = None
        try:
            cursor = self.db_connection.cursor()
            query = """
                UPDATE EMPLOYEES
                SET TIME_OFF_STATUS = :status
                WHERE WORKER_ID = :worker_id
            """
            cursor.execute(query, {'status': new_status, 'worker_id': worker_id})
            self.db_connection.commit()
            QMessageBox.information(self, "Success", f"Time off request {new_status.lower()}!")
            self.load_time_off_data()  # Refresh the view
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update status: {e}")
        finally:
            if cursor:
                cursor.close()

    def submit_time_off_request(self):
        """Handle submission of new time off requests"""
        worker_id = self.worker_id
        req_type = self.req_type_combo.currentText()
        start_date = self.req_start_date.date().toPyDate()
        end_date = self.req_end_date.date().toPyDate()
        
        if not worker_id or req_type == "Select Type":
            QMessageBox.warning(self, "Error", "Please select a request type")
            return
            
        if start_date > end_date:
            QMessageBox.warning(self, "Error", "End date must be after start date")
            return
            
        duration = (end_date - start_date).days + 1  # Inclusive of both dates
        
        cursor = None
        try:
            cursor = self.db_connection.cursor()
            query = """
                UPDATE EMPLOYEES
                SET 
                    TIME_OFF_STATUS = 'Pending',
                    TIME_OFF_TYPE = :req_type,
                    TIME_OFF_START_DATE = :start_date,
                    TIME_OFF_END_DATE = :end_date,
                    TIME_OFF_DURATION = :duration,
                    TIME_OFF_NOTES = :notes
                WHERE WORKER_ID = :worker_id
            """
            
            notes = f"{req_type} request submitted on {date.today()}"
            
            cursor.execute(query, {
                'req_type': req_type,
                'start_date': start_date,
                'end_date': end_date,
                'duration': duration,
                'notes': notes,
                'worker_id': worker_id
            })
            
            self.db_connection.commit()
            QMessageBox.information(self, "Success", "Time off request submitted!")
            
            # Reset form
            self.req_type_combo.setCurrentIndex(0)
            self.req_start_date.setDate(QDate.currentDate().addDays(1))
            self.req_end_date.setDate(QDate.currentDate().addDays(1))
            
            # Refresh data
            self.load_time_off_data()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to submit request: {e}")
        finally:
            if cursor:
                cursor.close()

    def update_week_label(self):
        if hasattr(self, 'week_label'):
            start_str = self.start_date.date().toString("MMM dd")
            end_str = self.end_date.date().toString("MMM dd, yyyy")
            self.week_label.setText(f"Week of {start_str} - {end_str}")

    def _generate_qchart(self, title, categories, values) -> QChart:
        """Generates and returns a QChart object with the given data."""
        bar_set = QBarSet("Value")
        numeric_values = []
        
        for v in values:
            try: 
                numeric_values.append(float(v))
            except (ValueError, TypeError): 
                numeric_values.append(0)
                
        bar_set.append(numeric_values)
        bar_series = QBarSeries()
        bar_series.append(bar_set)
        bar_series.setBarWidth(0.8)
        
        chart = QChart()
        chart.addSeries(bar_series)
        chart.setTitle(title)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.legend().setVisible(False)
        
        categories_axis = QBarCategoryAxis()
        categories_axis.append(categories)
        chart.addAxis(categories_axis, Qt.AlignBottom)
        bar_series.attachAxis(categories_axis)
        
        value_axis = QValueAxis()
        max_val = max(numeric_values) * 1.1 if numeric_values else 10
        min_val = 0
        value_axis.setRange(min_val, max_val if max_val > 0 else 10)
        value_axis.setLabelFormat("%.1f")
        chart.addAxis(value_axis, Qt.AlignLeft)
        bar_series.attachAxis(value_axis)
        
        return chart

    def create_bar_chart(self, title, categories, values):
        """Creates a QChartView containing a bar chart with given data."""
        chart = self._generate_qchart(title, categories, values)
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        return chart_view

class MainWindow(QMainWindow):
    def __init__(self, worker_id=None, full_name=None, role=None):
        super().__init__()
        self.worker_timing_widget = WorkerTimingSpace(worker_id, full_name, role, self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Employee Timing Management (Oracle DB - EMPLOYEES)")
        self.setMinimumSize(1200, 850)
        self.setCentralWidget(self.worker_timing_widget)

    def closeEvent(self, event):
        print("Close event triggered for MainWindow.")
        connection = self.worker_timing_widget.db_connection
        if connection:
            try: 
                connection.close()
                print("Database connection closed successfully.")
            except oracledb.Error as error: 
                print(f"Error closing Oracle connection: {error}")
                QMessageBox.warning(self, "DB Close Error", 
                                  f"Could not close the database connection cleanly.\nError: {error}")
            except Exception as e: 
                print(f"Unexpected error closing DB connection: {e}")
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # For testing, you can hardcode a role
    # In a real application, this would come from a login system
    test_role = "Doctor"  # or "Nurse" or any other role
    window = MainWindow(role=test_role)
    if window.worker_timing_widget.db_connection:
        window.show()
        sys.exit(app.exec_())
    else:
        print("Exiting application due to database connection failure on startup.")
        sys.exit(1)