import json
from flask import request, render_template, redirect, url_for, session, jsonify
from exts import db
from init import app, scheduler
from models import Admin,Notice,Flag,Source,AttackRecord,Team,Vulhub,Log,ULog,Time
from core.flag.saveFlag import authorizationSaveFlag
from core.unit.decorators import login_required,admin_login_required
from core.team.createTeam import createTeam
from core.flag.createFlag import updateFlagIndex,createFlagIndex
from config import OneRoundSec
from core.vulHub.vulManage import writeFlag2Vulhub
from core.flag.calculateTheScore import delTeamVulDownSource

@app.route('/start', methods=['GET', 'POST'])
def start():
    #初始化时钟
    session['TIMENOW']=0
    # 创建flag
    createFlagIndex()
    # 将 flag 写入靶机
    writeFlag2Vulhub()
    return render_template('T_admin_index.html')

@app.route('/lastTime',methods=['GET','POST'])
def lastTime():
    nowRound = {}
    if app.config['TIMENOW']==-1:
        nowRound['time']=0
    else:
        nowRound['time'] = int(OneRoundSec-app.config['TIMENOW']%OneRoundSec)
    return json.dumps(nowRound)

@app.route('/currentRound',methods=['GET','POST'])
def currentRound():
    # nowTime=Time.query.filter(Time.id==1).first()
    # print(nowTime.timeNow)
    nowRound={}
    if app.config['TIMENOW']==-1:
        nowRound['time']='未开始'
    else:
        nowRound['time'] = int(app.config['TIMENOW']/OneRoundSec)+1
    # app.config['TIMENOW']+=1
    return json.dumps(nowRound)

@app.route('/currentSource',methods=['GET','POST'])
def currentSource():
    tid=session.get('tid')

    source = Source.query.filter(Source.tid == tid).first()
    nowSource={}
    nowSource['source'] =1000
    return json.dumps(nowSource)

@app.route('/sourceList',methods=['GET','POST'])
def sourceList():
    sourceDict={}
    sourceList = Source.query.all()

    nowSource={}
    nowSource['source'] =source.source
    return json.dumps(nowSource)

@app.route('/', methods=['GET', 'POST'])
def index():
    tid = session.get("tid")
    if not tid:
        tid = 1
    team = Team.query.filter(Team.id == tid).first()
    vulhubList = Vulhub.query.filter(Vulhub.tid == tid)
    noticeList=Notice.query.all()
    context={
        "team":team,
        "vulhubList":vulhubList,
        "noticeList":noticeList
    }

    return render_template('K_index.html',context=context)

@app.route('/indexShow', methods=['GET', 'POST'])
def indexShow():
    return render_template('index_show.html')


@app.route('/adminIndex', methods=['GET', 'POST'])
def adminIndex():
    return render_template('T_admin_index.html')

@app.route('/loginLog', methods=['GET', 'POST'])
def loginLog():
    loglist=Log.query.all()

    return render_template('T_Login_log.html',loglist=loglist)

@app.route('/delLoginLog', methods=['GET', 'POST'])
def delLoginLog():
    with app.app_context():
        logList=Log.query.all()
        [db.session.delete(log) for log in logList]
        db.session.commit()
    return redirect(url_for('loginLog'))

@app.route('/useLog', methods=['GET', 'POST'])
def useLog():
    loglist = ULog.query.all()
    return render_template('T_Operation_Log.html',loglist=loglist)

@app.route('/delUseLog', methods=['GET', 'POST'])
def delUseLog():
    with app.app_context():
        ulogList = ULog.query.all()
        [db.session.delete(log) for log in ulogList]
        db.session.commit()
    return redirect(url_for('useLog'))

@app.route('/addTeam', methods=['GET', 'POST'])
def addTeam():
    if request.method=='GET':
        return render_template('T_add_Team.html')
    else:
        teamname=request.form.get('teamname')
        createTeam(teamname)
        team=Team.query.order_by(Team.id.desc()).first()
        return render_template('T_show_team.html',team=team)

@app.route('/delTeam/<tid>', methods=['GET', 'POST'])
def delTeam(tid):
    if tid:
        with app.app_context():
            team=Team.query.filter(Team.id == tid).first()
            db.session.delete(team)
            db.session.commit()
    return redirect(url_for('teamManage'))

@app.route('/editTeam/<tid>', methods=['GET', 'POST'])
def editTeam(tid):
    if not tid:
        tid=1
    team=Team.query.filter(Team.id == tid).first()
    if request.method=='GET':
        return render_template('T_edit_team.html',team=team)
    else:
        teamname=request.form.get('teamname')
        password=request.form.get('password')
        token=request.form.get('token')
        with app.app_context():
            team.teamname,team.password,team.token=teamname,password,token
            db.session.commit()
        tempteam=Team.query.filter(Team.id == tid).first()
        return render_template('T_edit_team.html',team=tempteam)

@app.route('/teamManage', methods=['GET', 'POST'])
def teamManage():
    teamList=Team.query.all()
    return render_template('T_team_manage.html',teamList=teamList)

@app.route('/noticeManage', methods=['GET', 'POST'])
def noticeManage():
    noticeList = Notice.query.all()
    return render_template('T_notice_manage.html',noticeList=noticeList)

@app.route('/addNotice', methods=['GET', 'POST'])
def addNotice():
    if request.method=='GET':
        return render_template('T_add_notice.html')
    else:
        title=request.form.get('title')
        content=request.form.get('content')
        with app.app_context():
            notice=Notice(title=title,content=content)
            db.session.add(notice)
            # 事务提交
            db.session.commit()
        return redirect(url_for('noticeManage'))

