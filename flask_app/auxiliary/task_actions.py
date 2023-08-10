from flask import url_for
from flask_app.database import db, Tasks
from sqlalchemy.orm.exc import UnmappedInstanceError
from flask_socketio import emit


def task_sorter(task_queries):
    try:
        list_of_tasks = sorted(task_queries, key=lambda task: task.order_)
    except TypeError:
        list_of_tasks = []
    return list_of_tasks


# _____________TASK ACTIONS_______________

def add_task(list_id, task):
    list_of_tasks = Tasks.query.filter_by(list_id=list_id).all()
    print(list_of_tasks)
    if len(list_of_tasks) == 0:
        order = 0
    else:
        # below snippet is to find the order of the new task before the star tasks.
        for task2 in list_of_tasks[::-1]:
            print(task2.todo)
            if task2.star == 1:
                var_saver = task2.order_
                order = var_saver
                task2.order_ += 1
                print(1)
            elif task2.star == 0:
                order = task2.order_ + 1
                print(2)
                break
    new_task = Tasks(todo=task, color="#8696FE", star=0, done=0, order_=order, list_id=list_id)
    db.session.add(new_task)
    db.session.commit()

    # This make the page to refresh using socketio which makes the page no need to back multiple time to reach the list page,
    # you just need to back once.
    return emit('redirect', {'url': url_for('todos', list_id=list_id)})


# _____________TASK ACTIONS PANEL_______________
def delete_task(id, list_id):
    try:
        task = Tasks.query.get(id)
        db.session.delete(task)
        db.session.commit()
    except UnmappedInstanceError:
        pass
    return emit('redirect', {'url': url_for('todos', list_id=list_id)})


def done_task(id, list_id):
    list_of_tasks = task_sorter(Tasks.query.filter_by(list_id=list_id).all())
    task = Tasks.query.get(id)
    task.done = 1
    task.star = 0
    # below snippet is to sort done tasks before undone tasks.
    for task2 in list_of_tasks:
        if task2.done == 0:
            task2.order_ += 1
    for task2 in list_of_tasks:
        if task2.done == 0:
            task.order_ = task2.order_ - 1
            break

    db.session.commit()
    return emit('redirect', {'url': url_for('todos', list_id=list_id)})


def star_task(id, list_id):
    task = Tasks.query.get(id)
    list_of_tasks = task_sorter(Tasks.query.filter_by(list_id=list_id).all())
    if task.star == 1:
        task.star = 0
        db.session.commit()
        # below snippet is to sort non-star tasks before star tasks.
        for task2 in list_of_tasks[::-1]:
            if task2.star == 1 and task2.order_ < task.order_:
                var_saver = task2.order_
                task2.order_ = task.order_
                task.order_ = var_saver
    # below snippet is to star a task ond move it to the top of the list.
    elif task.star == 0:
        task.star = 1
        task.order_ = list_of_tasks[-1].order_ + 1

    db.session.commit()
    return emit('redirect', {'url': url_for('todos', list_id=list_id)})


def color_task(id, color, list_id):
    task = Tasks.query.get(id)
    task.color = color
    db.session.commit()
    return emit('redirect', {'url': url_for('todos', list_id=list_id)})


def order_task(id, to, list_id):
    list_of_tasks = task_sorter(Tasks.query.filter_by(list_id=list_id).all())

    task = Tasks.query.get(id)
    task_to_change_order = task.order_

    if to == "UP":
        # is statement below determines the task not to be the top one in the list.
        if task_to_change_order is not list_of_tasks[-1].order_:
            task.order_ = list_of_tasks[list_of_tasks.index(task) + 1].order_
            list_of_tasks[list_of_tasks.index(task) + 1].order_ = task_to_change_order

    elif to == "DOWN":
        if task_to_change_order is not list_of_tasks[0].order_:
            task.order_ = list_of_tasks[list_of_tasks.index(task) - 1].order_
            list_of_tasks[list_of_tasks.index(task) - 1].order_ = task_to_change_order

    db.session.commit()
    return emit('redirect', {'url': url_for('todos', list_id=list_id)})
