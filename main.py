import sys
import cv2
import numpy as np
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QLabel, QPushButton, QComboBox, QSizePolicy)
from PySide6.QtCore import QTimer, Qt, Slot
from PySide6.QtGui import QImage, QPixmap

from src.camera import Camera
from src.pipeline import process_pipeline
from src.exporter import save_capture

class ScannerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real-Time Document Scanner")
        self.setGeometry(100, 100, 1000, 600)
        
        self.camera = Camera(0)
        
        self.frozen_data = None
        self.is_frozen = False
        
        self.setup_ui()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        # Image views
        views_layout = QHBoxLayout()
        
        # Live view
        self.live_label = QLabel("Live Feed")
        self.live_label.setAlignment(Qt.AlignCenter)
        self.live_label.setStyleSheet("border: 1px solid black;")
        self.live_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.live_label.setMinimumSize(320, 240)
        views_layout.addWidget(self.live_label)
        
        # Scanned view
        self.scan_label = QLabel("Scanned Document")
        self.scan_label.setAlignment(Qt.AlignCenter)
        self.scan_label.setStyleSheet("border: 1px solid black;")
        self.scan_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.scan_label.setMinimumSize(320, 240)
        views_layout.addWidget(self.scan_label)
        
        main_layout.addLayout(views_layout)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.camera_selector = QComboBox()
        self.camera_selector.addItems(["Camera 0", "Camera 1", "Camera 2", "Camera 3"])
        self.camera_selector.currentIndexChanged.connect(self.change_camera)
        controls_layout.addWidget(QLabel("Select Camera:"))
        controls_layout.addWidget(self.camera_selector)
        
        self.btn_capture = QPushButton("Capture Photo")
        self.btn_capture.clicked.connect(self.toggle_capture)
        controls_layout.addWidget(self.btn_capture)
        
        self.btn_save = QPushButton("Save Outputs")
        self.btn_save.clicked.connect(self.save_photo)
        self.btn_save.setEnabled(False)
        controls_layout.addWidget(self.btn_save)
        
        main_layout.addLayout(controls_layout)

    def update_frame(self):
        if self.is_frozen:
            return
            
        frame = self.camera.read_frame()
        if frame is None:
            self.live_label.setText("Error reading camera frame. Trying to reconnect...")
            return
            
        self.frozen_data = process_pipeline(frame)
        
        # Draw corners if found
        display_frame = frame.copy()
        if self.frozen_data['corners'] is not None:
            cv2.drawContours(display_frame, [self.frozen_data['corners'].reshape(-1, 1, 2).astype(int)], -1, (0, 255, 0), 2)
            
        self.set_image(self.live_label, display_frame)
        
        if self.frozen_data['warped'] is not None:
            self.set_image(self.scan_label, self.frozen_data['warped'])
        else:
            self.scan_label.setText("No document detected")
            
    def set_image(self, label, img):
        if img is None:
            return
            
        # Ensure memory is contiguous for PySide6 to read it safely
        img = np.ascontiguousarray(img)
        
        if len(img.shape) == 3:
            h, w, ch = img.shape
            bytes_per_line = ch * w
            img_format = QImage.Format_BGR888
        else:
            h, w = img.shape
            bytes_per_line = w
            img_format = QImage.Format_Grayscale8
            
        q_img = QImage(img.data, w, h, bytes_per_line, img_format)
        label.setPixmap(QPixmap.fromImage(q_img).scaled(label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    @Slot()
    def toggle_capture(self):
        self.is_frozen = not self.is_frozen
        if self.is_frozen:
            self.btn_capture.setText("Resume Camera")
            self.btn_save.setEnabled(True)
        else:
            self.btn_capture.setText("Capture Photo")
            self.btn_save.setEnabled(False)
            
    @Slot()
    def save_photo(self):
        if self.frozen_data:
            saved = save_capture(self.frozen_data)
            print(f"Saved {len(saved)} files.")
            
    @Slot(int)
    def change_camera(self, index):
        self.timer.stop()
        self.camera.open_camera(index)
        self.is_frozen = False
        self.btn_capture.setText("Capture Photo")
        self.btn_save.setEnabled(False)
        self.timer.start(30)

    def closeEvent(self, event):
        self.camera.release()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ScannerApp()
    window.show()
    sys.exit(app.exec())
