from PyQt5 import QtWidgets, QtGui, QtCore

class AbtusPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(600, 300)  # Définir une taille minimale
        self.setup_ui()

    def setup_ui(self):
        # Main layout with proper spacing
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setStyleSheet("background-color: #f8f9fa;")

        # Header Section
        self.header = QtWidgets.QFrame()
        self.header.setStyleSheet("background-color: #005b96; padding: 5px;")
        self.header_layout = QtWidgets.QVBoxLayout(self.header)
        
        # Title with proper font and anti-aliasing
        self.title_label = QtWidgets.QLabel("About Our Hospital")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        title_font = QtGui.QFont("Segoe UI", 16, QtGui.QFont.Bold)  # Smaller font
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("""
            color: white;
            padding: 0;
            margin: 0;
        """)
        self.header_layout.addWidget(self.title_label)
        self.layout.addWidget(self.header)

        # Content Area with Scroll
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none;")
        self.scroll_area.setMinimumHeight(600)  # Permet un meilleur affichage
        # self.scroll_area.setMinimumWidth(500)  # Ajuster pour éviter un texte tronqué

        
        self.content_widget = QtWidgets.QWidget()
        self.content_layout = QtWidgets.QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.content_layout.setSpacing(20)

        # Hospital Overview Section
        self.add_section(
            "ENSA-H HOSPITAL OVERVIEW",
            "Founded in 1990, ENSA-H Hospital has grown to become a premier healthcare institution. "
            "Our JCI-accredited facility offers comprehensive medical services across 32 specialties, "
            "combining cutting-edge technology with compassionate patient care.",
            "#e6f2ff"
        )

        # Mission/Vision Section
        self.add_section(
            "OUR MISSION & VISION",
            "<b>Mission:</b> To deliver exceptional healthcare through innovation, excellence, and "
            "compassionate patient-centered care.<br><br>"
            "<b>Vision:</b> To be recognized as a global leader in healthcare, setting standards for "
            "quality, research, and medical education.",
            "#fff4e6"
        )

        # Key Features
        self.add_feature_list()

        # Leadership Quote
        self.add_quote(
            "\"At ENSA-H Hospital, we combine medical excellence with human compassion. Every patient "
            "receives personalized care from our dedicated team of healthcare professionals.\"",
            "Dr. Sarah Johnson, Chief Medical Officer"
        )

        # Contact Information
        self.add_section(
            "CONTACT US",
            "📞 <b>Main Line:</b> +1 (555) 123-4567<br>"
            "🚑 <b>Emergency:</b> +1 (555) 987-6543<br>"
            "📧 <b>Email:</b> info@ensa-h.org<br>"
            "🌐 <b>Website:</b> www.ensa-h.org<br>"
            "📍 <b>Address:</b> 123 Medical Center Drive, City, Country",
            "#f0f8ff"
        )

        self.scroll_area.setWidget(self.content_widget)
        self.layout.addWidget(self.scroll_area)

        # Navigation Footer
        # self.footer = QtWidgets.QFrame()
        # self.footer.setStyleSheet("background-color: white; padding: 15px; border-top: 1px solid #e0e6ed;")
        # self.footer_layout = QtWidgets.QHBoxLayout(self.footer)
        
        # self.back_button = self.create_button("← Back to Main Menu", "#6c757d")
        # self.contact_button = self.create_button("Contact Support", "#005b96")
        
        # self.footer_layout.addWidget(self.back_button)
        # self.footer_layout.addStretch()
        # self.footer_layout.addWidget(self.contact_button)
        
        # self.layout.addWidget(self.footer)

    def add_section(self, title, content, bg_color):
        group = QtWidgets.QGroupBox(title)
        group.setStyleSheet(f"""
            QGroupBox {{
                font: bold 16px 'Segoe UI';
                color: #005b96;
                border: 1px solid #e0e6ed;
                border-radius: 8px;
                background-color: {bg_color};
                margin-top: 16px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """)
        
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(15, 25, 15, 15)
        
        label = QtWidgets.QLabel(content)
        label.setFont(QtGui.QFont("Segoe UI", 12))
        label.setWordWrap(True)
        label.setStyleSheet("color: #333; line-height: 1.5;")
        
        layout.addWidget(label)
        group.setLayout(layout)
        self.content_layout.addWidget(group)

    def add_feature_list(self):
        group = QtWidgets.QGroupBox("WHY CHOOSE ENSA-H?")
        group.setStyleSheet("""
            QGroupBox {
                font: bold 16px 'Segoe UI';
                color: #005b96;
                border: 1px solid #e0e6ed;
                border-radius: 8px;
                margin-top: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        
        features = [
            "✔ 24/7 Emergency & Trauma Center",
            "✔ Advanced Cardiac Care Unit",
            "✔ Robotic Surgery Capabilities",
            "✔ Electronic Medical Records System",
            "✔ Multilingual Staff & Interpreters",
            "✔ Patient-Centered Care Philosophy"
        ]
        
        layout = QtWidgets.QVBoxLayout()
        for feature in features:
            label = QtWidgets.QLabel(feature)
            label.setFont(QtGui.QFont("Segoe UI", 12))
            label.setStyleSheet("padding: 8px 0; color: #333;")
            layout.addWidget(label)
        
        group.setLayout(layout)
        self.content_layout.addWidget(group)

    def add_quote(self, text, author):
        frame = QtWidgets.QFrame()
        frame.setStyleSheet("""
            background-color: #f8f9fa;
            border-left: 4px solid #005b96;
            padding: 15px;
            margin: 20px 0;
        """)
        
        layout = QtWidgets.QVBoxLayout(frame)
        
        quote_label = QtWidgets.QLabel(f"<i>\"{text}\"</i>")
        quote_label.setFont(QtGui.QFont("Segoe UI", 12))
        quote_label.setStyleSheet("color: #555;")
        quote_label.setWordWrap(True)
        
        author_label = QtWidgets.QLabel(f"<div align='right' style='font-weight: bold;'>{author}</div>")
        author_label.setFont(QtGui.QFont("Segoe UI", 11))
        author_label.setStyleSheet("color: #005b96; margin-top: 10px;")
        
        layout.addWidget(quote_label)
        layout.addWidget(author_label)
        self.content_layout.addWidget(frame)

    def create_button(self, text, color):
        button = QtWidgets.QPushButton(text)
        button.setFont(QtGui.QFont("Segoe UI", 10, QtGui.QFont.Bold))
        button.setMinimumHeight(40)
        button.setMinimumWidth(180)
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 6px;
                padding: 0 20px;
            }}
            QPushButton:hover {{
                background-color: {self.darken_color(color)};
            }}
        """)
        return button

    def darken_color(self, hex_color, factor=0.8):
        """Utility to darken colors for hover effects"""
        color = QtGui.QColor(hex_color)
        return color.darker(int(1/(factor)*100)).name()