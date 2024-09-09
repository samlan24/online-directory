import os
from flask import Blueprint, current_app, render_template, abort, flash, request, redirect, url_for
from app.models import Agent, Location, Message
from werkzeug.utils import secure_filename
from app.auth.forms import EditProfileForm, DeleteProfileForm, MessageForm, DeleteMessageForm
from flask_login import current_user, login_required, logout_user
from sqlalchemy import func
from app import db

""" Blueprint for main routes """
main = Blueprint('main', __name__, template_folder='templates', static_folder='static')


# main route
@main.route('/')
def index():
    featured_agents = Agent.query.limit(3).all()
    return render_template('index.html', featured_agents=featured_agents)

# find agent route
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

# about route
@main.route('/about')
def about():
    return render_template('about.html')

# contact route
@main.route('/contact')
def contact():
    return render_template('contact.html')

# search route
@main.route('/search')
def search():
    return render_template('search.html')

# route to view public agent profile
@main.route('/public_agent_profile/<name>')
def public_agent_profile(name):
    user = Agent.query.filter_by(name=name).first()
    if user is None:
        abort(404)
    return render_template('public_agent_profile.html', user=user)

# agent route
@main.route('/agent/<name>', methods=['GET', 'POST'])
def agent(name):
    user = Agent.query.filter_by(name=name).first()
    if user is None:
        abort(404)
    form = MessageForm()
    if form.validate_on_submit():
        message = Message(
            email=form.email.data,
            agent_id=user.id,
            content=form.content.data
        )
        db.session.add(message)
        db.session.commit()
        flash('Your message has been sent successfully!', 'success')
        return redirect(url_for('main.public_agent_profile', name=user.name))
    return render_template('agent_details.html', user=user, form=form)


# agent details route
@main.route('/agent_details/<name>')
@login_required
def agent_details(name):
    user = Agent.query.filter_by(name=name).first()
    if user is None:
        abort(404)
    return render_template('agent.html', user=user)


# agent messages route
@main.route('/agent/<name>/messages')
@login_required
def agent_messages(name):
    user = Agent.query.filter_by(name=name).first()
    if user is None or user != current_user:
        abort(404)
    messages = Message.query.filter_by(agent_id=user.id).order_by(Message.timestamp.desc()).all()
    return render_template('agent_messages.html', user=user, messages=messages)

# deleting messages route
@main.route('/delete_message/<int:message_id>', methods=['POST'])
@login_required
def delete_message(message_id):
    message = Message.query.get_or_404(message_id)
    agent = Agent.query.get_or_404(message.agent_id)
    if agent != current_user:
        abort(403)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted successfully.', 'success')
    return redirect(url_for('main.agent_messages', name=agent.name))


# agent delete profile route
@main.route('/agent_profile/<int:user_id>')
@login_required
def profile(user_id):
    user = Agent.query.get_or_404(user_id)
    form = DeleteProfileForm()
    return render_template('agent.html', user=user, form=form)


# edit profile route
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

        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            form.image.data.save(image_path)
            current_user.image_url = 'uploads/' + filename

        db.session.commit()
        return redirect(url_for('main.agent', name=current_user.name))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.location.data = current_user.location
        form.description.data = current_user.description
    return render_template('edit_profile.html', form=form)

# delete profile route
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