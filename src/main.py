from gui import MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

if __name__ == "__main__":
    """
    Uruchamia aplikację PyQt5 i wyświetla główne okno aplikacji.
    """
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
