# ismed2024Z_zad2_Kuna_Franczuk - Wizualizacja danych z tomografii komputerowej (CT) w postaci obrazów planarnych

Oprogramowanie musi umożliwiać ładowanie zbioru plików DICOM pochodzących z pojedynczego badania CT  (pozwalając  na nawigacją pomiędzy seriami i skanami), regulację okna diagnostycznego (szerokości i położenia jego środka) oraz zaznaczania na obrazie jednego obszaru ROI, dla którego wyświetlane są statystyki: wartość średnia, odchylenie standardowe i rozmiar w mm2 (po skalowaniu zgodnie z danymi zapisanymi w DICOM).  

(Zbiór danych: wolumin CT w formacie DICOM.)

## Wymagania

Program ma być wyposażony w graficzny interfejs użytkownika i realizować założenia projektowe bez 
zbędnych „wodotrysków”. GUI aplikacji można zrealizować przy użyciu dowolnej biblioteki, np. Tkinter, 
PyQT/PySide, PyGTK, wxPython. 

• Musi zostać napisany w języku Python 3, a uruchomienie go powinno być możliwe na dowolnym systemie operacyjnym (należy go sprawdzić zarówno pod Windows, jak i pod systemem Linux lub macOS). Dla wybranych tematów wskazano zbiory danych, na których projekty powinny działać. 

• W repozytorium należy umieścić instrukcję, opisującą w jaki sposób uruchomić program, co jest potrzebne do jego działania oraz jakich używa pakietów dodatkowych (pliki requierments.txt lub environment.yml). Ponadto kod źródłowy programu powinien być oparzony komentarzami dokumentującymi typu docstring 
(https://realpython.com/documenting-python-code/). 

• Należy dbać o stosowanie odpowiednich typów danych (w tym również definiować własne klasy) oraz rodzajów kolekcji do ich przechowywania. Istotne jest też właściwe podzielenie kodu na funkcje i moduły. 

### Termin oddania; 19.01.2025

## Jak uruchomić?

1. Sklonuj repozytorium.
2. Zainstaluj zależności: `pip install -r requirements.txt`
3. Uruchom program:

```bash
python main.py
```

### Instrukcja obsługi
1. Załaduj wolumin CT kilkając w "Wybierz folder".
2. Po wybraniu folderu, nawiguj skany po lewej stronie, klikając myszką na docelowy plik.
3. Zaznacz prostokąt ROI przeciągając myszką naciskając lewy przycisk i odczytaj dane.