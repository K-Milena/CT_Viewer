from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QImage
import pydicom
import numpy as np
from PyQt5.QtCore import Qt


class ImageContainer(QWidget):
    """
    Widżet odpowiadający za wyświetlenie obrazu DICOM.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.image_label = QLabel("Obraz DICOM")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid black;")
        layout.addWidget(self.image_label)

    def display_dicom(self, file_path):
        """
        Wyświetla obraz DICOM w QLabel.
        """
        try:
            ds = pydicom.dcmread(file_path)  # Wczytaj plik DICOM
            pixel_array = ds.pixel_array  # Pobierz dane pikselowe
            image = self.to_qimage(pixel_array)
            pixmap = QPixmap.fromImage(image)
            self.image_label.setPixmap(pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))
        except Exception as e:
            self.image_label.setText(f"Błąd wczytywania: {e}")

    def to_qimage(self, array):
        """
        Konwertuje macierz numpy na QImage.
        """
        normalized_array = (255 * (array - np.min(array)) / (np.max(array) - np.min(array))).astype(np.uint8)
        height, width = normalized_array.shape
        return QImage(normalized_array.data, width, height, width, QImage.Format_Grayscale8)

    def resizeEvent(self, event):
        """
        Skaluj obraz podczas zmiany rozmiaru okna.
        """
        if self.image_label.pixmap():
            self.image_label.setPixmap(self.image_label.pixmap().scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))
