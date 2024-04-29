import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QLabel, QSlider, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np
import matplotlib.pyplot as plt


class ImageProcessor(QMainWindow):

    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Image Processor")
        self.setGeometry(100, 100, 800, 600)

        # Create the widgets
        self.image_label = QLabel()
        self.brightness_label = QLabel("Brightness: 0")
        self.brightness_slider = QSlider(Qt.Horizontal)
        self.brightness_slider.setMinimum(-50)
        self.brightness_slider.setMaximum(50)
        self.brightness_slider.setValue(0)
        self.contrast_label = QLabel("Contrast: 0")
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setMinimum(-50)
        self.contrast_slider.setMaximum(300)
        self.contrast_slider.setSingleStep(1)
        self.contrast_slider.setValue(0)
        self.reset_button = QPushButton("Reset")
        self.histogram_label = QLabel()

        # Create the layout
        layout = QGridLayout()
        layout.addWidget(self.image_label, 0, 0, 1, 4)
        layout.addWidget(self.brightness_label, 1, 0)
        layout.addWidget(self.brightness_slider, 1, 1, 1, 3)
        layout.addWidget(self.contrast_label, 2, 0)
        layout.addWidget(self.contrast_slider, 2, 1, 1, 3)
        layout.addWidget(self.reset_button, 3, 3)

        histogram_layout = QVBoxLayout()
        histogram_layout.addWidget(self.histogram_label)

        # Create the central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Connect the signals
        self.brightness_slider.valueChanged.connect(self.update_brightness_label)
        self.contrast_slider.valueChanged.connect(self.update_contrast_label)
        self.reset_button.clicked.connect(self.reset_sliders)

        # Load the default image
        self.image_path = "peppers_bw.jpg"
        self.update_image()

    def update_image(self):
        # Load the image
        image = cv2.imread(self.image_path)

        # Adjust the image based on the slider values
        brightness = self.brightness_slider.value()
        contrast = self.contrast_slider.value()
        adjusted_image = self.adjust_brightness_contrast(image, brightness, contrast)

        # Display the image in the GUI
        height, width, channel = adjusted_image.shape
        bytes_per_line = channel * width
        q_image = QImage(adjusted_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap(q_image)
        self.image_label.setPixmap(pixmap)

    def adjust_brightness_contrast(self, image, brightness, contrast):
        # Convert the image to a signed 16-bit data type
        image = image.astype(np.int16)
        
        # Adjust the brightness and contrast
        alpha = (contrast + 100) / 100
        beta = brightness
        adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        
        # Convert the image back to unsigned 8-bit data type
        adjusted_image = adjusted_image.astype(np.uint8)
        
        return adjusted_image


    def update_brightness_label(self):
        value = self.brightness_slider.value()
        self.brightness_label.setText(f"Brightness: {value}")

        # Update the image display
        self.update_image()

    def update_contrast_label(self):
        value = self.contrast_slider.value()
        self.contrast_label.setText(f"Contrast: {value}")

        # Update the image display
        self.update_image()

    def reset_sliders(self):
        self.brightness_slider.setValue(0)
        self.contrast_slider.setValue(0)


if __name__ == '__main__':
    app = QApplication([])
    window = ImageProcessor()
    window.show()
    app.exec_()
