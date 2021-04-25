from flask import request,render_template,redirect,url_for
from init import app
from models import *

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        #print("{} {}".format(username,password))
        user1 = User.query.filter(User.username == username).filter(User.password==password).first()
        #print(user1)
        if user1:
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
        print("{} {}".format(adminname,password))
        admin1 = Admin.query.filter(User.username == adminname).filter(Admin.password==password).first()
        if admin1:
            return redirect(url_for('index'))
        else:
            return render_template('login_manager.html')


@app.route('/announcement/')
def notice():
    notice1=Notice.query.filter(Notice.content !=None).all()
    notice2=notice1.sort(reverse=False)
    # for i in notice2:
    #     print(notice1.id)
    return render_template('announcement.html')

if __name__ == "__main__":
    app.run(debug=True)