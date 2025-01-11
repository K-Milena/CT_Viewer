from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,
    QListWidget, QHBoxLayout, QMessageBox, QScrollArea
)
from PyQt5.QtCore import Qt


class DirectoryTreeContainer(QWidget):
    """
    Widżet odpowiadający za możliwość wyboru katalogu i przegądanego pliku z woluminu Dicom. 
    (może umożliwienie przewijania za pomocą przycisków i strzałek?)
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Przeglądarka woluminu DICOM")
        layout = QVBoxLayout(self)

        self.folder_label = QLabel("Nie wybrano folderu")
        self.folder_label.setWordWrap(True)  
        layout.addWidget(self.folder_label)

        self.select_folder_btn = QPushButton("Wybierz folder")
        self.select_folder_btn.clicked.connect(self.select_folder)
        layout.addWidget(self.select_folder_btn)

        self.file_list = QListWidget()
        self.file_list.setSelectionMode(QListWidget.SingleSelection)
        self.file_list.itemClicked.connect(self.load_file)
        layout.addWidget(self.file_list)

        self.preview_label = QLabel("Podgląd pliku")
        self.preview_label.setAlignment(Qt.AlignCenter)
        self.preview_label.setStyleSheet("border: 1px solid black;")
        layout.addWidget(self.preview_label)

    def select_folder(self):
        """
        Obsługa wyboru folderu zawierającego pliki DICOM.
        """
        folder_path = QFileDialog.getExistingDirectory(self, "Wybierz folder z plikami DICOM")
        if folder_path:
            self.folder_label.setText(f"Wybrany folder: {folder_path}")
            self.populate_file_list(folder_path)

    def populate_file_list(self, folder_path):
        """
        Wyświetla listę plików DICOM w wybranym folderze.
        """
        self.file_list.clear()
        try:
            files = [f for f in os.listdir(folder_path) if f.lower().endswith(".dcm")]
            if files:
                self.file_list.addItems(files)
            else:
                QMessageBox.warning(self, "Brak plików", "Nie znaleziono plików DICOM w wybranym folderze.")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie udało się odczytać zawartości folderu: {e}")

    def load_file(self, item):
        """
        Obsługa ładowania pliku po jego kliknięciu na liście.
        """
        file_name = item.text()
        self.preview_label.setText(f"Wybrano plik: {file_name}")
        #  kod do wczytania i wyswietlenia zawartości pliku dicom