from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class DirectoryTreeContainer(QWidget):
    """
    Widżet odpowiadający za możliwość wyboru katalogu i przegądanego pliku z woluminu Dicom. 
    (może umożliwienie przewijania za pomocą przycisków i strzałek?)
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Kolumna 1"))
        layout.addWidget(QPushButton("Przycisk 1"))
