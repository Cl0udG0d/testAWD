import json

from flask import request,render_template,redirect,url_for,session
from init import app
from models import *
from operator import attrgetter
from core.flag.saveFlag import authorizationSaveFlag

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        teamname = request.form.get('username')
        password = request.form.get('password')
        #print("{} {}".format(username,password))
        team1 = Team.query.filter(Team.username == teamname).filter(Team.password==password).first()
        #print(user1)
        if team1:
            return redirect(url_for('index'))
        else:
            return render_template('login.html')


@app.route('/login_manager/',methods=['GET','POST'])
def adminLogin():
    if request.method == 'GET':
        return render_template('login_manager.html')
    else:
        adminname = request.form.get('adminname')
        password = request.form.get('password')
        # print("{} {}".format(adminname,password))
        admin1 = Admin.query.filter(Admin.adminname == adminname).filter(Admin.password==password).first()
        if admin1:
            return redirect(url_for('index'))
        else:
            return render_template('login_manager.html')


@app.route('/announcement/')
def notice():
    notice1=Notice.query.filter(Notice.content !=None).order_by(Notice.id.desc()).all()
    # notice1 =sorted(notice1,key=attrgetter('id'),reverse=True)
    for i in notice1:
        print(i.content)
    return render_template('announcement.html',notice1=notice1)

@app.route('/flag',methods=['POST'])
def flag():
    try:
        Authorization=request.headers.get('Authorization')
        flag=json.loads(request.get_data().decode('ascii'))['flag']
        if not Authorization:
            return "need Authorization"
        status=authorizationSaveFlag(flag,Authorization)
        if status==0:
            return "error flag"
        return "you are right!"
    except:
        return "error"

#测试路由
@app.route('/test/')
def test():
    a=1/0
    return "hi!"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'),500
if __name__ == "__main__":
    app.run()