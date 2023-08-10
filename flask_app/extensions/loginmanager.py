from flask_app.database import Users
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.login_view = 'index'


@login_manager.user_loader
def user_load(user_id):
    return Users.query.get(int(user_id))
