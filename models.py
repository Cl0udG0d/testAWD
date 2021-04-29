from datetime import datetime

from exts import db


class Admin (db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    adminname = db.Column(db.String(128),nullable=False)
    password = db.Column(db.String(128), nullable=False)


class Notice (db.Model):
    __tablename__ = 'notice'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title=db.Column(db.String(128),nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

class Flag(db.Model):
    __tablename__='flag'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    tid=db.Column(db.Integer, nullable=False)
    flag=db.Column(db.String(128),nullable=False)

class Source(db.Model):
    __tablename__='source'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tid = db.Column(db.Integer, nullable=False)
    source=db.Column(db.Integer, nullable=False)

class AttackRecord(db.Model):
    __tablename__='attackrecord'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    sourcetid=db.Column(db.Integer, nullable=False)
    goaltid=db.Column(db.Integer, nullable=False)
    round=db.Column(db.Integer, nullable=False)

class Team(db.Model):
    __tablename__='team'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    teamname=db.Column(db.String(128),nullable=False)
    password=db.Column(db.String(128),nullable=False)
    token=db.Column(db.String(128),nullable=False)

class Vulhub(db.Model):
    __tablename__='vulhub'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tid=db.Column(db.Integer, nullable=False)
    title=db.Column(db.String(128),nullable=False)
    sshpass = db.Column(db.String(128), nullable=False)
    status=db.Column(db.Boolean,nullable=False)
    addr=db.Column(db.String(64),nullable=False)
    detail=db.Column(db.Text)

class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    ischeck = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)