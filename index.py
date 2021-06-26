import json
from flask import request, render_template, redirect, url_for, session, jsonify, flash

from core.vulHub.vulManage import writeFlag2Vulhub
from exts import db
from init import app
from models import Admin,Notice,Flag,AttackRecord,Team,Vulhub,Log,ULog,Game
from core.flag.saveFlag import authorizationSaveFlag,checkFlagIndex
from core.unit.decorators import login_required,admin_login_required
from core.team.createTeam import createTeam
from core.flag.createFlag import updateFlagIndex, createFlagIndex
from config import OneRoundSec,CheckDownPath,OneRoundSec
import os
from time import strftime, localtime
from apscheduler.schedulers.background import BackgroundScheduler
from tasks import checkDownMain, timeCount,newRoundFlushCheck

scheduler = BackgroundScheduler(timezone='MST')

#===================================== AJAX定时任务 =========================
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
    tid=session.get('teamid')
    nowSource = {}
    if tid is not None:
        source = Team.query.filter(Team.id == tid).first().source
        nowSource['source'] = source
    else:
        nowSource['source'] =1000
    return json.dumps(nowSource)


@app.route('/', methods=['GET', 'POST'])
def index():
    tid = session.get("teamid")
    if not tid:
        tid = 1
    team = Team.query.filter(Team.id == tid).first()
    vulhubList = Vulhub.query.filter(Vulhub.tid == tid).filter(Vulhub.cansee==True)
    noticeList=Notice.query.all()
    sourcelist=Team.query.order_by(Team.source.desc()).all()
    context={
        "team":team,
        "vulhubList":vulhubList,
        "noticeList":noticeList,
        "sourcelist":sourcelist,
    }

    return render_template('K_index.html',context=context)

#=============================启动比赛相关
@app.route('/start', methods=['GET', 'POST'])
def start():
    gamelist = Game.query.all()
    return render_template('T_game_manager.html',gamelist=gamelist)

@app.route('/startGame/<gid>', methods=['GET', 'POST'])
def startGame(gid):
    '''
    开始某场比赛
    1，将比赛 is_start 设置为 True
    2，参赛选手靶机可见
    3，写入flag
    3，比赛开始计时
    4，定时check脚本开始运行
    :return:
    '''
    if gid is None:
        return redirect(url_for('start'))

    tempgame = Game.query.filter(Game.id == gid).first()
    tempgame.is_start=True

    vulhublist = Vulhub.query.all()
    for vulhub in vulhublist:
        vulhub.cansee=True

    #创建 flag
    createFlagIndex()
    #写入 flag
    writeFlag2Vulhub()
    nowTime=strftime('%Y-%m-%d %H:%M:%S', localtime())
    tempgame.starttime=nowTime

    db.session.commit()

    intervalTaskStart()
    return redirect(url_for('start'))

def startGameFactor():
    return


def intervalTaskStart():
    '''
    开启定时任务函数
    :return:
    '''
    app.config['TIMENOW'] = 0

    # 比赛计时开始 每秒钟该时间递增
    scheduler.add_job(func=timeCount, trigger='interval', seconds=1)
    # 检测宕机任务 宕机检测每15秒一次
    scheduler.add_job(func=checkDownMain, trigger='interval', seconds=15)
    scheduler.add_job(func=newRoundFlushCheck,trigger='interval', seconds=1)
    scheduler.start()
    print("定时任务已开启")
    return


@app.route('/addGame', methods=['GET', 'POST'])
def addGame():
    if request.method=='GET':
        context=[]
        teamInfoList=Team.query.all()
        for team in teamInfoList:
            vulhubList=Vulhub.query.filter(Vulhub.tid==team.id)
            teamInfo={'id':team.id,'teamname':team.teamname,'vulhubList':vulhubList,'token':team.token}
            context.append(teamInfo)
        return render_template('T_add_game.html',context=context)
    else:
        gametitle=request.form.get('gametitle')
        tempgame=Game(gametitle=gametitle)
        db.session.add(tempgame)
        db.session.commit()
        return redirect(url_for('start'))

@app.route('/indexShow', methods=['GET', 'POST'])
def indexShow():
    nowgame=Game.query.order_by(Game.id.desc()).first()
    if nowgame is None:
        title="暂未开始"
    else:
        title=nowgame.gametitle
    attackrecord=AttackRecord.query.order_by(AttackRecord.id.desc()).all()
    attacklist=[]
    for attack in attackrecord:
        attackteamname=Team.query.filter(Team.id==attack.sourcetid).first().teamname
        attedteamname=Team.query.filter(Team.id==attack.goaltid).first().teamname
        attacklist.append({
            "time":attack.atttime,
            "attteamname":attackteamname,
            "attedteamname":attedteamname,
        })
    context={
        "title":title,
        "teamlist":zip(range(len(Team.query.order_by(Team.source.desc()).all())),Team.query.order_by(Team.source.desc()).all()),
        "attackrecord":attacklist
    }

    return render_template('index_show.html',context=context)


