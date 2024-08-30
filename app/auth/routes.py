from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from app.models import Agent
from app import db
from flask_login import login_user, logout_user, current_user
from . import auth
from app.auth.forms import LoginForm, RegistrationForm

# log in route
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Agent.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('invalid username or password')
    return render_template('login.html', form=form)

# logout
@auth.route('/logout')
def logout():
    logout_user()
    flash("successfully logged out.")
    return redirect(url_for("main.index"))


# registering
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Agent(email=form.email.data,
                     name=form.name.data,
                     password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)
