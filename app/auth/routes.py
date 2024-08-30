from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from app.models import Agent, Location, Role
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
            return redirect(request.args.get('next') or url_for('main.agent', name=user.name))
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
    form.location.choices = [(location.id, location.name) for location in Location.query.all()]

    if form.validate_on_submit():
        location = Location.query.get(form.location.data)
        role = Role.query.filter_by(default=True).first()
        user = Agent(email=form.email.data,
                     name=form.name.data,
                     password=form.password.data,
                     location=location,
                     role=role,
                     description=form.description.data)
        db.session.add(user)
        db.session.commit()
        flash('You can now login')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)



