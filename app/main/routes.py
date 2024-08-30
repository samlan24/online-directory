from flask import Blueprint, render_template, abort
from app.models import Agent

""" blueprint for main routes """

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/contact')
def contact():
    return render_template('contact.html')


@main.route('/search')
def search():
    return render_template('search.html')

@main.route('/agent/<username>')
def agent(username):
    user = Agent.query.filter_by(name=username).first()
    if user is None:
        abort(404)
    return render_template('agent.html', user=user)