from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from gui.widgets.DirectoryTreeContainer import DirectoryTreeContainer

class ImageContainer(QWidget):
    """
    Widżet odpowiadający za wyświetlenie obrazu Dicom i możliwość zaznaczenia na nim ROI 
    (dane pobierane z DirectoryTreeContainer)
    (chyba zaznaczanie ROI zrobimy tutaj a dane przekażemy do params)
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Kolumna 2"))
        layout.addWidget(QPushButton("Przycisk 2"))
