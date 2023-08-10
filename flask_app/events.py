from flask import redirect, url_for, flash
from flask_app import socketio
from flask_app.auxiliary import task_actions
from flask_login import current_user
from flask_app.auxiliary.login_actions import open_todos_permission


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
