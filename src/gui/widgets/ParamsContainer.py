from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from gui.widgets.ImageContainer import ImageContainer

class ParamsContainer(QWidget):
    """
    Widżet odpowiadający za obliczanie parametrów ROI sczytanych z widżetu ImageContainer.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Parametry"))
        layout.addWidget(QPushButton("Parametry"))
