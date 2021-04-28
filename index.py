import json

from flask import request,render_template,redirect,url_for,session
from init import app
from models import *
from operator import attrgetter
from core.flag.saveFlag import authorizationSaveFlag
import os

app.config['SECRET_KEY']=os.urandom(24) #产生24位的随机字符串

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
            session['teamid'] = team1.id
            return redirect(url_for('index'))
        else:
            return render_template('login.html')



@app.route('/login_out/')
def LoginOut():
    if session.get('teamid'):
        session.pop('teamid')
        return redirect(url_for('login'))
    elif session.get('adminid'):
        session.pop('adminid')
        return redirect(url_for('adminLogin'))



@app.route('/EditPassword/',methods=['POST'])
def EditTeamPassword():
    team1=Team.query.filter(Team.id==session.get('teamid')).first()
    if request.form.get('oldpassword') == team1.password:
        team1.password =request.form.get('newpassword')
        db.session.commit()
        return redirect(url_for('LoginOut'))
    else:
        return redirect(url_for('login'))




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
            session['adminid'] = admin1.id
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



@app.route('/rank/')
def Rank():
    source1 = Source.query.order_by(Source.source.desc()).all()
    return render_template('rank.html', source1=source1)

#测试路由
@app.route('/test/')
def test():
    print(request.path)
    return "hi!"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'),500

@app.before_request#执行所有装饰器都要执行当前装饰器(简洁版实现同样功能)
def login_required():
    if request.path in ['/login/','/login_manager/','/index/']: #如果登录的路由是注册和登录就返会none
        return None
    teamid=session.get('teamid') #获取用户登录信息
    #adminid=session.get('adminid')
    if not teamid:                 #没有登录就自动跳转到登录页面去
        return redirect('/login')
    return None

if __name__ == "__main__":
    app.run()