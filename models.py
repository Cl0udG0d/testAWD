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
    cansee=db.Column(db.Boolean,nullable=False,default=False)
    vulname=db.Column(db.String(128),nullable=False)
    addr = db.Column(db.String(64), nullable=False)
    serviceport = db.Column(db.String(64), nullable=False)
    sshport=db.Column(db.Integer, nullable=False)
    sshname = db.Column(db.String(128), nullable=False)
    sshpass = db.Column(db.String(128), nullable=False)
    dockerid = db.Column(db.String(128), nullable=False)
    status=db.Column(db.Boolean,nullable=False,default=True)
    detail=db.Column(db.Text)

class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    ischeck = db.Column(db.Boolean, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

class ULog(db.Model):
    __tablename__ = 'ulog'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(128), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

class Time(db.Model):
    __tablename__='time'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timeNow = db.Column(db.Integer, nullable=False,default=0)

class Game(db.Model):
    __tablename__='game'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    gametitle=db.Column(db.String(128), nullable=False)
    starttime=db.Column(db.String(128))
    endtime=db.Column(db.String(128))
    is_start=db.Column(db.Boolean, nullable=False,default=False)
    is_end=db.Column(db.Boolean, nullable=False,default=False)