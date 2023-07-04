from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/intersection', methods=['GET', 'POST'])
def intersection():
    # Pobranie danych z formularza
    x1 = request.form['x1']  # Pobranie współrzędnej x dla pierwszego punktu
    y1 = request.form['y1']  # Pobranie współrzędnej y dla pierwszego punktu
    x2 = request.form['x2']  # Pobranie współrzędnej x dla drugiego punktu
    y2 = request.form['y2']  # Pobranie współrzędnej y dla drugiego punktu
    x3 = request.form['x3']  # Pobranie współrzędnej x dla trzeciego punktu
    y3 = request.form['y3']  # Pobranie współrzędnej y dla trzeciego punktu
    x4 = request.form['x4']  # Pobranie współrzędnej x dla czwartego punktu
    y4 = request.form['y4']  # Pobranie współrzędnej y dla czwartego punktu

    # Sprawdzenie, czy żadne pole nie jest puste
    if not x1 or not y1 or not x2 or not y2 or not x3 or not y3 or not x4 or not y4:
        return render_template('error2.html')  # Renderowanie szablonu 'error2.html' w przypadku pustego pola

    # Konwersja na liczby zmiennoprzecinkowe
    x1 = float(x1)  # Konwersja współrzędnej x pierwszego punktu na liczbę zmiennoprzecinkową
    y1 = float(y1)  # Konwersja współrzędnej y pierwszego punktu na liczbę zmiennoprzecinkową
    x2 = float(x2)  # Konwersja współrzędnej x drugiego punktu na liczbę zmiennoprzecinkową
    y2 = float(y2)  # Konwersja współrzędnej y drugiego punktu na liczbę zmiennoprzecinkową
    x3 = float(x3)  # Konwersja współrzędnej x trzeciego punktu na liczbę zmiennoprzecinkową
    y3 = float(y3)  # Konwersja współrzędnej y trzeciego punktu na liczbę zmiennoprzecinkową
    x4 = float(x4)  # Konwersja współrzędnej x czwartego punktu na liczbę zmiennoprzecinkową
    y4 = float(y4)  # Konwersja współrzędnej y czwartego punktu na liczbę zmiennoprzecinkową

    # Obliczenie punktu przecięcia
    pxr, pyr = calculate_intersection(x1, y1, x2, y2, x3, y3, x4, y4)  # Wywołanie funkcji calculate_intersection

    if pxr == 'None' and pyr == 'None':
        plt.plot([x1, x2], [y1, y2], label='Odcinek 1')  # Dodanie odcinka 1 do wykresu
        plt.plot([x3, x4], [y3, y4], label='Odcinek 2')  # Dodanie odcinka 2 do wykresu
        plt.plot(x1, y1, 'bo', label='Punkt A')  # Dodanie punktu A do wykresu
        plt.plot(x2, y2, 'bo', label='Punkt B')  # Dodanie punktu B do wykresu
        plt.plot(x3, y3, 'go', label='Punkt C')  # Dodanie punktu C do wykresu
        plt.plot(x4, y4, 'go', label='Punkt D')  # Dodanie punktu D do wykresu
        plt.legend()  # Dodanie legendy do wykresu
        plt.grid(color='grey', linestyle='-', linewidth=0.3)
        plt.savefig('static/plot.png', dpi=200)  # Zapisanie wykresu w pliku 'plot.png'
        plt.close()  # Zamknięcie wykresu
        return render_template('error.html')  # Renderowanie szablonu 'error.html' w przypadku braku punktu przecięcia
    if pxr=='infinite' and pyr =='infinite':
        starting_point, ending_point = check_collinear_points(x1, y1, x2, y2, x3, y3, x4, y4)
        plt.plot([x1, x2], [y1, y2], label='Odcinek 1')  # Dodanie odcinka 1 do wykresu
        plt.plot([x3, x4], [y3, y4], label='Odcinek 2')  # Dodanie odcinka 2 do wykresu
        plt.plot(x1, y1, 'bo', label='Punkt A')  # Dodanie punktu A do wykresu
        plt.plot(x2, y2, 'bo', label='Punkt B')  # Dodanie punktu B do wykresu
        plt.plot(x3, y3, 'go', label='Punkt C')  # Dodanie punktu C do wykresu
        plt.plot(x4, y4, 'go', label='Punkt D')  # Dodanie punktu D do wykresu
        plt.legend()  # Dodanie legendy do wykresu
        plt.grid(color='grey', linestyle='-', linewidth=0.3)
        plt.savefig('static/plot.png', dpi=200)  # Zapisanie wykresu w pliku 'plot.png'
        plt.close()  # Zamknięcie wykresu
        return render_template('wspolliniowe.html', starting_point=starting_point, ending_point=ending_point)  # Renderowanie szablonu 'wspoliniowe.html' w przypadku nieskonczonych punktow przeciecia
    else:
        plt.plot([x1, x2], [y1, y2], label='Odcinek 1')  # Dodanie odcinka 1 do wykresu
        plt.plot([x3, x4], [y3, y4], label='Odcinek 2')  # Dodanie odcinka 2 do wykresu
        plt.plot(pxr, pyr, 'ro', label='Punkt przecięcia', zorder=10)  # Dodanie punktu przecięcia do wykresu
        plt.plot(x1, y1, 'bo', label='Punkt A')  # Dodanie punktu A do wykresu
        plt.plot(x2, y2, 'bo', label='Punkt B')  # Dodanie punktu B do wykresu
        plt.plot(x3, y3, 'go', label='Punkt C')  # Dodanie punktu C do wykresu
        plt.plot(x4, y4, 'go', label='Punkt D')  # Dodanie punktu D do wykresu
        plt.legend()  # Dodanie legendy do wykresu
        plt.grid(color='grey', linestyle='-', linewidth=0.3)
        plt.savefig('static/plot.png', dpi=200)  # Zapisanie wykresu w pliku 'plot.png'
        plt.close()  # Zamknięcie wykresu

        return render_template('intersection.html', px=pxr, py=pyr)  # Renderowanie szablonu 'intersection.html' z danymi punktu przecięcia

