from PyQt5 import QtWidgets, QtGui, QtCore

class AnimatedButton(QtWidgets.QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_geometry = None
        self.animation = QtCore.QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(150)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        
    def enterEvent(self, event):
        if self.original_geometry is None:
            self.original_geometry = self.geometry()
        new_rect = self.original_geometry.adjusted(-3, -3, 3, 3)
        self.animation.stop()
        self.animation.setStartValue(self.geometry())
        self.animation.setEndValue(new_rect)
        self.animation.start()
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QtGui.QColor(0, 0, 0, 80))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        if self.original_geometry is not None:
            self.animation.stop()
            self.animation.setStartValue(self.geometry())
            self.animation.setEndValue(self.original_geometry)
            self.animation.start()
            self.setGraphicsEffect(None)
        super().leaveEvent(event)


class BackgroundImageFrame(QtWidgets.QFrame):
    def __init__(self, parent=None, background_image=None):
        super().__init__(parent)
        self.background_image = background_image
        self.parent_widget = parent
        
    def setBackgroundImage(self, pixmap):
        self.background_image = pixmap
        self.update()
        
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        
        # Draw rounded corners and border
        path = QtGui.QPainterPath()
        path.addRoundedRect(QtCore.QRectF(self.rect()), 20, 20)
        painter.setClipPath(path)
        
        if self.background_image and not self.background_image.isNull():
            # Scale the background image to fit the frame nicely
            scaled_img = self.background_image.scaled(
                self.size(),
                QtCore.Qt.KeepAspectRatioByExpanding,
                QtCore.Qt.SmoothTransformation
            )
            
            # Center the image within frame
            pos_x = (self.width() - scaled_img.width()) // 2
            pos_y = (self.height() - scaled_img.height()) // 2
            
            # Draw the background image
            painter.drawPixmap(pos_x, pos_y, scaled_img)
            
            # Add a subtle overlay for better text visibility
            painter.fillRect(self.rect(), QtGui.QColor(0, 0, 0, 40))
        else:
            # Fallback gradient if image loading fails
            gradient = QtGui.QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QtGui.QColor("#3498db"))
            gradient.setColorAt(1, QtGui.QColor("#2c3e50"))
            painter.fillRect(self.rect(), gradient)
        
        # Draw a border
        painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255, 100), 1))
        painter.drawRoundedRect(0, 0, self.width()-1, self.height()-1, 20, 20)


