from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    def __repr__(self):
        return '<User %r>' % self.email

class Ttable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return '<Ttable %r>' % self.name

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(300))
    status = db.Column(db.Integer)

    ttable_id = db.Column(db.Integer, db.ForeignKey('ttable.id'),
        nullable=False)
    ttable = db.relationship('Ttable',
        backref=db.backref('tasks', lazy=True))

    def __repr__(self):
        return '<Task %r>' % self.name
