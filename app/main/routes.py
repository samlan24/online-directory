from flask import Blueprint, render_template, abort, flash, request, redirect, url_for
from app.models import Agent, Location, Role
from app.auth.forms import EditProfileForm, DeleteProfileForm
from flask_login import current_user, login_required, logout_user
from .decorators import admin_required
from app import db
from sqlalchemy import func

""" blueprint for main routes """

main = Blueprint('main', __name__, template_folder='templates', static_folder='static')

@main.route('/')
def index():
    featured_agents = Agent.query.limit(3).all()
    return render_template('index.html', featured_agents=featured_agents)


@main.route('/find_agent', methods=['GET', 'POST'])
def find_agent():
    query = request.args.get('query', '')
    if query:
        users = Agent.query.join(Location).filter(
            (func.lower(Agent.name).like(f'%{query.lower()}%')) |
            (func.lower(Location.name).like(f'%{query.lower()}%'))
        ).all()
    else:
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

@main.route('/agent/<int:user_id>')
@login_required
def profile(user_id):
    user = Agent.query.get_or_404(user_id)
    form = DeleteProfileForm()
    return render_template('agent.html', user=user, form=form)

@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    form.location.choices = [(location.id, location.name) for location in Location.query.all()]
    if form.validate_on_submit():
        location = Location.query.get(form.location.data)
        current_user.name = form.name.data
        current_user.location = location
        current_user.description = form.description.data
        db.session.commit()
        return redirect(url_for('main.agent', name=current_user.name))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.location.data = current_user.location
        form.description.data = current_user.description
    return render_template('edit_profile.html', form=form)


@main.route('/delete_profile', methods=['POST', 'GET'])
@login_required
def delete_profile():
    form = DeleteProfileForm()
    if form.validate_on_submit():
        agent = Agent.query.get_or_404(current_user.id)
        db.session.delete(agent)
        db.session.commit()
        logout_user()
        flash("Your profile has been deleted")
        return redirect(url_for('main.index'))
    return render_template('delete_profile.html', form=form)