def calculate_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    # Obliczanie współrzędnych punktu przecięcia dwóch odcinków
    A1 = y2 - y1  # Obliczanie współczynnika A1
    B1 = x1 - x2  # Obliczanie współczynnika B1
    C1 = A1 * x1 + B1 * y1  # Obliczanie współczynnika C1

    A2 = y4 - y3  # Obliczanie współczynnika A2
    B2 = x3 - x4  # Obliczanie współczynnika B2
    C2 = A2 * x3 + B2 * y3  # Obliczanie współczynnika C2

    denominator = A1 * B2 - A2 * B1  # Obliczanie mianownika

    if denominator == 0:
        # Sprawdzenie, czy odcinki są współliniowe
       if (A1 * x3 + B1 * y3 - C1) == 0:
            # Odcinki są współliniowe

            # Sprawdzenie, czy odcinki stykają się tylko krańcami
            if (x1 == x3 and y1 == y3) or (x1 == x4 and y1 == y4):
                return x1, y1  # Zwróć punkt styku

            if (x2 == x3 and y2 == y3) or (x2 == x4 and y2 == y4):
                return x2, y2  # Zwróć punkt styku
            if max(x1, x2) < min(x3, x4) or max(x3, x4) < min(x1, x2) or max(y1, y2) < min(y3, y4) or max(y3, y4) < min(y1, y2):
                return 'None', 'None'
            return 'infinite', 'infinite'

    if denominator == 0:
        # Sprawdzenie, czy odcinki są współliniowe
        if (A1 * x3 + B1 * y3 - C1) == 0:
            # Odcinki są współliniowe
            # Sprawdzenie, czy istnieje część wspólna
            
            if max(x1, x2) < min(x3, x4) or max(x3, x4) < min(x1, x2) or max(y1, y2) < min(y3, y4) or max(y3, y4) < min(y1, y2):
                return 'None', 'None'
            else:
                # Znaleziono część wspólną - zwróć punkt leżący na danym odcinku
                dx1 = x2 - x1
                dy1 = y2 - y1
                dx2 = x4 - x3
                dy2 = y4 - y3

                d1 = (dx1 ** 2 + dy1 ** 2) ** 0.5
                d2 = (dx2 ** 2 + dy2 ** 2) ** 0.5

                t1 = ((x3 - x1) * dx1 + (y3 - y1) * dy1) / (d1 ** 2)
                t2 = ((x4 - x1) * dx1 + (y4 - y1) * dy1) / (d1 ** 2)

                if 0 <= t1 <= 1:
                    x = x1 + t1 * dx1
                    y = y1 + t1 * dy1
                    return x, y

                if 0 <= t2 <= 1:
                    x = x1 + t2 * dx1
                    y = y1 + t2 * dy1
                    return x, y
                    

                return 'None', 'None'
        else:
            # Odcinki są równoległe lub nie mają punktu przecięcia
            return 'None', 'None'
    else:
        px = (B2 * C1 - B1 * C2) / denominator
        py = (A1 * C2 - A2 * C1) / denominator

        # Sprawdzenie, czy punkt przecięcia należy do odcinków
        if min(x1, x2) <= px <= max(x1, x2) and min(y1, y2) <= py <= max(y1, y2) and min(x3, x4) <= px <= max(x3, x4) and min(y3, y4) <= py <= max(y3, y4):
            pxr = round(px, 2)  # Zaokrąglenie współrzędnej x punktu przecięcia do dwóch miejsc po przecinku
            pyr = round(py, 2)  # Zaokrąglenie współrzędnej y punktu przecięcia do dwóch miejsc po przecinku
            return pxr, pyr  # Zwrócenie zaokrąglonych współrzędnych punktu przecięcia
        else:
            return 'None', 'None'  # Zwrócenie informacji o braku punktu przecięcia
        

