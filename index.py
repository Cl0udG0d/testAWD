from flask import request,render_template
from init import app


@app.route('/', methods=['GET', 'POST'])
def hello():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run()