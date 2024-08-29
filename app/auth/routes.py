from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from app.models import Agent
from flask_login import login_user, logout_user
from . import auth
from app.auth.forms import LoginForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = user.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('invalid username or password')
    return render_template('login.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash("successfully logged out.")
    return redirect(url_for("main.index"))


