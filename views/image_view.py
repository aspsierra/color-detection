from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import numpy as np


class ImageView(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.image_label = QLabel()
        self.color_label = QLabel("Double-click on the image to select a color.")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.color_label)
        self.setLayout(layout)
        self.setWindowTitle("Color Picker")

    def load_image(self, file_path):
        """Load and display the image."""
        self.image = cv2.imread(file_path)
        if self.image is None:
            raise ValueError("Failed to load the image. Please check the file.")

        self.display_image()

    def display_image(self):
        """Convert the image to Qt format and display it."""
        rgb_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)

    def get_image_rgb(self, x, y):
        """Get the RGB values of the pixel at (x, y)."""
        b, g, r = self.image[y, x]
        return r, g, b

    def update_color_label(self, text, bg_color, text_color):
        """Update the label with color information."""
        self.color_label.setText(text)
        self.color_label.setStyleSheet(f"background-color: {bg_color}; color: {text_color}; padding: 5px;")

    def mouseDoubleClickEvent(self, event):
        """Handle double-click to select a color."""
        if event.button() == Qt.LeftButton:
            x = event.pos().x() - self.image_label.geometry().x()
            y = event.pos().y() - self.image_label.geometry().y()

            # Ensure the click is within the image bounds
            if 0 <= x < self.image.shape[1] and 0 <= y < self.image.shape[0]:
                rgb = self.get_image_rgb(x, y)
                self.controller.handle_color_selection(rgb)
