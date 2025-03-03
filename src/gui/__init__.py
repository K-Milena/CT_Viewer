from gui.widgets.directory_tree_container import DirectoryTreeContainer
from gui.widgets.image_container import ImageContainer
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QSplitter
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    """
    Główne okno aplikacji.
    """
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Wizualizacja danych z tomografii komputerowej (CT)')

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        layout = QHBoxLayout()
        splitter = QSplitter(Qt.Horizontal)

        self.col1 = DirectoryTreeContainer()
        self.col2 = ImageContainer()

        splitter.addWidget(self.col1)
        splitter.addWidget(self.col2)

        self.col1.setMinimumWidth(100)
        self.col2.setMinimumWidth(500)

        splitter.setSizes([100, 500])

        layout.addWidget(splitter)
        main_widget.setLayout(layout)

        self.col1.file_selected.connect(self.col2.display_dicom)

        self.showMaximized()

    def resizeEvent(self, event):
        """
        Obsługa zmiany rozmiaru okna.
        """
        super().resizeEvent(event)
        self.centralWidget().setMaximumSize(self.size())
