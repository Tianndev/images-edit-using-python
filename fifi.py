import sys
import os
try:
    import cv2
except ImportError:
    print(">> Installing OpenCV... <<")
    os.system("pip install opencv-python")
    print(">> Installing PyQt5... <<")
    os.system("pip install PyQt5")
    import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QVBoxLayout, QWidget, QFileDialog, QMessageBox, QSlider
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
try:
    import rich
except ImportError:
    print(">> Installing rich... <<")
    os.system("pip install rich")
from rich.panel import Panel as panel
from rich import print as prints

class ImageProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tiann Devz")
        self.image = None
        self.processed_image = None
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.title_label = QLabel("Image Processor")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title_label)
        self.open_button = QPushButton("Open Image")
        self.open_button.clicked.connect(self.open_image)
        self.layout.addWidget(self.open_button)
        self.effect_label = QLabel("Choose Effect:")
        self.layout.addWidget(self.effect_label)
        self.effect_combobox = QComboBox()
        self.effect_combobox.addItems(["", "Blur", "Rotate", "Crop", "Invers"])
        self.effect_combobox.currentIndexChanged.connect(self.show_effect_options)
        self.layout.addWidget(self.effect_combobox)
        self.blur_slider = QSlider(Qt.Horizontal)
        self.blur_slider.setRange(0, 100)
        self.blur_slider.setValue(0)
        self.blur_slider.setTickInterval(5)
        self.blur_slider.setTickPosition(QSlider.TicksBelow)
        self.blur_slider.valueChanged.connect(self.update_blur_label)
        self.layout.addWidget(self.blur_slider)
        self.blur_label = QLabel("Blur Percentage: 0")
        self.layout.addWidget(self.blur_label)
        self.blur_slider.hide()
        self.blur_label.hide()
        self.crop_widget = QWidget()
        self.crop_layout = QVBoxLayout(self.crop_widget)
        self.crop_x_slider = QSlider(Qt.Horizontal)
        self.crop_x_slider.setRange(0, 100)
        self.crop_x_slider.setValue(0)
        self.crop_x_slider.valueChanged.connect(self.update_crop_x_label)
        self.crop_x_label = QLabel("Crop X: 0")
        self.crop_layout.addWidget(self.crop_x_label)
        self.crop_layout.addWidget(self.crop_x_slider)
        self.crop_y_slider = QSlider(Qt.Horizontal)
        self.crop_y_slider.setRange(0, 100)
        self.crop_y_slider.setValue(0)
        self.crop_y_slider.valueChanged.connect(self.update_crop_y_label)
        self.crop_y_label = QLabel("Crop Y: 0")
        self.crop_layout.addWidget(self.crop_y_label)
        self.crop_layout.addWidget(self.crop_y_slider)
        self.crop_width_slider = QSlider(Qt.Horizontal)
        self.crop_width_slider.setRange(0, 100)
        self.crop_width_slider.setValue(100)
        self.crop_width_slider.valueChanged.connect(self.update_crop_width_label)
        self.crop_width_label = QLabel("Crop Width: 100")
        self.crop_layout.addWidget(self.crop_width_label)
        self.crop_layout.addWidget(self.crop_width_slider)
        self.crop_height_slider = QSlider(Qt.Horizontal)
        self.crop_height_slider.setRange(0, 100)
        self.crop_height_slider.setValue(100)
        self.crop_height_slider.valueChanged.connect(self.update_crop_height_label)
        self.crop_height_label = QLabel("Crop Height: 100")
        self.crop_layout.addWidget(self.crop_height_label)
        self.crop_layout.addWidget(self.crop_height_slider)
        self.crop_widget.hide()
        self.layout.addWidget(self.crop_widget)
        self.display_label = QLabel()
        self.layout.addWidget(self.display_label)
        self.process_button = QPushButton("Process")
        self.process_button.clicked.connect(self.process_image)
        self.layout.addWidget(self.process_button)
        self.save_button = QPushButton("Save Image")
        self.save_button.clicked.connect(self.save_image)
        self.layout.addWidget(self.save_button)

    def update_blur_label(self):
        value = self.blur_slider.value()
        self.blur_label.setText(f"Blur Percentage: {value}")

    def update_crop_x_label(self):
        value = self.crop_x_slider.value()
        self.crop_x_label.setText(f"Crop X: {value}")

    def update_crop_y_label(self):
        value = self.crop_y_slider.value()
        self.crop_y_label.setText(f"Crop Y: {value}")

    def update_crop_width_label(self):
        value = self.crop_width_slider.value()
        self.crop_width_label.setText(f"Crop Width: {value}")

    def update_crop_height_label(self):
        value = self.crop_height_slider.value()
        self.crop_height_label.setText(f"Crop Height: {value}")

    def show_effect_options(self, index):
        effect = self.effect_combobox.itemText(index)
        if effect == "Blur":
            self.blur_slider.show()
            self.blur_label.show()
            self.crop_widget.hide()
        elif effect == "Rotate":
            self.blur_slider.hide()
            self.blur_label.hide()
            self.crop_widget.hide()
        elif effect == "Crop":
            self.blur_slider.hide()
            self.blur_label.hide()
            self.crop_widget.show()
        elif effect == "Invers":
            self.blur_slider.hide()
            self.blur_label.hide()
            self.crop_widget.hide()

    def hide_crop_widgets(self):
        self.crop_x_label.hide()
        self.crop_x_slider.hide()
        self.crop_y_label.hide()
        self.crop_y_slider.hide()
        self.crop_width_label.hide()
        self.crop_width_slider.hide()
        self.crop_height_label.hide()
        self.crop_height_slider.hide()

    def show_crop_widgets(self):
        self.crop_x_label.show()
        self.crop_x_slider.show()
        self.crop_y_label.show()
        self.crop_y_slider.show()
        self.crop_width_label.show()
        self.crop_width_slider.show()
        self.crop_height_label.show()
        self.crop_height_slider.show()

    def apply_blur(self):
        if self.image is None or len(self.image) == 0:
            QMessageBox.critical(self, "Error", "No image loaded!")
            return
        blur_percent = self.blur_slider.value()
        if blur_percent <= 0:
            QMessageBox.critical(self, "Error", "Please enter a positive blur percentage!")
            return
        elif blur_percent > 100:
            QMessageBox.critical(self, "Error", "Blur percentage cannot exceed 100!")
            return
        blur_radius = int(blur_percent * 0.1)
        if blur_radius <= 0:
            QMessageBox.critical(self, "Error", "Blur radius must be positive!")
            return
        try:
            self.processed_image = cv2.blur(self.image, (blur_radius, blur_radius))
        except cv2.error as e:
            QMessageBox.critical(self, "Error", f"Failed to apply blur: {str(e)}")
            return
        medium_size = medium_size = (300, 300)
        self.processed_image = cv2.resize(self.processed_image, medium_size)
        self.show_processed_image(self.processed_image)

    def apply_rotate(self):
        if self.image is None or len(self.image) == 0:
            QMessageBox.critical(self, "Error", "No image loaded!")
            return
        if self.processed_image is None:
            self.angle = 90
        else:
            self.angle += 90
        self.angle %= 360
        (h, w) = self.image.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, self.angle, 1.0)
        self.processed_image = cv2.warpAffine(self.image, matrix, (w, h))
        medium_size = (300, 300)
        self.processed_image = cv2.resize(self.processed_image, medium_size)
        self.show_processed_image(self.processed_image)

    def apply_crop(self):
        if self.image is None or len(self.image) == 0:
            QMessageBox.critical(self, "Error", "No image loaded!")
            return
        original_height, original_width = self.image.shape[:2]
        display_width = self.display_label.width()
        display_height = self.display_label.height()
        x = self.crop_x_slider.value() * original_width // display_width
        y = self.crop_y_slider.value() * original_height // display_height
        width = self.crop_width_slider.value() * original_width // display_width
        height = self.crop_height_slider.value() * original_height // display_height
        if x < 0 or y < 0 or width <= 0 or height <= 0 or x + width > original_width or y + height > original_height:
            error_message = "Invalid crop parameters: "
            if x < 0:
                error_message += "X coordinate cannot be negative. "
            if y < 0:
                error_message += "Y coordinate cannot be negative. "
            if width <= 0:
                error_message += "Width must be greater than zero. "
            if height <= 0:
                error_message += "Height must be greater than zero. "
            if x + width > original_width:
                error_message += "X coordinate + Width exceeds image width. "
            if y + height > original_height:
                error_message += "Y coordinate + Height exceeds image height. "
            QMessageBox.critical(self, "Error", error_message.strip())
            return
        self.processed_image = self.image[y:y + height, x:x + width]
        if self.processed_image is None:
            QMessageBox.critical(self, "Error", "Crop operation failed!")
            return
        medium_size = (300, 300)
        self.processed_image = cv2.resize(self.processed_image, medium_size)
        self.show_processed_image(self.processed_image)

    def apply_invers(self):
        if self.image is None or len(self.image) == 0:
            QMessageBox.critical(self, "Error", "No image loaded!")
            return
        try:
            self.processed_image = cv2.bitwise_not(self.image)
        except cv2.error as e:
            QMessageBox.critical(self, "Error", f"Failed to apply invers: {str(e)}")
            return
        medium_size = (300, 300)
        self.processed_image = cv2.resize(self.processed_image, medium_size)
        self.show_processed_image(self.processed_image)

    def show_processed_image(self, processed_image):
        height, width, channel = processed_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(processed_image.data, width, height, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_image)
        self.display_label.setPixmap(pixmap)

    def process_image(self):
        effect = self.effect_combobox.currentText()
        if effect == "Blur":
            self.apply_blur()
        elif effect == "Rotate":
            self.apply_rotate()
        elif effect == "Crop":
            self.apply_crop()
        elif effect == "Invers":
            self.apply_invers()

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.jpg *.jpeg *.png *.bmp)")
        if file_path:
            self.image = cv2.imread(file_path)
            medium_size = (300, 300)
            self.image = cv2.resize(self.image, medium_size)
            self.show_processed_image(self.image)

    def save_image(self):
        if self.processed_image is not None:
            target_width, target_height = 930, 620
            resized_image = cv2.resize(self.processed_image, (target_width, target_height))
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Image Files (*.jpg *.jpeg *.png *.bmp)")
            if file_path:
                cv2.imwrite(file_path, resized_image)
                QMessageBox.information(self, "Success", "Image saved successfully!")
        else:
            QMessageBox.critical(self, "Error", "No processed image to save!")

if __name__ == "__main__":
    prints(panel(f"[!] Menjalankan Aplikasi!. \n[%] Developed by Tiann Dev", title="[green]Success[/]", style="bold white"))
    app = QApplication(sys.argv)
    window = ImageProcessorApp()
    window.show()
    sys.exit(app.exec_())