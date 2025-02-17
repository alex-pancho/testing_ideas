from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = Flask(__name__)

# Налаштування бази даних
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # SQLite база даних у файлі app.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Вимикаємо непотрібні повідомлення

# Ініціалізація SQLAlchemy
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(app, model_class=Base)

# Модель таблиці
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Унікальний ідентифікатор
    username = db.Column(db.String(80), nullable=False, unique=True)  # Ім'я користувача
    email = db.Column(db.String(120), nullable=False, unique=True)  # Email користувача

    def __repr__(self):
        return f'<User {self.username}>'

with app.app_context():
    db.create_all()
