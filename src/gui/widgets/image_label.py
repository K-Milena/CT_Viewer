from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QRect, QPoint
import numpy as np


class ImageLabel(QLabel):
    """
    Widget QLabel rozszerzony o funkcjonalność wyświetlania obrazów DICOM,
    zarządzania regionami zainteresowania (ROI) i regulacji okna diagnostycznego.
    """
    def __init__(self, parent=None):
        """
        Inicjalizuje obiekt ImageLabel.
        """
        super().__init__(parent)
        self.rois = []
        self.current_roi = None
        self.start_point = None
        self.pixel_array = None
        self.pixel_spacing = None
        self.window_center = 0
        self.window_width = 256  
        self.scaled_image = None

    def get_displayed_image_rect(self):
        """
        Oblicza i zwraca prostokąt zajmowany przez obraz w widgetcie.
        """
        if not self.pixmap():
            return QRect()

        label_width, label_height = self.width(), self.height()
        pixmap_width, pixmap_height = self.pixmap().width(), self.pixmap().height()

        scale = min(label_width / pixmap_width, label_height / pixmap_height)
        displayed_width = int(pixmap_width * scale)
        displayed_height = int(pixmap_height * scale)

        offset_x = (label_width - displayed_width) // 2
        offset_y = (label_height - displayed_height) // 2

        return QRect(offset_x, offset_y, displayed_width, displayed_height)

    def update_image(self):
        """
        Aktualizuje wyświetlany obraz na podstawie ustawień okna diagnostycznego.
        """
        if self.pixel_array is None:
            return

        min_intensity = self.window_center - self.window_width / 2
        max_intensity = self.window_center + self.window_width / 2

        scaled_array = np.clip(self.pixel_array, min_intensity, max_intensity)
        scaled_array = ((scaled_array - min_intensity) / (max_intensity - min_intensity) * 255).astype(np.uint8)

        height, width = scaled_array.shape
        image = QImage(scaled_array.data, width, height, width, QImage.Format_Grayscale8)

        self.scaled_image = QPixmap.fromImage(image)
        self.setPixmap(self.scaled_image)

    def paintEvent(self, event):
        """
        Rysuje dodatkowe elementy, takie jak prostokąty ROI i ich statystyki.
        """
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.red, 2)
        painter.setPen(pen)

        for rect, roi_stats in self.rois:
            painter.drawRect(rect)
            stats_lines = roi_stats.split(", ")
            for i, line in enumerate(stats_lines):
                text_position = QPoint(rect.x() + rect.width() + 5, rect.y() + 10 + i * 20)
                painter.drawText(text_position, line)

        if self.current_roi:
            painter.drawRect(self.current_roi)

    def mousePressEvent(self, event):
        """
        Obsługuje kliknięcie myszy w celu rozpoczęcia zaznaczania ROI lub usunięcia ROI.
        """
        if event.button() == Qt.LeftButton:
            displayed_image_rect = self.get_displayed_image_rect()
            if displayed_image_rect.contains(event.pos()):
                self.start_point = event.pos()
                self.current_roi = None
        elif event.button() == Qt.RightButton:
            self.remove_roi(event.pos())
        self.update()

    def mouseMoveEvent(self, event):
        """
        Obsługuje ruch myszy w celu aktualizacji prostokąta ROI podczas zaznaczania.
        """
        if event.buttons() == Qt.LeftButton and self.start_point:
            end_point = event.pos()
            displayed_image_rect = self.get_displayed_image_rect()

            constrained_start = displayed_image_rect.intersected(QRect(self.start_point, self.start_point))
            constrained_end = displayed_image_rect.intersected(QRect(end_point, end_point))

            if not constrained_start.isNull() and not constrained_end.isNull():
                self.current_roi = QRect(constrained_start.topLeft(), constrained_end.bottomRight()).normalized()
            self.update()

    def mouseReleaseEvent(self, event):
        """
        Obsługuje zakończenie zaznaczania ROI i oblicza statystyki dla wybranego obszaru.
        """
        if event.button() == Qt.LeftButton and self.current_roi:
            roi_stats = self.calculate_roi_stats(self.current_roi)
            self.rois.append((self.current_roi, roi_stats))
            self.current_roi = None
            self.start_point = None
            self.update()

    def remove_roi(self, point):
        """
        Usuwa ROI, jeśli kliknięto wewnątrz zaznaczonego obszaru.
        """
        for rect, _ in self.rois:
            if rect.contains(point):
                self.rois.remove((rect, _))
                self.update()
                break

    def calculate_roi_stats(self, rect):
        """
        Oblicza statystyki (min, max, średnia, odchylenie standardowe) dla wybranego ROI.
        """
        if self.pixel_array is None or self.pixel_spacing is None:
            return "Brak danych"

        displayed_image_rect = self.get_displayed_image_rect()
        scale_x = self.pixel_array.shape[1] / displayed_image_rect.width()
        scale_y = self.pixel_array.shape[0] / displayed_image_rect.height()

        x1 = int((rect.x() - displayed_image_rect.x()) * scale_x)
        y1 = int((rect.y() - displayed_image_rect.y()) * scale_y)
        x2 = int((rect.x() + rect.width() - displayed_image_rect.x()) * scale_x)
        y2 = int((rect.y() + rect.height() - displayed_image_rect.y()) * scale_y)

        cropped_array = self.pixel_array[y1:y2, x1:x2]
        if cropped_array.size > 0:
            min_val = np.min(cropped_array)
            max_val = np.max(cropped_array)
            mean_val = np.mean(cropped_array)
            std_dev = np.std(cropped_array)

            pixel_width, pixel_height = self.pixel_spacing
            roi_area_mm2 = (rect.width() * pixel_width) * (rect.height() * pixel_height)

            return f"MIN: {min_val}, MAX: {max_val}, AVG: {mean_val:.2f}, STD: {std_dev:.2f}, Size: {roi_area_mm2:.2f} mm²"
        return "Brak danych"
