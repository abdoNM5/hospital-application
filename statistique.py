import sys
import random
from datetime import datetime, timedelta
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QTabWidget, QLabel, QComboBox, QFrame, 
                            QPushButton, QGridLayout, QSizePolicy, QSpacerItem)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QIcon
import pyqtgraph as pg
import pandas as pd
import numpy as np

# Set global pyqtgraph configuration for a more professional look
pg.setConfigOption('background', 'w')  # White background
pg.setConfigOption('foreground', 'k')  # Black foreground


class StyledFrame(QFrame):
    """Custom styled panel for dashboard widgets"""
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setStyleSheet("""
            StyledFrame {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 6px;
            }
        """)
        
        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        # Title if provided
        if title:
            title_label = QLabel(title)
            title_label.setStyleSheet("""
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                padding-bottom: 5px;
            """)
            self.layout.addWidget(title_label)


class DiseaseStatsDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hospital Disease Statistics Dashboard")
        self.setGeometry(100, 100, 1280, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f7fa;
            }
            QTabWidget::pane {
                border: 1px solid #e0e0e0;
                background-color: #f5f7fa;
                border-radius: 4px;
            }
            QTabBar::tab {
                background-color: #e0e6f2;
                color: #2c3e50;
                border: 1px solid #b8c4d9;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #ffffff;
                border-bottom: 1px solid #ffffff;
            }
            QComboBox {
                border: 1px solid #b8c4d9;
                border-radius: 4px;
                padding: 4px 8px;
                background-color: white;
                min-width: 120px;
                height: 24px;
            }
            QLabel {
                color: #2c3e50;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        # Sample data - replace with your actual data loading mechanism
        self.load_data()
        
        # Create the main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Add header with hospital name and dashboard title
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                border-radius: 6px;
            }
        """)
        header_layout = QHBoxLayout(header_frame)
        
        hospital_name = QLabel("Central Medical Hospital")
        hospital_name.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
        """)
        
        dashboard_title = QLabel("Disease Statistics Dashboard")
        dashboard_title.setStyleSheet("""
            color: white;
            font-size: 24px;
            font-weight: bold;
        """)
        
        current_date = QLabel(datetime.now().strftime("%B %d, %Y"))
        current_date.setStyleSheet("""
            color: #ecf0f1;
            font-size: 14px;
        """)
        
        header_layout.addWidget(hospital_name)
        header_layout.addStretch()
        header_layout.addWidget(dashboard_title)
        header_layout.addStretch()
        header_layout.addWidget(current_date)
        
        main_layout.addWidget(header_frame)
        
        # Create filters section
        filter_frame = StyledFrame()
        filter_layout = QHBoxLayout()
        filter_layout.setContentsMargins(0, 0, 0, 0)
        
        date_label = QLabel("Time Period:")
        date_label.setStyleSheet("font-weight: bold;")
        
        self.period_combo = QComboBox()
        self.period_combo.addItems(["Last Week", "Last Month", "Last Quarter", "Last Year", "All Time"])
        self.period_combo.currentIndexChanged.connect(self.update_charts)
        
        dept_label = QLabel("Department:")
        dept_label.setStyleSheet("font-weight: bold;")
        
        self.dept_combo = QComboBox()
        self.dept_combo.addItems(["All Departments", "Cardiology", "Neurology", "Pediatrics", "Oncology", "Emergency"])
        self.dept_combo.currentIndexChanged.connect(self.update_charts)
        
        disease_label = QLabel("Disease Focus:")
        disease_label.setStyleSheet("font-weight: bold;")
        
        self.disease_combo = QComboBox()
        self.disease_combo.addItems(["All Diseases", "Influenza", "Diabetes", "Hypertension", "COVID-19", "Pneumonia"])
        self.disease_combo.currentIndexChanged.connect(self.update_charts)
        
        refresh_btn = QPushButton("Refresh Data")
        refresh_btn.setIcon(QIcon.fromTheme("view-refresh"))
        refresh_btn.clicked.connect(self.update_charts)
        
        filter_layout.addWidget(date_label)
        filter_layout.addWidget(self.period_combo)
        filter_layout.addSpacing(20)
        filter_layout.addWidget(dept_label)
        filter_layout.addWidget(self.dept_combo)
        filter_layout.addSpacing(20)
        filter_layout.addWidget(disease_label)
        filter_layout.addWidget(self.disease_combo)
        filter_layout.addStretch()
        filter_layout.addWidget(refresh_btn)
        
        filter_frame.layout.addLayout(filter_layout)
        main_layout.addWidget(filter_frame)
        
        # Create summary cards section
        summary_layout = QHBoxLayout()
        
        # Total cases card
        self.total_cases_frame = StyledFrame("Total Cases")
        self.total_cases_number = QLabel("0")
        self.total_cases_number.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            color: #3498db;
            text-align: center;
        """)
        self.total_cases_number.setAlignment(Qt.AlignCenter)
        self.total_cases_frame.layout.addWidget(self.total_cases_number)
        
        # Critical cases card
        self.critical_cases_frame = StyledFrame("Critical Cases")
        self.critical_cases_number = QLabel("0")
        self.critical_cases_number.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            color: #e74c3c;
            text-align: center;
        """)
        self.critical_cases_number.setAlignment(Qt.AlignCenter)
        self.critical_cases_frame.layout.addWidget(self.critical_cases_number)
        
        # Average age card
        self.avg_age_frame = StyledFrame("Average Patient Age")
        self.avg_age_number = QLabel("0")
        self.avg_age_number.setStyleSheet("""
            font-size: 36px;
            font-weight: bold;
            color: #2ecc71;
            text-align: center;
        """)
        self.avg_age_number.setAlignment(Qt.AlignCenter)
        self.avg_age_frame.layout.addWidget(self.avg_age_number)
        
        # Most common disease card
        self.common_disease_frame = StyledFrame("Most Common Disease")
        self.common_disease_name = QLabel("N/A")
        self.common_disease_name.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #9b59b6;
            text-align: center;
        """)
        self.common_disease_name.setAlignment(Qt.AlignCenter)
        self.common_disease_frame.layout.addWidget(self.common_disease_name)
        
        summary_layout.addWidget(self.total_cases_frame)
        summary_layout.addWidget(self.critical_cases_frame)
        summary_layout.addWidget(self.avg_age_frame)
        summary_layout.addWidget(self.common_disease_frame)
        
        main_layout.addLayout(summary_layout)
        
        # Create tab widget for different visualizations
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs, 1)  # Give the chart area more space
        
        # Create tabs for different charts
        self.create_disease_distribution_tab()
        self.create_trend_analysis_tab()
        self.create_demographics_tab()
        self.create_severity_analysis_tab()
        
        # Initial update
        self.update_charts()
        
    def load_data(self):
        # Simulated data - replace with actual data loading
        # In a real application, you would load this from a database or file
        diseases = ["Influenza", "Diabetes", "Hypertension", "Asthma", "COVID-19", 
                   "Pneumonia", "Heart Disease", "Cancer", "Stroke", "Arthritis"]
        
        # Generate sample data with more realistic patterns
        n_records = 5000
        
        # Create dates with higher frequency in winter months for some diseases
        winter_heavy = ["Influenza", "Pneumonia"]
        summer_heavy = ["Asthma", "Heat Stroke"]
        
        dates = []
        disease_list = []
        
        for _ in range(n_records):
           disease = np.random.choice(diseases)
        
        # Seasonal patterns - ensuring probabilities sum to exactly 1
        if disease in winter_heavy:
            # Winter heavy months (Jan, Feb, Dec have higher probabilities)
            month = np.random.choice(range(1, 13), p=[0.15, 0.15, 0.1, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.15])
        elif disease in summer_heavy:
            # Summer heavy months (May-Aug have higher probabilities)
            month = np.random.choice(range(1, 13), p=[0.05, 0.05, 0.05, 0.1, 0.15, 0.15, 0.15, 0.15, 0.05, 0.05, 0.05, 0.05])
        else:
            # Equal distribution throughout the year
            month = np.random.choice(range(1, 13), p=[1/12] * 12)
            
        day = np.random.choice(range(1, 29))
        year = 2024
        
        date = datetime(year, month, day)
        dates.append(date)
        disease_list.append(disease)
        
        # Create age distributions appropriate to each disease
        ages = []
        departments = []
        severities = []
        
        for disease in disease_list:
            if disease in ["Diabetes", "Heart Disease", "Stroke", "Arthritis"]:
                # More common in older patients
                age = int(np.random.beta(5, 2) * 90) + 10
                dept = np.random.choice(["Cardiology", "Internal Medicine", "Endocrinology"], 
                                       p=[0.5, 0.3, 0.2])
            elif disease in ["Asthma", "Influenza"]:
                # More distributed across ages
                age = int(np.random.beta(2, 2) * 90) + 5
                dept = np.random.choice(["Pulmonology", "Pediatrics", "Emergency"], 
                                       p=[0.4, 0.3, 0.3])
            elif disease == "Cancer":
                # Increases with age but can affect any age
                age = int(np.random.beta(3, 2) * 90) + 5
                dept = "Oncology"
            else:
                age = int(np.random.normal(45, 20))
                # Constrain age to reasonable range
                age = max(1, min(age, 99))
                dept = np.random.choice(["Emergency", "Internal Medicine", "Neurology", "Cardiology", "Pediatrics", "Oncology"])
                
            # Severity tends to increase with age
            age_factor = age / 100
            
            if disease in ["COVID-19", "Pneumonia", "Cancer"]:
                # These can be more severe
                p_severe = 0.4 + (0.3 * age_factor)
                p_critical = 0.1 + (0.2 * age_factor)
            else:
                p_severe = 0.2 + (0.2 * age_factor)
                p_critical = 0.05 + (0.1 * age_factor)
                
            p_moderate = 0.5 - (p_severe / 2) - (p_critical / 2)
            p_mild = 1 - p_severe - p_critical - p_moderate
            
            severity = np.random.choice(
                ["Mild", "Moderate", "Severe", "Critical"],
                p=[p_mild, p_moderate, p_severe, p_critical]
            )
            
            ages.append(age)
            departments.append(dept)
            severities.append(severity)
        
        # Construct the DataFrame
        self.data = pd.DataFrame({
            'disease': disease_list,
            'date': dates,
            'age': ages,
            'department': departments,
            'severity': severities,
        })
        
    def create_disease_distribution_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 10, 0, 0)
        tab.setLayout(layout)
        
        # Create plot widget
        self.disease_plot = pg.PlotWidget()
        self.disease_plot.setBackground('w')
        self.disease_plot.setTitle("Disease Distribution")
        self.disease_plot.setLabel('left', 'Number of Cases')
        self.disease_plot.setLabel('bottom', 'Disease')
        self.disease_plot.showGrid(x=True, y=True)
        self.disease_plot.getAxis('bottom').setTicks([])  # We'll handle labels in update_charts
        layout.addWidget(self.disease_plot)
        
        self.tabs.addTab(tab, "Disease Distribution")
    
    def create_trend_analysis_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 10, 0, 0)
        tab.setLayout(layout)
        
        # Create plot widget
        self.trend_plot = pg.PlotWidget()
        self.trend_plot.setBackground('w')
        self.trend_plot.setTitle("Disease Trends Over Time")
        self.trend_plot.setLabel('left', 'Number of Cases')
        self.trend_plot.setLabel('bottom', 'Time')
        self.trend_plot.showGrid(x=True, y=True)
        layout.addWidget(self.trend_plot)
        
        self.tabs.addTab(tab, "Trend Analysis")
    
    def create_demographics_tab(self):
        tab = QWidget()
        layout = QGridLayout()
        layout.setContentsMargins(0, 10, 0, 0)
        tab.setLayout(layout)
        
        # Age distribution chart
        self.age_dist_plot = pg.PlotWidget()
        self.age_dist_plot.setBackground('w')
        self.age_dist_plot.setTitle("Age Distribution of Patients")
        self.age_dist_plot.setLabel('left', 'Number of Cases')
        self.age_dist_plot.setLabel('bottom', 'Age Group')
        self.age_dist_plot.showGrid(x=True, y=True)
        
        # Department distribution chart
        self.dept_dist_plot = pg.PlotWidget()
        self.dept_dist_plot.setBackground('w')
        self.dept_dist_plot.setTitle("Cases by Department")
        self.dept_dist_plot.setLabel('left', 'Number of Cases')
        self.dept_dist_plot.setLabel('bottom', 'Department')
        self.dept_dist_plot.showGrid(x=True, y=True)
        
        layout.addWidget(self.age_dist_plot, 0, 0)
        layout.addWidget(self.dept_dist_plot, 0, 1)
        
        self.tabs.addTab(tab, "Demographics")
    
    def create_severity_analysis_tab(self):
        tab = QWidget()
        layout = QGridLayout()
        layout.setContentsMargins(0, 10, 0, 0)
        tab.setLayout(layout)
        
        # Overall severity chart
        self.severity_plot = pg.PlotWidget()
        self.severity_plot.setBackground('w')
        self.severity_plot.setTitle("Overall Disease Severity")
        self.severity_plot.setLabel('left', 'Number of Cases')
        self.severity_plot.setLabel('bottom', 'Severity Level')
        self.severity_plot.showGrid(x=True, y=True)
        
        # Severity by disease chart
        self.severity_by_disease_plot = pg.PlotWidget()
        self.severity_by_disease_plot.setBackground('w')
        self.severity_by_disease_plot.setTitle("Severity by Top 5 Diseases")
        self.severity_by_disease_plot.setLabel('left', 'Percentage of Cases')
        self.severity_by_disease_plot.setLabel('bottom', 'Disease')
        self.severity_by_disease_plot.showGrid(x=True, y=True)
        
        layout.addWidget(self.severity_plot, 0, 0)
        layout.addWidget(self.severity_by_disease_plot, 0, 1)
        
        self.tabs.addTab(tab, "Severity Analysis")
    
    def update_charts(self):
        # Filter data based on selected period and department
        period = self.period_combo.currentText()
        dept = self.dept_combo.currentText().replace("All Departments", "")
        disease = self.disease_combo.currentText().replace("All Diseases", "")
        
        filtered_data = self.data.copy()
        
        # Apply department filter
        if dept:
            filtered_data = filtered_data[filtered_data['department'] == dept]
        
        # Apply disease filter
        if disease:
            filtered_data = filtered_data[filtered_data['disease'] == disease]
        
        # Apply period filter
        days = 0
        if period == "Last Week":
            days = 7
        elif period == "Last Month":
            days = 30
        elif period == "Last Quarter":
            days = 90
        elif period == "Last Year":
            days = 365
            
        if days > 0:
            cutoff_date = datetime.now() - timedelta(days=days)
            filtered_data = filtered_data[filtered_data['date'] >= cutoff_date]
        
        # Update summary cards
        self.update_summary_cards(filtered_data)
        
        # Update the disease count plot
        self.update_disease_distribution_plot(filtered_data)
        
        # Update the trend analysis plot
        self.update_trend_analysis_plot(filtered_data)
        
        # Update the demographics plots
        self.update_demographics_plots(filtered_data)
        
        # Update the severity analysis plot
        self.update_severity_analysis_plots(filtered_data)
    
    def update_summary_cards(self, data):
        # Update total cases
        total_cases = len(data)
        self.total_cases_number.setText(f"{total_cases:,}")
        
        # Update critical cases
        critical_cases = len(data[data['severity'] == 'Critical'])
        self.critical_cases_number.setText(f"{critical_cases:,}")
        
        # Update average age
        avg_age = data['age'].mean()
        self.avg_age_number.setText(f"{avg_age:.1f}")
        
        # Update most common disease
        if not data.empty:
            common_disease = data['disease'].value_counts().idxmax()
            self.common_disease_name.setText(common_disease)
        else:
            self.common_disease_name.setText("N/A")
    
    def update_disease_distribution_plot(self, data):
        # Clear the plot
        self.disease_plot.clear()
        
        if data.empty:
            return
            
        # Count diseases
        disease_counts = data['disease'].value_counts().nlargest(10)  # Top 10 diseases
        
        # Create bar chart
        x = np.arange(len(disease_counts))
        y = disease_counts.values
        
        # Create bar graph with professional color
        bar_graph = pg.BarGraphItem(x=x, height=y, width=0.6, brush=(52, 152, 219))
        self.disease_plot.addItem(bar_graph)
        
        # Set x-axis labels
        ticks = [(i, name) for i, name in enumerate(disease_counts.index)]
        self.disease_plot.getAxis('bottom').setTicks([ticks])
    
    def update_trend_analysis_plot(self, data):
        # Clear the plot
        self.trend_plot.clear()
        
        if data.empty:
            return
            
        # Group by week for a cleaner trend line
        data['week'] = pd.to_datetime(data['date']).dt.isocalendar().week
        data['year'] = pd.to_datetime(data['date']).dt.isocalendar().year
        time_series = data.groupby(['year', 'week']).size()
        
        # Convert to lists for plotting
        x = list(range(len(time_series)))
        y = time_series.values
        
        # Create line plot with professional styling
        pen = pg.mkPen(color=(41, 128, 185), width=3)
        self.trend_plot.plot(x, y, pen=pen, symbol='o', symbolSize=6, symbolBrush=(41, 128, 185))
        
        # Add labels for x-axis
        tick_labels = []
        for i, (year, week) in enumerate(time_series.index):
            if i % 4 == 0:  # Only show every 4th label to avoid crowding
                tick_labels.append((i, f"{year}-W{week}"))
        
        if tick_labels:
            self.trend_plot.getAxis('bottom').setTicks([tick_labels])
    
    def update_demographics_plots(self, data):
        # Clear the plots
        self.age_dist_plot.clear()
        self.dept_dist_plot.clear()
        
        if data.empty:
            return
            
        # Age distribution
        age_bins = [(0, 10), (11, 20), (21, 30), (31, 40), (41, 50), 
                    (51, 60), (61, 70), (71, 80), (81, 90), (91, 100)]
        age_labels = ['0-10', '11-20', '21-30', '31-40', '41-50', 
                      '51-60', '61-70', '71-80', '81-90', '91-100']
        
        # Create age groups
        data['age_group'] = pd.cut(data['age'], bins=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 
                                   labels=age_labels)
        
        # Count by age group
        age_counts = data['age_group'].value_counts().reindex(age_labels)
        
        # Create bar chart
        x = np.arange(len(age_counts))
        y = age_counts.values
        
        # Create bar graph with professional color
        bar_graph = pg.BarGraphItem(x=x, height=y, width=0.6, brush=(46, 204, 113))
        self.age_dist_plot.addItem(bar_graph)
        
        # Set x-axis labels
        ticks = [(i, name) for i, name in enumerate(age_counts.index)]
        self.age_dist_plot.getAxis('bottom').setTicks([ticks])
        
        # Department distribution
        dept_counts = data['department'].value_counts()
        
        # Create bar chart
        x = np.arange(len(dept_counts))
        y = dept_counts.values
        
        # Create bar graph with professional color
        bar_graph = pg.BarGraphItem(x=x, height=y, width=0.6, brush=(142, 68, 173))
        self.dept_dist_plot.addItem(bar_graph)
        
        # Set x-axis labels
        ticks = [(i, name) for i, name in enumerate(dept_counts.index)]
        self.dept_dist_plot.getAxis('bottom').setTicks([ticks])
    
    def update_severity_analysis_plots(self, data):
        # Clear the plots
        self.severity_plot.clear()
        self.severity_by_disease_plot.clear()
        
        if data.empty:
            return
            
        # Overall severity counts
        severity_order = ['Mild', 'Moderate', 'Severe', 'Critical']
        severity_counts = data['severity'].value_counts().reindex(severity_order)
        
        # Create bar chart for overall severity
        x = np.arange(len(severity_counts))
        y = severity_counts.values
        
        # Define colors based on severity
        severity_colors = {
            'Mild': (46, 204, 113),      # Green
            'Moderate': (241, 196, 15),  # Yellow
            'Severe': (230, 126, 34),    # Orange
            'Critical': (231, 76, 60)    # Red
        }
        
        # Create individual bar graph items with different colors
        for i, severity in enumerate(severity_counts.index):
            if pd.notna(severity):  # Check if severity is not NaN
                color = severity_colors.get(severity, (52, 152, 219))  # Default blue
                bar = pg.BarGraphItem(x=[i], height=[severity_counts[severity]], width=0.6, brush=color)
                self.severity_plot.addItem(bar)
        
        # Set x-axis labels
        ticks = [(i, name) for i, name in enumerate(severity_counts.index)]
        self.severity_plot.getAxis('bottom').setTicks([ticks])
        
        # Severity by disease (stacked bar chart)
        top_diseases = data['disease'].value_counts().nlargest(5).index.tolist()
        disease_data = data[data['disease'].isin(top_diseases)]
        
        # Create severity percentages by disease
        severity_by_disease = pd.crosstab(disease_data['disease'], disease_data['severity'], 
                                          normalize='index') * 100
        
        # Reindex to ensure all severity levels are included
        severity_by_disease = severity_by_disease.reindex(columns=severity_order, fill_value=0)
        
        # Create stacked bar chart
        bar_offset = np.zeros(len(top_diseases))
        
        for i, severity in enumerate(severity_order):
            if severity in severity_by_disease.columns:
                x = np.arange(len(top_diseases))
                y = severity_by_disease[severity].values
                
                # Color based on severity
                color = severity_colors.get(severity, (52, 152, 219))
                
                # Add bar for this severity level
                bars = pg.BarGraphItem(x=x, height=y, width=0.6, brush=color, name=severity)
                self.severity_by_disease_plot.addItem(bars)
        
        # Set x-axis labels
        ticks = [(i, name) for i, name in enumerate(top_diseases)]
        self.severity_by_disease_plot.getAxis('bottom').setTicks([ticks])
        
        # Add legend
        legend = self.severity_by_disease_plot.addLegend()
        for severity, color in severity_colors.items():
            legend.addItem(pg.BarGraphItem(x=[0], height=[0], width=0.6, brush=color), severity)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiseaseStatsDashboard()
    window.show()
    sys.exit(app.exec_())