def check_collinear_points(x1, y1, x2, y2, x3, y3, x4, y4):
    # Sprawdzenie i zamiana kolejności punktów, aby zachować porządek x1 <= x2 i x3 <= x4
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    if x3 > x4:
        x3, x4 = x4, x3
        y3, y4 = y4, y3

    # Obliczenie współczynników A, B i C dla równań prostych przechodzących przez punkty (x1, y1), (x2, y2) i (x3, y3), (x4, y4)
    A1 = y2 - y1
    B1 = x1 - x2
    C1 = A1 * x1 + B1 * y1

    A2 = y4 - y3
    B2 = x3 - x4

    # Obliczenie mianownika równania, który jest różny od zera, jeśli proste są niezależne
    denominator = A1 * B2 - A2 * B1

    # Sprawdzenie, czy proste są równoległe i mają te same równania (punkt wspólny)
    if denominator == 0 and (A1 * x3 + B1 * y3 - C1) == 0:
        # Obliczenie kierunku linii prostych
        line_direction, _ = np.polyfit([x1, x2], [y1, y2], 1)
        
        # Wybór punktów początkowych i końcowych w zależności od kierunku linii
        if x1 == x2:  # Pionowa linia
            starting_x_point = round(x1, 2)
            y_cords = sorted([y1, y2, y3, y4])
            starting_y_point = y_cords[1]
            ending_x_point = x1
            ending_y_point = y_cords[-2]
        elif line_direction > 0:  # Linia rosnąca
            starting_x_point = round(max(x1, x3), 2)
            starting_y_point = round(max(y1, y3), 2)
            ending_x_point = round(min(x2, x4), 2)
            ending_y_point = round(min(y2, y4), 2)
        elif line_direction < 0:  # Linia malejąca
            starting_x_point = round(max(x1, x3), 2)
            starting_y_point = round(min(y1, y3), 2)
            ending_x_point = round(min(x2, x4), 2)
            ending_y_point = round(max(y2, y4), 2)
        else:  # Pozioma linia
            starting_x_point = round(max(x1, x3))
            starting_y_point = y1
            ending_x_point = min(x2, x4)
            ending_y_point = y2

        return (starting_x_point, starting_y_point), (ending_x_point, ending_y_point)

if __name__ == '__main__':
    app.run(debug=True)