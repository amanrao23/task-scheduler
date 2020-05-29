from flask import Blueprint, render_template, redirect, url_for, request, abort, flash
from flask_login import login_required, current_user
from app.models import Schedule
from .forms import TaskForm
from app import db
from datetime import datetime

task = Blueprint('task', __name__)

'''Function to check if user is allowed to view/update/delete task.'''


def isUserNotAllowed(task_id):
    events = Schedule.query.filter_by(id=task_id).first()
    if not events or events.user_id != current_user.id:
        return True
    return False


'''API to create a new task'''


@task.route('/task/create', methods=['GET', 'POST'])
@login_required
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        s_time = form.start_time.data
        e_time = form.end_time.data

        if s_time > e_time:
            flash('Start-Time must be greater than End-Time')
            return redirect(url_for('task.create_task'))
        if s_time < datetime.now():
            flash('Start-Time cannot be in past')
            return redirect(url_for('task.create_task'))
        new_task = Schedule(title=form.title.data, content=form.content.data,
                            start_time=s_time, end_time=e_time, user_id=current_user.id)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('auth.profile'))
    return render_template('newtask.html', form=form)


'''API to display a task'''


@task.route('/task/<int:task_id>')
@login_required
def view_task(task_id):
    events = Schedule.query.filter_by(id=task_id).first()
    if isUserNotAllowed(task_id):
        flash('You cannot view this Event.')
        return redirect(url_for('auth.profile'))
    return render_template('task.html', tasko=events)


'''API to delete a task'''


@task.route('/task/<int:task_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_task(task_id):
    if isUserNotAllowed(task_id):
        flash('You cannot delete this Event.')
        return redirect(url_for('auth.profile'))
    event = Schedule.query.filter_by(id=task_id).first()
    db.session.delete(event)
    db.session.commit()
    flash('Your event has been deleted!', 'success')
    return redirect(url_for('auth.profile'))


'''API to update a task'''


@task.route('/task/<int:task_id>/update', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    event = Schedule.query.filter_by(id=task_id).first()
    if isUserNotAllowed(task_id):
        flash('You cannot update this Event.')
        return redirect(url_for('auth.profile'))
    form = TaskForm()
    if form.validate_on_submit():
        event.title = form.title.data
        event.content = form.content.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        db.session.commit()
        return redirect(url_for('auth.profile'))

    elif request.method == 'GET':
        form.title.data = event.title
        form.content.data = event.content
        form.start_time.data = event.start_time
        form.end_time.data = event.end_time
    return render_template('updatetask.html', task_id=event.id,
                           form=form)
