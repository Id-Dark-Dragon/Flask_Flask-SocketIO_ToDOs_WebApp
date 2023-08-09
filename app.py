import html
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import db, Tasks, Lists, Users
import task_actions
from flask_socketio import SocketIO
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from login_actions import autogenerate_account, user_pass_is_valid, open_todos_permission

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret! temporary'
login_manager = LoginManager(app)
login_manager.login_view = 'index'
socketio = SocketIO(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db.init_app(app)

with app.app_context():
    db.create_all()


@login_manager.user_loader
def user_load(user_id):
    return Users.query.get(int(user_id))


@app.route('/login', methods=["POST"])
def login():
    if user_pass_is_valid(request.form.get('name'), request.form.get('pass')):
        # sanitizing inputs
        username = html.escape(request.form.get('name'))
        password = html.escape(request.form.get("pass"))

        user_to_login = Users.query.filter_by(name=username).first()
        # ___ sign in ___
        if request.form.get('sign') == '0':
            if user_to_login is None:
                flash("This user is not registered before, \n Sign For The First Time")
            else:
                print(current_user.lists)
                if user_to_login.passw == password:
                    # previous registered user enters
                    for list in current_user.lists:
                        print(list)
                        list.name = f"{list.name} new"
                        list.user_id = user_to_login.id
                        db.session.commit()

                    db.session.delete(Users.query.get(current_user.id))
                    logout_user()
                    db.session.commit()

                    user_to_login.first_session_id = session['visitor_id']
                    db.session.commit()
                    login_user(user_to_login, remember=True)
                else:
                    flash("Wrong Username or Password!")

        # ___ sign up ___
        elif request.form.get('sign') == '1':
            if user_to_login is None:
                # make (update info of) new user
                user = Users.query.get(current_user.id)
                user.name = username
                user.passw = password
                db.session.commit()
            else:
                flash("This username already exists, \n Try a different one.")

        else:
            flash("Enter the Correct info!")

    else:
        flash("Unsupported Type of Info!")

    return redirect(url_for('index'))


@app.route('/')
def index():
    if current_user.is_authenticated:
        session['visitor_id'] = current_user.first_session_id
    else:
        login_user(autogenerate_account(), remember=True)
    return redirect(url_for("lists"))


@app.route('/lists', methods=["GET", "POST"])
@ login_required
def lists():

    return render_template('lists.html', lists=current_user.lists, current_user=current_user)


@app.route('/<int:list_id>/todos', methods=["GET", ])
@login_required
def todos(list_id):
    list_of_tasks = task_actions.task_sorter(Tasks.query.filter_by(list_id=list_id).all())

    # checking if the list belongs to the current use
    if open_todos_permission(list_id, current_user) is False:
        flash("Access denied. This list doesn't belong to you.")
        return redirect(url_for('lists'))

    return render_template('todos.html', tasks=list_of_tasks[::-1], list_id=list_id, current_user=current_user)


@app.route('/add-list')
@login_required
def add_list():

    # list naming
    l = 1
    for _ in current_user.lists:
        l += 1
    new_list = Lists(name=f"Tasks list {l}", user_id=current_user.id)
    db.session.add(new_list)
    db.session.commit()

    return redirect(url_for('lists'))


@app.route('/del-list/<int:list_id>')
def del_list(list_id):
    if open_todos_permission(list_id, current_user) is False:
        flash("Access denied. This list doesn't belong to you.")
        return redirect(url_for('lists'))
    lst_to_del = Lists.query.get(list_id)
    for task in lst_to_del.tasks:
        db.session.delete(task)
    db.session.delete(lst_to_del)
    db.session.commit()
    return redirect(url_for('lists'))


@socketio.on("add-task")
def add_task(list_id, task):
    if open_todos_permission(list_id, current_user) is False:
        flash("Access denied. This list doesn't belong to you.")
        return redirect(url_for('lists'))
    return task_actions.add_task(list_id=list_id, task=task)


@socketio.on("deleteTask")
def delete_task(id, list_id):
    if open_todos_permission(list_id, current_user) is False:
        flash("Access denied. This list doesn't belong to you.")
        return redirect(url_for('lists'))
    return task_actions.delete_task(id, list_id)


@socketio.on("doneTask")
def done_task(id, list_id):
    if open_todos_permission(list_id, current_user) is False:
        flash("Access denied. This list doesn't belong to you.")
        return redirect(url_for('lists'))
    return task_actions.done_task(id, list_id)


@socketio.on("starTask")
def star_task(id, list_id):
    if open_todos_permission(list_id, current_user) is False:
        flash("Access denied. This list doesn't belong to you.")
        return redirect(url_for('lists'))
    return task_actions.star_task(id, list_id)


@socketio.on("colorTask")
def color_task(id, color, list_id):
    if open_todos_permission(list_id, current_user) is False:
        flash("Access denied. This list doesn't belong to you.")
        return redirect(url_for('lists'))
    return task_actions.color_task(id, color, list_id)


@socketio.on("orderTask")
def order_task(id, direction, list_id):
    if open_todos_permission(list_id, current_user) is False:
        flash("Access denied. This list doesn't belong to you.")
        return redirect(url_for('lists'))
    return task_actions.order_task(id, direction, list_id)


if __name__ == '__main__':
    socketio.run(app, debug=True)
