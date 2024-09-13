import os
from flask import Blueprint, current_app, render_template, abort, flash, request, redirect, url_for
from app.models import Agent, Location, Message, Rating
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


    name_query = request.args.get('name', '')
    location_query = request.args.get('location', '')
    rating_query = request.args.get('rating', '')


    query_result = Agent.query.join(Location)


    if query:
        query_result = query_result.filter(
            (func.lower(Agent.name).like(f'%{query.lower()}%')) |
            (func.lower(Location.name).like(f'%{query.lower()}%'))
        )

    # Apply filters if they are provided
    if name_query:
        query_result = query_result.filter(func.lower(Agent.name).like(f'%{name_query.lower()}%'))

    if location_query:
        query_result = query_result.filter(func.lower(Location.name).like(f'%{location_query.lower()}%'))

    if rating_query:
        rating_value = float(rating_query)
        query_result = query_result.filter(
            Agent.id.in_(
                db.session.query(Rating.agent_id)
                .group_by(Rating.agent_id)
                .having(func.avg(Rating.value) >= rating_value)
            )
        )

    # Final result after applying search and filters
    users = query_result.all()

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
    avg_rating = user.average_rating()
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
    return render_template('agent_details.html', user=user, form=form, avg_rating=avg_rating)


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
    """deletes a message"""
    message = Message.query.get_or_404(message_id)
    agent = Agent.query.get_or_404(message.agent_id)
    if agent != current_user:
        abort(403)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted successfully.', 'success')
    return redirect(url_for('main.agent_messages', name=agent.name))

# route to handle rating submission
@main.route('/rate_agent/<name>', methods=['POST'])
def rate_agent(name):
    """submits user rating"""
    user = Agent.query.filter_by(name=name).first()
    if user is None:
        abort(404)
    rating_value = int(request.form['rating'])
    rating = Rating(value=rating_value, agent_id=user.id)
    db.session.add(rating)
    db.session.commit()
    flash('Your rating has been submitted!', 'success')
    return redirect(url_for('main.agent', name=user.name))



# edit profile route
@main.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """allows agent to edit profile"""
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
        return redirect(url_for('main.agent_details', name=current_user.name))
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