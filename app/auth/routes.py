from flask import Blueprint, render_template, redirect, url_for, flash, session
from app import db, oauth
from app.models import Agent
import os

"""route for authentication"""

auth = Blueprint('auth', __name__, template_folder='templates', static_folder='static')



# create an oauth object
google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    userinfo_endpoint='https://www.googleapis.com/oauth2/v1/userinfo',
    client_kwargs={'scope': 'openid profile email'},
)


# create a route for registration
@auth.route('/register')
def register():
    google = oauth.create_client('google')
    redirect_uri = url_for('auth.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

# create a route for login
@auth.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('auth.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@auth.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    user = Agent.query.filter_by(email=user_info['email']).first()
    if user is None:
        user = Agent(name=user_info['name'], email=user_info['email'])
        db.session.add(user)
        db.session.commit()
    session['user_id'] = user.id
    flash('You were successfully logged in')
    return redirect(url_for('auth.profile'))


@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You were successfully logged out')
    return redirect(url_for('auth.login'))


@auth.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('Please login first', 'warning')
        return redirect(url_for('auth.login'))
    user = Agent.query.get(session['user_id'])
    return render_template('profile.html', user=user)
