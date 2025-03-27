from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Model użytkownika
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    
    # Relacja do ulubionych szachistów
    favorite_players = db.relationship('FavoritePlayer', backref='user', lazy=True)

# Model turnieju
class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    details = db.Column(db.String(500), nullable=True)
    rounds_info = db.Column(db.String(500), nullable=True)

# Model profilu szachisty
class PlayerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(500), nullable=True)
    ranking = db.Column(db.Integer, nullable=False)

    # Relacja do ulubionych – sprawdzanie, kto dodał do ulubionych
    favorited_by = db.relationship('FavoritePlayer', backref='player', lazy=True)

# Model do ulubionych szachistów
class FavoritePlayer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('player_profile.id'), nullable=False)
