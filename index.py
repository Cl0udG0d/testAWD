from init import app
from app.users import users
from app.admin import admin
from app.tourist import tourist

from models import Role

Role.init_role()

# 注册蓝图
app.register_blueprint(admin, url_prefix='/admin')
app.register_blueprint(users, url_prefix='/users')
app.register_blueprint(tourist)


if __name__ == "__main__":
    app.run(debug=True)