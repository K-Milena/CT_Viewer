from gui.widgets.DirectoryTreeContainer import DirectoryTreeContainer
from gui.widgets.ImageContainer import ImageContainer
from gui.widgets.ParamsContainer import ParamsContainer
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QSplitter
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    """
    Główne okno aplikacji.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle('CT Dicom')
        self.setGeometry(100, 100, 800, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout()
        splitter = QSplitter(Qt.Horizontal)

        self.col1 = DirectoryTreeContainer()
        self.col2 = ImageContainer()
        # self.col3 = ParamsContainer()

        splitter.addWidget(self.col1)
        splitter.addWidget(self.col2)
        # splitter.addWidget(self.col3)

        self.col1.setMinimumWidth(100)
        self.col2.setMinimumWidth(300)
        # self.col3.setMinimumWidth(150)

        splitter.setSizes([100, 300])

        layout.addWidget(splitter)
        main_widget.setLayout(layout)


        self.col1.file_selected.connect(self.col2.display_dicom)
        
    def resizeEvent(self, event):
        """
        Obsługa zmiany rozmiaru okna.
        """
        super().resizeEvent(event)
        self.centralWidget().setMaximumSize(self.size())


