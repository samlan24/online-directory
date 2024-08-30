from flask import Blueprint, render_template, abort, redirect, url_for
from app.models import Agent
from app.auth.forms import EditProfileForm
from flask_login import current_user
from app import db

""" blueprint for main routes """

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')

@main.route('/')
def index():
    featured_agents = Agent.query.limit(3).all()
    return render_template('index.html', featured_agents=featured_agents)

@main.route('/find agent')
def find_agent():
    users = Agent.query.all()
    return render_template('find_agent.html', users=users)

@main.route('/agent/<int:user_id>')
def agent_detail(user_id):
    user = Agent.query.get_or_404(user_id)
    return render_template('agent_details.html', user=user)

@main.route('/about')
def about():
    return render_template('about.html')


@main.route('/contact')
def contact():
    return render_template('contact.html')


@main.route('/search')
def search():
    return render_template('search.html')

@main.route('/agent/<name>')
def agent(name):
    user = Agent.query.filter_by(name=name).first()
    if user is None:
        abort(404)
    return render_template('agent.html', user=user)

@main.route('/edit_profile')
def edit_profile():
    form = EditProfileForm
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.description = form.description.data
        db.session.add(agent)
        db.session.commit()
        return redirect(url_for('.agent', name=current_user.name))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.description.data = current_user.description
    return render_template('edit_profile', form=form)