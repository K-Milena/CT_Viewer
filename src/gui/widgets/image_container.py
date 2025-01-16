from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QGroupBox
from PyQt5.QtCore import Qt
import pydicom
from .image_label import ImageLabel

class ImageContainer(QWidget):
    """
    Kontener do wyświetlania obrazów DICOM z możliwością regulacji okna diagnostycznego
    i obsługą zdarzeń związanych z wyświetlanym obrazem.
    """
    def __init__(self, parent=None):
        """
        Inicjalizuje obiekt ImageContainer.
        """
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """
        Tworzy i konfiguruje elementy interfejsu użytkownika, w tym suwaki do regulacji okna diagnostycznego
        oraz komponent do wyświetlania obrazu.
        """
        layout = QVBoxLayout(self)

        self.window_center_slider = QSlider(Qt.Horizontal)
        self.window_width_slider = QSlider(Qt.Horizontal)

        self.window_center_slider.setRange(-1024, 2048)
        self.window_width_slider.setRange(1, 2048)

        self.window_center_slider.setValue(0)
        self.window_width_slider.setValue(256)

        self.window_center_slider.valueChanged.connect(self.update_windowing)
        self.window_width_slider.valueChanged.connect(self.update_windowing)

        windowing_layout = QHBoxLayout()
        windowing_layout.addWidget(QLabel("Położenie środka"))
        windowing_layout.addWidget(self.window_center_slider)
        windowing_layout.addWidget(QLabel("Szerokość"))
        windowing_layout.addWidget(self.window_width_slider)

        windowing_group = QGroupBox("Dopasuj okno")
        windowing_group.setLayout(windowing_layout)
        windowing_group.setFixedHeight(80)  
        layout.addWidget(windowing_group)

        self.image_label = ImageLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("border: none;")
        layout.addWidget(self.image_label)

    def display_dicom(self, file_path):
        """
        Wczytuje plik DICOM, wyodrębnia macierz pikseli oraz informacje o rozdzielczości
        i przekazuje je do komponentu wyświetlającego obraz.
        """
        try:
            ds = pydicom.dcmread(file_path)
            pixel_array = ds.pixel_array
            self.image_label.pixel_array = pixel_array
            self.image_label.pixel_spacing = ds.PixelSpacing
            self.image_label.update_image()

            if self.image_label.pixmap():
                self.image_label.setPixmap(self.image_label.pixmap().scaled(
                    self.image_label.size(),
                    Qt.KeepAspectRatio,
                    Qt.SmoothTransformation
                ))
            self.image_label.update()
        except Exception as e:
            self.image_label.setText(f"Błąd wczytywania: {e}")

    def update_windowing(self):
        """
        Aktualizuje wartości środka i szerokości okna diagnostycznego
        oraz odświeża wyświetlany obraz.
        """
        self.image_label.window_center = self.window_center_slider.value()
        self.image_label.window_width = self.window_width_slider.value()
        self.image_label.update_image()

    def resizeEvent(self, event):
        """
        Obsługuje zdarzenie zmiany rozmiaru widgetu i odpowiednio skaluje wyświetlany obraz.
        """
        if self.image_label.pixmap():
            self.image_label.setPixmap(self.image_label.pixmap().scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            ))
        self.image_label.update()
