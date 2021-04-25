from datetime import datetime

from exts import db

class User (db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(128),nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Admin (db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    adminname = db.Column(db.String(128),nullable=False)
    password = db.Column(db.String(128), nullable=False)


class Notice (db.Model):
    __tablename__ = 'notice'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