@app.route('/adminIndex', methods=['GET', 'POST'])
def adminIndex():
    return render_template('T_admin_index.html')

#===============================日志相关
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

def operateLog(text):
    '''
    记录操作日志:
    1，攻击事件记录
    2，提交flag记录
    3，更新容器flag记录
    4，轮数记录
    5，宕机记录
    :return:
    '''
    with app.app_context():
        ulog = ULog(text=text)
        db.session.add(ulog)
        db.session.commit()
    return

#=================================管理员相关
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
        checklist = list()
        for tempfile in os.listdir(CheckDownPath):
            if tempfile.endswith('.py'):
                checklist.append(tempfile.split('.')[0])
        return render_template('T_edit_vulhub.html', vulhub=vulhub,checklist=checklist)
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
        return redirect(url_for('vulhubManage'))

@app.route('/addVulhub', methods=['GET', 'POST'])
def addVulhub():
    if request.method=='GET':
        teamlist=Team.query.all()
        checklist=list()
        for tempfile in os.listdir(CheckDownPath):
            if tempfile.endswith('.py'):
                checklist.append(tempfile.split('.')[0])
        return render_template('T_add_vulhub.html',teamlist=teamlist,checklist=checklist)
    else:
        tname=request.form.get('tname')
        team = Team.query.filter(Team.teamname == tname).first()
        if team is None:
            return "无此队伍信息"
        vulname=request.form.get('vulname')
        addr=request.form.get('addr')
        serviceport=request.form.get('serviceport')
        sshport=request.form.get('sshport')
        sshname=request.form.get('sshname')
        sshpass=request.form.get('sshpass')
        dockerid=request.form.get('dockerid')
        detail=request.form.get('detail')
        with app.app_context():
            vulhub=Vulhub(tid=team.id,vulname=vulname,addr=addr,serviceport=serviceport,sshport=sshport,sshname=sshname,sshpass=sshpass,dockerid=dockerid,detail=detail)
            db.session.add(vulhub)
            db.session.commit()
        return redirect(url_for('vulhubManage'))

@app.route('/delVulhub/<vid>', methods=['GET', 'POST'])
def delVulhub(vid):
    if vid is None:
        return redirect(url_for('vulhubManage'))
    else:
        with app.app_context():
            vulhub = Vulhub.query.filter(Vulhub.id == vid).first()
            db.session.delete(vulhub)
            db.session.commit()
        return redirect(url_for('vulhubManage'))

@app.route('/sysInfo', methods=['GET', 'POST'])
def sysInfo():
    if request.method == 'GET':
        return render_template('T_SysConfig.html',context=app.config)
    else:
        flagstart=request.form.get('flagstart')
        flagend=request.form.get('flagend')
        sshpass=request.form.get('sshpass')
        app.config['FLAG_START']=flagstart
        app.config['FLAG_END']=flagend
        app.config['SSHPASS']=sshpass
        return render_template('T_SysConfig.html',context=app.config)

#=============================================登录相关
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
            return "success"
        else:
            saveLog(teamname, password,False)
            return "wrong"

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


#curl 提交flag的路由
#存在两种提交flag的方式
#一种是网页上直接提交
#另一种是编写脚本文件进行批量定时提交
#两种方式各有千秋，推荐编写脚本自动提交，方便拿到shell维权后躺赢
#消息闪现
@app.route('/flag',methods=['POST'])
def flag():
    nowRound = int(app.config['TIMENOW'] / OneRoundSec) + 1
    try:
        if session.get('teamid'):
            teamid= session.get('teamid')
            flag = request.form.get('flag')
            msg,status=checkFlagIndex(teamid,nowRound,flag)
            flash(msg, status)  # 添加闪现信息
            return redirect(url_for('index'))
        elif request.headers.get('Authorization'):
            Authorization=request.headers.get('Authorization')
            flag=json.loads(request.get_data().decode('ascii'))['flag']
            if not Authorization:
                return "need Authorization"
            status=authorizationSaveFlag(flag,Authorization,nowRound)
            if status==0:
                return "error flag"
            elif status==2:
                return "flag already submit"
            return "flag is right!"
        else:
            return redirect(url_for('login'))
    except Exception as e:
        print(e)
        return "error"



#=======================================404 500 测试页面 注释
# 404 页面
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


# 500 页面
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'),500


#测试路由
@app.route('/test/')
def test():
    def add():
        print(1+1)
    app.config['EXECUTOR'].submit(add)
    return str(app.config['CURRENTROUND'])



if __name__ == "__main__":
    app.run()