@app.route('/delNotice/<nid>', methods=['GET', 'POST'])
def delNotice(nid):
    if nid:
        with app.app_context():
            notice=Notice.query.filter(Notice.id == nid).first()
            db.session.delete(notice)
            db.session.commit()
    noticeList = Notice.query.all()
    return render_template('T_notice_manage.html',noticeList=noticeList)

@app.route('/editNotice/<nid>', methods=['GET', 'POST'])
def editNotice(nid):
    if not nid:
        nid=1
    notice = Notice.query.filter(Notice.id == nid).first()
    if request.method=='GET':
        return render_template('T_edit_notice.html',notice=notice)
    else:
        title=request.form.get('title')
        content=request.form.get('content')
        with app.app_context():
            notice.title,notice.content=title,content
            db.session.commit()
        notice = Notice.query.filter(Notice.id == nid).first()
        return render_template('T_edit_notice.html',notice=notice)

@app.route('/flagManage', methods=['GET', 'POST'])
def flagManage():
    flagList = Flag.query.all()
    return render_template('T_flag_manage.html',flagList=flagList)

@app.route('/editFlag/<fid>', methods=['GET', 'POST'])
def editFlag(fid):
    if not fid:
        fid=1
    flag = Flag.query.filter(Flag.id == fid).first()
    if request.method == 'GET':
        return render_template('T_edit_flag.html', flag=flag)
    else:
        flag = request.form.get('flag')
        with app.app_context():
            flag.flag=flag
            db.session.commit()
        flag = Flag.query.filter(Flag.id == fid).first()
        return render_template('T_edit_flag.html', flag=flag)

@app.route('/resetFlag', methods=['GET', 'POST'])
def resetFlag():
    updateFlagIndex()
    return redirect(url_for('flagManage'))

@app.route('/vulhubManage', methods=['GET', 'POST'])
def vulhubManage():
    vulhubList = Vulhub.query.all()
    return render_template('T_vulhub_manage.html',vulhubList=vulhubList)

@app.route('/editVulhub/<vid>', methods=['GET', 'POST'])
def editVulhub(vid):
    if not vid:
        vid=1
    vulhub = Vulhub.query.filter(Vulhub.id == vid).first()
    if request.method=='GET':
        return render_template('T_edit_vulhub.html', vulhub=vulhub)
    else:
        vulname=request.form.get('vulname')
        addr=request.form.get('addr')
        serviceport=request.form.get('serviceport')
        sshport=request.form.get('sshport')
        sshname=request.form.get('sshname')
        sshpass=request.form.get('sshpass')
        dockerid=request.form.get('dockerid')
        status=bool(request.form.get('status'))
        detail=request.form.get('detail')
        with app.app_context():
            vulhub.vulname,vulhub.addr,vulhub.serviceport,vulhub.sshport,vulhub.sshname,vulhub.sshpass,vulhub.dockerid,vulhub.status,vulhub.detail=vulname,addr,serviceport,sshport,sshname,sshpass,dockerid,status,detail
            db.session.commit()
        vulhub = Vulhub.query.filter(Vulhub.id == vid).first()
        return render_template('T_edit_vulhub.html',vulhub=vulhub)

@app.route('/addVulhub', methods=['GET', 'POST'])
def addVulhub():
    if request.method=='GET':
        return render_template('T_add_vulhub.html')
    else:
        tid=request.form.get('tid')
        vulname=request.form.get('vulname')
        addr=request.form.get('addr')
        serviceport=request.form.get('serviceport')
        sshport=request.form.get('sshport')
        sshname=request.form.get('sshname')
        sshpass=request.form.get('sshpass')
        dockerid=request.form.get('dockerid')
        detail=request.form.get('detail')
        with app.app_context():
            vulhub=Vulhub(tid=tid,vulname=vulname,addr=addr,serviceport=serviceport,sshport=sshport,sshname=sshname,sshpass=sshpass,dockerid=dockerid,detail=detail)
            db.session.add(vulhub)
            db.session.commit()
        return redirect(url_for('vulhubManage'))

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
        team1 = Team.query.filter(Team.teamname == teamname).filter(Team.password==password).first()
        #print(user1)
        if team1:
            saveLog(teamname, password,True)
            session['teamid'] = team1.id
            return redirect(url_for('index'))
        else:
            saveLog(teamname, password,False)
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
            saveLog(adminname, password,True)
            session['adminid'] = admin1.id
            return redirect(url_for('adminIndex'))
        else:
            saveLog(adminname, password,False)
            return render_template('login_manager.html')


@app.route('/login_out/')
def LoginOut():
    if session.get('teamid'):
        session.pop('teamid')
        return redirect(url_for('login'))
    elif session.get('adminid'):
        session.pop('adminid')
        return redirect(url_for('adminLogin'))
    else:
        return redirect(url_for('login'))



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



@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'),500


#测试路由
@app.route('/test/')
def test():
    app.config['TIMENOW'] = 0
    return str(app.config['TIMENOW'])


def saveLog(username,password,ischeck):
    '''
    存储登录日志函数
    :param username:
    :param ischeck:
    :return:
    '''
    log=Log(username=username,password=password,ischeck=ischeck)
    db.session.add(log)
    db.session.commit()

def flushAll():
    '''
    每隔一段时间就需要刷新场内的数据，例如分数统计
    :return:
    '''
    return

def newRound():
    '''
    新的一轮开始啦
    需要刷新所有靶机的flag
    :return:
    '''
    nowround=int(app.config['TIMENOW']/OneRoundSec)+1
    # 扣除本轮靶机宕机队伍的分数
    delTeamVulDownSource(nowround)
    # 创建flag
    createFlagIndex()
    # 将 flag 写入靶机
    writeFlag2Vulhub()
    return

if __name__ == "__main__":
    app.run()