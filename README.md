Chess FLOW

Wydawca: PROGRAMATORIUMVS
Producent: Chess FLOW Team
Właściciel: Blumix

Opis

Chess FLOW to aplikacja webowa umożliwiająca śledzenie turniejów szachowych, śledzenie ulubionych graczy oraz interakcję społeczności szachowej. Aplikacja została zbudowana przy użyciu Flask oraz SQLAlchemy.

Funkcjonalności

- Rejestracja i logowanie użytkowników

- Panel administracyjny do zarządzania turniejami

- Lista turniejów

- Profil użytkownika

- Dodawanie szachistów do ulubionych

Instalacja

Sklonuj repozytorium:

git clone https://github.com/TwojaNazwaRepo/chess-flow.git

Przejdź do katalogu projektu:

cd chess-flow

Stwórz wirtualne środowisko i aktywuj je:

python -m venv venv
source venv/bin/activate  # Na Windows: venv\Scripts\activate

Zainstaluj zależności:

pip install -r requirements.txt

Uruchomienie aplikacji

python app.py

Konfiguracja na Render

W pliku app.py dodaj obsługę portu:

import os
port = int(os.environ.get("PORT", 5000))
app.run(host="0.0.0.0", port=port, debug=True)

W pliku requirements.txt upewnij się, że Flask oraz SQLAlchemy są uwzględnione.

W panelu Rendera ustaw Start Command na:

gunicorn -w 4 -b 0.0.0.0:$PORT app:app

Licencja

Projekt jest objęty licencją MIT.

Kontakt:

Aby zgłośić błędy należy wysłać emaila (najlepiej z zdjęciami lub filmami gdzie znajduje się błąd) na chessflow1@gmail.com  // Błędy w kodzie a nie na stronie należy zgłaszać na email: programatoriumvs@gmail.com
