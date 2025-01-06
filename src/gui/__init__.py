#from widgets import DirectoryTreeContainer, ImageContainer, ParamsContainer
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QSplitter
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('CT Dicom')
        self.setGeometry(100, 100, 800, 600)

        # Główne okno kontenerowe
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Układ dla głównego okna
        layout = QHBoxLayout()

        # Tworzenie QSplitter
        splitter = QSplitter(Qt.Horizontal)

        # Directory tree container (kolumna 1)
        col1 = QWidget()
        col1_layout = QVBoxLayout(col1)
        col1_layout.addWidget(QLabel("Kolumna 1"))
        col1_layout.addWidget(QPushButton("Przycisk 1"))

        # Image Container (kolumna 2)
        col2 = QWidget()
        col2_layout = QVBoxLayout(col2)
        col2_layout.addWidget(QLabel("Kolumna 2"))
        col2_layout.addWidget(QPushButton("Przycisk 2"))

        # Params container (kolumna 3)
        col3 = QWidget()
        col3_layout = QVBoxLayout(col3)
        col3_layout.addWidget(QLabel("Kolumna 3"))
        col3_layout.addWidget(QPushButton("Przycisk 3"))

        # Dodanie kolumn do QSplitter
        splitter.addWidget(col1)
        splitter.addWidget(col2)
        splitter.addWidget(col3)

        # Minimalne wymiary kolumn
        col1.setMinimumWidth(100)
        col2.setMinimumWidth(300)
        col3.setMinimumWidth(150)

        # Dodanie splitter do głównego układu
        layout.addWidget(splitter)

        # Ustawienie QSplitter jako centralny widget
        main_widget.setLayout(layout)

        # Dodatkowe ustawienia QSplitter
        splitter.setSizes([100, 300, 150])  # Wstępne szerokości dla kolumn