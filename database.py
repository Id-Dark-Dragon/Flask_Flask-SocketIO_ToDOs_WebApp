from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()


class Users(db.Model, UserMixin):
    __tablename__ = "userstable"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    passw = db.Column(db.String(40), unique=False, nullable=False)
    first_session_id = db.Column(db.String(1000), unique=True, nullable=False)  # user first visiting id for saveing porposes
    join_timestamp = db.Column(db.Float, unique=False, nullable=True)
    lists = db.relationship("Lists", backref="user", lazy=True)

    def __repr__(self):
        return f'<user {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'passw': self.passw,
            'lists': self.lists,
            'first_session_id': self.first_session_id,
            'join_timestamp': self.join_timestamp
        }


class Lists(db.Model):
    __tablename__ = "liststable"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=False, nullable=False)
    tasks = db.relationship("Tasks", backref="list", lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey("userstable.id"))

    def __repr__(self):
        return f'<Task {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'tasks': self.tasks,
            'user_id': self.user_id,

        }


class Tasks(db.Model):
    __tablename__ = "taskstable"
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(40), unique=False, nullable=False)
    color = db.Column(db.String(), unique=False, nullable=False)
    star = db.Column(db.Boolean(), unique=False, nullable=False)
    done = db.Column(db.Boolean(), unique=False, nullable=False)
    order_ = db.Column(db.Integer(), unique=False, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey("liststable.id"), nullable=False)

    def __repr__(self):
        return f'<Task {self.todo}>'

    def to_dict(self):
        return {
            'id': self.id,
            'todo': self.todo,
            'order_': self.order_,
            'done': self.done,
            'color': self.color,
            'list_id': self.list_id
        }


