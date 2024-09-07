import os
from flask import Blueprint, current_app, render_template, abort, flash, request, redirect, url_for
from app.models import Agent, Location, Appointment
from werkzeug.utils import secure_filename
from app.auth.forms import EditProfileForm, DeleteProfileForm, AppointmentForm
from flask_login import current_user, login_required, logout_user
from sqlalchemy import func
from app import db

""" Blueprint for main routes """
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


@main.route('/agent/<name>', methods=['GET', 'POST'])
def agent_detail(name):
    user = Agent.query.filter_by(name=name).first()
    if user is None:
        abort(404)

    form = AppointmentForm()

    if form.validate_on_submit():
        # Create new appointment
        appointment = Appointment(
            user_name=form.user_name.data,
            user_email=form.user_email.data,
            date=form.date.data,
            agent_id=user.id
        )
        db.session.add(appointment)
        db.session.commit()
        flash('Your appointment has been booked successfully!', 'success')
        return redirect(url_for('main.agent_details', name=user.name))

    return render_template('agent.html', user=user, form=form)


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
    return render_template('agent_details.html', user=user)

@main.route('/agent/<name>')
def agent_details(name):
    user = Agent.query.filter_by(name=name).first()
    if user is None:
        abort(404)
    return render_template('agent_details.html', user=user)



@main.route('/agent_profile/<int:user_id>')
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


@main.route('/appointments')
@login_required
def appointments():
    if not current_user.is_authenticated:
        flash('Please log in to access this page.', 'danger')
        return redirect(url_for('auth.login'))
    appointments = Appointment.query.filter_by(agent_id=current_user.id).all()
    return render_template('appointments.html', appointments=appointments)
