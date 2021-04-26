from models import *
from init import app


def editTeamName(tid,newTeamName):
    with app.app_context():
        tempteam = Team.query.filter(Team.id == tid ).first()
        tempteam.teamname=newTeamName
        db.session.commit()
    return

def delTeam(tid):
    with app.app_context():
        tempteam = Team.query.filter(Team.id == tid ).first()
        db.session.delete(tempteam)
        db.session.commit()
    return

