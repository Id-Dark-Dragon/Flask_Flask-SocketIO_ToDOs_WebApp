from flask import session
import uuid
from flask_app.database import db, Lists, Users
from time import time


def autogenerate_account():
    if 'visitor_id' not in session:
        # If the visitor has no ID yet, generate a new one and store it in the session
        session['visitor_id'] = str(uuid.uuid4())

    # making a new account automatically when a new user enters the site.
    if db.session.query(Users).filter_by(first_session_id=session['visitor_id']).first() is None:
        new_temp_user = Users(name='temp-user-saver', passw='not-set', join_timestamp=time(),
                              first_session_id=session['visitor_id'])
        db.session.add(new_temp_user)
        db.session.commit()

    return db.session.query(Users).filter_by(first_session_id=session['visitor_id']).first()


def user_pass_is_valid(user, password):
    if len(user) > 1 and len(password) > 1:
        if user is not 'temp-user-saver':
            return True
    else:
        return False


def open_todos_permission(list_id, current_user):
    requested_list = Lists.query.get(list_id)
    if requested_list is None:
        return False
    elif requested_list.user_id != current_user.id:
        return False


