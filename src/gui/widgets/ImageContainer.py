from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QRect, QPoint
import pydicom
import numpy as np


class ImageLabel(QLabel):
    """
    QLabel z obsługą rysowania prostokątów ROI.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rois = []  
        self.current_roi = None  
        self.start_point = None  
        self.pixel_array = None  

    def paintEvent(self, event):
        """
        Rysuje obraz i prostokąty ROI.
        """
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.red, 2)
        painter.setPen(pen)

        for rect, roi_stats in self.rois:
            painter.drawRect(rect)
            text_position = QPoint(rect.x() + rect.width() + 5, rect.y() + 10)
            painter.drawText(text_position, roi_stats)

        if self.current_roi:
            painter.drawRect(self.current_roi)

    def mousePressEvent(self, event):
        """
        Obsługa kliknięcia myszy.
        """
        if event.button() == Qt.LeftButton:
            self.start_point = event.pos()
            self.current_roi = None
        elif event.button() == Qt.RightButton:
            self.remove_roi(event.pos())
        self.update()

    def mouseMoveEvent(self, event):
        """
        Obsługa przeciągania myszy.
        """
        if event.buttons() == Qt.LeftButton and self.start_point:
            end_point = event.pos()
            self.current_roi = QRect(self.start_point, end_point).normalized()
            self.update()

    def mouseReleaseEvent(self, event):
        """
        Obsługa zwolnienia przycisku myszy.
        """
        if event.button() == Qt.LeftButton and self.current_roi:
            roi_stats = self.calculate_roi_stats(self.current_roi)
            self.rois.append((self.current_roi, roi_stats))
            self.current_roi = None
            self.start_point = None
            self.update()

    def remove_roi(self, point):
        """
        Usuwa ROI, jeśli kliknięto prawym przyciskiem w jego obszarze.
        """
        for rect, _ in self.rois:
            if rect.contains(point):
                self.rois.remove((rect, _))
                self.update()
                break

    def calculate_roi_stats(self, rect):
        """
        Oblicza statystyki dla zaznaczonego obszaru ROI.
        """
        if self.pixel_array is None:
            return "Brak danych"

        label_width = self.width()
        label_height = self.height()
        pixmap_width = self.pixmap().width()
        pixmap_height = self.pixmap().height()

        scale_x = self.pixel_array.shape[1] / pixmap_width
        scale_y = self.pixel_array.shape[0] / pixmap_height

        x1 = int(rect.x() * scale_x)
        y1 = int(rect.y() * scale_y)
        x2 = int((rect.x() + rect.width()) * scale_x)
        y2 = int((rect.y() + rect.height()) * scale_y)

        cropped_array = self.pixel_array[y1:y2, x1:x2]

        if cropped_array.size > 0:
            min_val = np.min(cropped_array)
            max_val = np.max(cropped_array)
            mean_val = np.mean(cropped_array)
            std_dev = np.std(cropped_array)
            return f"MIN: {min_val}, MAX: {max_val}, AVG: {mean_val:.2f}, STD: {std_dev:.2f}"
        return "Brak danych"


class ImageContainer(QWidget):
    """
    Widżet odpowiadający za wyświetlenie obrazu DICOM z możliwością zaznaczania ROI.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

        self.pixel_array = None  

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.image_label = ImageLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: none;")
        layout.addWidget(self.image_label)

    def display_dicom(self, file_path):
        """
        Wyświetla obraz DICOM w QLabel.
        """
        try:
            ds = pydicom.dcmread(file_path)
            pixel_array = ds.pixel_array
            self.pixel_array = pixel_array  
            self.image_label.pixel_array = pixel_array  
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
        self.image_label.update()  
