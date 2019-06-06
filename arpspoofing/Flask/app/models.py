from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db
from app import login
from sqlalchemy.orm import relationship
import datetime

@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    number = db.Column(db.String, index=True, unique=True) # Lo ponemos como string, pero es un numero
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Account {}>'.format(self.amount)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    accounts = relationship("Account")
    transactions = relationship("Movement")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    receiver = db.Column(db.String)
    reason = db.Column(db.String)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    amount = db.Column(db.Float)

    def __repr__(self):
        return '<Movement {}>'.format(self.id)