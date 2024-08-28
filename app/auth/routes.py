from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.models import Agent
from . import auth
from app.auth.forms import LoginForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Handle login logic here
        flash('Login requested for user {}, remember_me={}'.format(
            form.email.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@auth.route('/register')
def register():
    return render_template('register.html')


