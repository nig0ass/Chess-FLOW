import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Tournament, PlayerProfile, FavoritePlayer

app = Flask(__name__)

# Konfiguracja aplikacji
app.config['SECRET_KEY'] = 'tajnyklucz'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///szachy.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optymalizacja SQLAlchemy

# Inicjalizacja bazy danych
db.init_app(app)

# Inicjalizacja systemu logowania
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Tworzenie tabel przy starcie aplikacji
with app.app_context():
    db.create_all()

# Funkcja do ładowania użytkownika
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Strona główna - przekierowanie do dashboard, jeśli użytkownik jest zalogowany
@app.route('/')
def home():
    return redirect(url_for('dashboard')) if current_user.is_authenticated else redirect(url_for('login'))

# Rejestracja użytkownika
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256')

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template('register.html')

# Logowanie użytkownika
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Błędny login lub hasło', category='error')

    return render_template('login.html')

# Wylogowanie użytkownika
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Panel użytkownika (dashboard)
@app.route('/dashboard')
@login_required
def dashboard():
    tournaments = Tournament.query.all()
    return render_template('dashboard.html', tournaments=tournaments)

# Dodawanie turnieju (admin)
@app.route('/add_tournament', methods=['GET', 'POST'])
@login_required
def add_tournament():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        details = request.form['details']
        rounds_info = request.form['rounds_info']

        new_tournament = Tournament(name=name, date=date, details=details, rounds_info=rounds_info)
        db.session.add(new_tournament)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template('add_tournament.html')

# Profil użytkownika
@app.route('/profile/<int:player_id>')
@login_required
def profile(player_id):
    player = PlayerProfile.query.get_or_404(player_id)
    return render_template('profile.html', player=player)

# Dodawanie szachisty do ulubionych
@app.route('/add_favorite/<int:player_id>', methods=['POST'])
@login_required
def add_favorite(player_id):
    favorite = FavoritePlayer(user_id=current_user.id, player_id=player_id)
    db.session.add(favorite)
    db.session.commit()
    return redirect(url_for('profile', player_id=player_id))

# Lista ulubionych szachistów
@app.route('/favorites')
@login_required
def favorites():
    favorite_players = FavoritePlayer.query.filter_by(user_id=current_user.id).all()
    players = [PlayerProfile.query.get(fav.player_id) for fav in favorite_players]
    return render_template('favorite_players.html', favorite_players=players)

# Uruchamianie aplikacji
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Pobiera PORT z env, domyślnie 10000
    app.run(host="0.0.0.0", port=port, debug=True)
