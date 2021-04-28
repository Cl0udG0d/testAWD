from models import *
from init import app
#插入用户数据
def insertTeamData(teamname,password):
    with app.app_context():
        team1=Team(teamname=teamname,password=password)
        db.session.add(team1)
        #事务提交
        db.session.commit()

#修改用户数据
  #1.先把你要更改的数据查找出来
def editTeamData(id,newteamname,newpassword):
    with app.app_context():
        team1 = Team.query.filter(Team.id == id ).first()
        #2.把这条数据，你需要修改的地方进行修改
        team1.username = newteamname
        team1.password = newpassword
        #3.把事务进行提交
        db.session.commit()


#删除用户数据
    #1.把需要删除的数据查找出来
def DeleteTeamData(id):
    with app.app_context():
        team1 = Team.query.filter(Team.id == id ).first()
        #2.把这条数据删除掉
        db.session.delete(team1)
        #3.做数据的提交
        db.session.commit()



#插入管理员数据
def insertAdminData(adminname,password):
    with app.app_context():
        admin1=Admin(adminname=adminname,password=password)
        db.session.add(admin1)
        #事务提交
        db.session.commit()


#修改管理员数据
  #1.先把你要更改的数据查找出来
def editAdminData(id,newadminname,newpassword):
    with app.app_context():
        admin1 = Admin.query.filter(Admin.id == id ).first()
        #2.把这条数据，你需要修改的地方进行修改
        admin1.username = newadminname
        admin1.password = newpassword
        #3.把事务进行提交
        db.session.commit()


#删除管理员数据
    #1.把需要删除的数据查找出来
def DeleteAdminData(id):
    with app.app_context():
        admin1 = Admin.query.filter(Admin.id == id ).first()
        #2.把这条数据删除掉
        db.session.delete(admin1)
        #3.做数据的提交
        db.session.commit()


#插入公告数据
def insertNoticeData(content):
    with app.app_context():
        notice1=Notice(content=content)
        db.session.add(notice1)
        #事务提交
        db.session.commit()

#修改公告数据
  #1.先把你要更改的数据查找出来
def editAdminData(id,newcontent):
    with app.app_context():
        notice1 = Notice.query.filter(Notice.id == id ).first()
        #2.把这条数据，你需要修改的地方进行修改
        notice1.username = newcontent
        #3.把事务进行提交
        db.session.commit()

#删除公告数据
    #1.把需要删除的数据查找出来
def DeleteAdminData(id):
    with app.app_context():
        notice1 = Notice.query.filter(Notice.id == id ).first()
        #2.把这条数据删除掉
        db.session.delete(notice1)
        #3.做数据的提交
        db.session.commit()

if __name__ == '__main__':
    insertNoticeData('4月2号交数据挖掘课设')