class ExitPage(QtWidgets.QWidget):
    def __init__(self, stacked_widget, parent=None):
        super().__init__(parent)
        self.stacked_widget = stacked_widget
        # Load main background
        self.bg_pixmap = QtGui.QPixmap("resources/hospital-bg5.jpg")
        if self.bg_pixmap.isNull():
            print("Warning: Failed to load background image from resources/hospital-bg5.jpg")
        
        # Load frame background
        self.frame_bg_pixmap = QtGui.QPixmap("resources/app2bg.jpg")
        if self.frame_bg_pixmap.isNull():
            print("Warning: Failed to load frame background image from resources/app2bg.jpg")
            # Fall back to main background if frame background fails
            self.frame_bg_pixmap = self.bg_pixmap
        
        self.setup_ui()

    def setup_ui(self):
        # Main layout for the widget
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Add a semi-transparent overlay panel behind the frame
        self.overlay = QtWidgets.QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 130);")
        self.overlay.setGeometry(self.rect())
        self.overlay.hide()

        # Create the custom frame for the exit box with background image
        self.frame = BackgroundImageFrame(self, self.frame_bg_pixmap)
        self.frame.setFixedSize(550, 380)
        
        # Add shadow effect to the frame
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QtGui.QColor(0, 0, 0, 80))
        shadow.setOffset(0, 2)
        self.frame.setGraphicsEffect(shadow)
        
        frame_layout = QtWidgets.QVBoxLayout(self.frame)
        frame_layout.setSpacing(20)
        frame_layout.setContentsMargins(30, 40, 30, 40)
        frame_layout.setAlignment(QtCore.Qt.AlignCenter)
        
        # Title label with modern font
        self.title_label = QtWidgets.QLabel("Confirm Exit")
        self.title_label.setAlignment(QtCore.Qt.AlignCenter)
        self.title_label.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
        self.title_label.setStyleSheet("""
            color: #00008B; 
            padding: 8px;
            background-color: rgba(0, 0, 0, 40);
            border-radius: 10px;
        """)
        frame_layout.addWidget(self.title_label)
        
        # Add some spacing
        frame_layout.addSpacing(20)
        
        # Exit question label
        self.question_label = QtWidgets.QLabel("Are you sure you want to exit the application?")
        self.question_label.setAlignment(QtCore.Qt.AlignCenter)
        self.question_label.setWordWrap(True)
        self.question_label.setFont(QtGui.QFont("Segoe UI", 14))
        self.question_label.setStyleSheet("""
            color: white;
            background-color: rgba(0, 0, 0, 40);
            padding: 15px;
            border-radius: 10px;
        """)
        frame_layout.addWidget(self.question_label)
        
        # Add spacer
        frame_layout.addSpacing(30)
        
        # Button layout for Yes/No buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(30)
        button_layout.setAlignment(QtCore.Qt.AlignCenter)

        # No Button (returns to previous page)
        self.no_button = AnimatedButton("Cancel")
        self.no_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(240, 240, 240, 230);
                color: #2c3e50;
                padding: 14px;
                border-radius: 10px;
                border: 1px solid #e0e0e0;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 250);
            }
            QPushButton:pressed {
                background-color: rgba(220, 220, 220, 250);
            }
        """)
        self.no_button.setFont(QtGui.QFont("Segoe UI", 12))
        self.no_button.setFixedWidth(160)
        self.no_button.clicked.connect(self.go_back)

        # Yes Button (exits the application)
        self.yes_button = AnimatedButton("Exit")
        self.yes_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(231, 76, 60, 230);
                color: white;
                padding: 14px;
                border-radius: 10px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(192, 57, 43, 250);
            }
            QPushButton:pressed {
                background-color: rgba(169, 50, 38, 250);
            }
        """)
        self.yes_button.setFont(QtGui.QFont("Segoe UI", 12))
        self.yes_button.setFixedWidth(160)
        self.yes_button.clicked.connect(QtWidgets.qApp.quit)

        button_layout.addWidget(self.no_button)
        button_layout.addWidget(self.yes_button)
        frame_layout.addLayout(button_layout)

        self.layout.addWidget(self.frame)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, 'overlay'):
            self.overlay.setGeometry(self.rect())

    def paintEvent(self, event):
        # Draw the background for the entire widget
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        
        if not self.bg_pixmap.isNull():
            scaled_pixmap = self.bg_pixmap.scaled(
                self.size(),
                QtCore.Qt.KeepAspectRatioByExpanding,
                QtCore.Qt.SmoothTransformation
            )
            
            pos_x = (self.width() - scaled_pixmap.width()) // 2 if scaled_pixmap.width() > self.width() else 0
            pos_y = (self.height() - scaled_pixmap.height()) // 2 if scaled_pixmap.height() > self.height() else 0
            
            painter.drawPixmap(pos_x, pos_y, scaled_pixmap)
            
            # Add a subtle gradient overlay
            gradient = QtGui.QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QtGui.QColor(0, 0, 0, 40))
            gradient.setColorAt(1, QtGui.QColor(0, 0, 0, 100))
            painter.fillRect(self.rect(), gradient)
        else:
            # If no background image, use a gradient
            gradient = QtGui.QLinearGradient(0, 0, 0, self.height())
            gradient.setColorAt(0, QtGui.QColor("#3498db"))
            gradient.setColorAt(1, QtGui.QColor("#2c3e50"))
            painter.fillRect(self.rect(), gradient)

    def showEvent(self, event):
        super().showEvent(event)
        
        # Show the overlay with fade-in effect
        self.overlay.show()
        overlay_effect = QtWidgets.QGraphicsOpacityEffect(self.overlay)
        self.overlay.setGraphicsEffect(overlay_effect)
        overlay_animation = QtCore.QPropertyAnimation(overlay_effect, b"opacity")
        overlay_animation.setDuration(300)
        overlay_animation.setStartValue(0)
        overlay_animation.setEndValue(1)
        overlay_animation.start()
        
        # Create scale + opacity animation for the frame
        self.frame.setGraphicsEffect(None)
        combined_effect = QtWidgets.QGraphicsOpacityEffect(self.frame)
        self.frame.setGraphicsEffect(combined_effect)
        
        self.frame_animation = QtCore.QPropertyAnimation(combined_effect, b"opacity")
        self.frame_animation.setDuration(400)
        self.frame_animation.setStartValue(0)
        self.frame_animation.setEndValue(1)
        self.frame_animation.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        
        # Scale animation
        self.frame_scale = QtCore.QPropertyAnimation(self.frame, b"geometry")
        current_geometry = self.frame.geometry()
        start_geometry = QtCore.QRect(
            current_geometry.x() + current_geometry.width() // 2 - 10,
            current_geometry.y() + current_geometry.height() // 2 - 10,
            20, 20
        )
        self.frame_scale.setStartValue(start_geometry)
        self.frame_scale.setEndValue(current_geometry)
        self.frame_scale.setDuration(400)
        self.frame_scale.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        
        # Start animations together
        self.animation_group = QtCore.QParallelAnimationGroup()
        self.animation_group.addAnimation(self.frame_animation)
        self.animation_group.addAnimation(self.frame_scale)
        self.animation_group.finished.connect(self.restore_shadow)
        self.animation_group.start()

    def restore_shadow(self):
        shadow = QtWidgets.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QtGui.QColor(0, 0, 0, 80))
        shadow.setOffset(0, 2)
        self.frame.setGraphicsEffect(shadow)

    def go_back(self):
        # Fade out animation
        fade_effect = QtWidgets.QGraphicsOpacityEffect(self.frame)
        self.frame.setGraphicsEffect(fade_effect)
        fade_out = QtCore.QPropertyAnimation(fade_effect, b"opacity")
        fade_out.setDuration(250)
        fade_out.setStartValue(1)
        fade_out.setEndValue(0)
        fade_out.finished.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        fade_out.start()
        
        # Also fade out the overlay
        overlay_effect = QtWidgets.QGraphicsOpacityEffect(self.overlay)
        self.overlay.setGraphicsEffect(overlay_effect)
        overlay_fade = QtCore.QPropertyAnimation(overlay_effect, b"opacity")
        overlay_fade.setDuration(250)
        overlay_fade.setStartValue(1)
        overlay_fade.setEndValue(0)
        overlay_fade.start()