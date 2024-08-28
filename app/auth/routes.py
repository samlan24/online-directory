from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.models import Agent
from . import auth

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/register')
def register():
    return render_template('register.html')


