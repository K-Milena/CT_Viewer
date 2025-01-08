from gui.widgets.DirectoryTreeContainer import DirectoryTreeContainer
from gui.widgets.ImageContainer import ImageContainer
from gui.widgets.ParamsContainer import ParamsContainer
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QSplitter
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    """
    Główne okno aplikacji, które zawiera QSplitter do podzielenia przestrzeni na 3 kolumny.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle('CT Dicom')
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout()
        splitter = QSplitter(Qt.Horizontal)

        col1 = DirectoryTreeContainer()
        col2 = ImageContainer()
        col3 = ParamsContainer()

        splitter.addWidget(col1)
        splitter.addWidget(col2)
        splitter.addWidget(col3)

        col1.setMinimumWidth(100)
        col2.setMinimumWidth(300)
        col3.setMinimumWidth(150)

        splitter.setSizes([100, 300, 150])

        layout.addWidget(splitter)
        main_widget.setLayout(layout)
