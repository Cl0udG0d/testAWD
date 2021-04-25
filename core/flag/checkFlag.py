from flask import session

def getSessionTeamFlag():
    session['teamflag']="1"

def checkSessionTeamFlag():
    print(session.get('teamflag'))
    return

if __name__ == '__main__':
    getSessionTeamFlag()
    checkSessionTeamFlag()