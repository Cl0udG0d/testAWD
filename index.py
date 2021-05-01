import json
from flask import request,render_template,redirect,url_for,session
from init import app
from models import *
from core.flag.saveFlag import authorizationSaveFlag
from core.unit.decorators import login_required,admin_login_required

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('K_index.html')

@app.route('/adminIndex', methods=['GET', 'POST'])
def adminIndex():
    return render_template('T_admin_index.html')

@app.route('/loginLog', methods=['GET', 'POST'])
def loginLog():
    return render_template('T_Login_log.html')

@app.route('/useLog', methods=['GET', 'POST'])
def useLog():
    return render_template('T_Operation_Log.html')

@app.route('/teamManage', methods=['GET', 'POST'])
def teamManage():
    return render_template('T_team_manage.html')

@app.route('/noticeManage', methods=['GET', 'POST'])
def noticeManage():
    return render_template('T_notice_manage.html')

@app.route('/flagManage', methods=['GET', 'POST'])
def flagManage():
    return render_template('T_flag_manage.html')

@app.route('/vulhubManage', methods=['GET', 'POST'])
def vulhubManage():
    return render_template('T_vulhub_manage.html')

@app.route('/sysInfo', methods=['GET', 'POST'])
def sysInfo():
    return render_template('T_SysConfig.html')

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
            saveLog(teamname, True)
            session['teamid'] = team1.id
            return redirect(url_for('index'))
        else:
            saveLog(teamname, False)
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
            saveLog(adminname, True)
            session['adminid'] = admin1.id
            return redirect(url_for('index'))
        else:
            saveLog(adminname, False)
            return render_template('login_manager.html')


@app.route('/login_out/')
def LoginOut():
    if session.get('teamid'):
        session.pop('teamid')
        return redirect(url_for('login'))
    elif session.get('adminid'):
        session.pop('adminid')
        return redirect(url_for('adminLogin'))



@app.route('/EditPassword/',methods=['POST'])
@admin_login_required
def EditTeamPassword():
    team1=Team.query.filter(Team.id==session.get('teamid')).first()
    if request.form.get('oldpassword') == team1.password:
        team1.password =request.form.get('newpassword')
        db.session.commit()
        return redirect(url_for('LoginOut'))
    else:
        return redirect(url_for('login'))




@app.route('/announcement/')
@login_required
def notice():
    notice1=Notice.query.filter(Notice.content !=None).order_by(Notice.id.desc()).all()
    # notice1 =sorted(notice1,key=attrgetter('id'),reverse=True)
    for i in notice1:
        print(i.content)
    return render_template('announcement.html',notice1=notice1)

#curl 提交flag的路由
@app.route('/flag',methods=['POST'])
def flag():
    try:
        Authorization=request.headers.get('Authorization')
        flag=json.loads(request.get_data().decode('ascii'))['flag']
        if not Authorization:
            return "need Authorization"
        status=authorizationSaveFlag(flag,Authorization,1)
        if status==0:
            return "error flag"
        return "you are right!"
    except:
        return "error"



@app.route('/showSource/')
def showSource():
    source1 = Source.query.order_by(Source.source.desc()).all()
    return render_template('rank.html', source1=source1)


@app.route('/showStatus/')
@login_required
def showStatus():
    teamid=session.get('teamid')
    vulList=Vulhub.query.filter(tid=teamid).all()
    return render_template('time.html',vulList=vulList)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'),500


#测试路由
@app.route('/test/')
def test():
    print(request.path)
    return "hi!"


def saveLog(username,ischeck):
    '''
    存储登录日志函数
    :param username:
    :param ischeck:
    :return:
    '''
    log=Log(username=username,ischeck=ischeck)
    db.session.add(log)
    db.session.commit()


if __name__ == "__main__":
    app.run()