from flask import Flask
from flask_app.database import db, Tasks, Lists, Users
from flask_app.extensions.loginmanager import login_manager
from flask_app.extensions.socketio import socketio
from flask_app.auxiliary.login_actions import autogenerate_account, user_pass_is_valid, open_todos_permission
from config import ConfigsByName

app = Flask(__name__)
app.config.from_object(ConfigsByName['development'])

login_manager.init_app(app)
socketio.init_app(app)


db.init_app(app)

with app.app_context():
    db.create_all()

from flask_app import routes
from flask_app import events
