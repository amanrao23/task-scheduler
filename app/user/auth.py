from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, Schedule
from app.user.forms import LoginForm, RegisterForm
from app import db, bcrypt

auth = Blueprint('auth', __name__)

'''API to display profile page of User'''


@auth.route('/profile')
@login_required
def profile():
    page = request.args.get('page', 1, type=int)
    tasks = Schedule.query.filter_by(user_id=current_user.id).order_by(Schedule.start_time).paginate(page=page,
                                                                                                     per_page=5)
    return render_template('profile.html', name=current_user.name, tasks=tasks)


'''API to login a user'''


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user or not bcrypt.check_password_hash(user.password, form.password.data):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember)
        return redirect(url_for('auth.profile'))

    return render_template('login.html', form=form)


'''API to register a user'''


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(name=form.username.data, email=form.email.data,
                        password=hashed_password)
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('User already exists')
            return redirect(url_for('auth.signup'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)


'''API to logout a user'''


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
