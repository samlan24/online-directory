# create_admin.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Agent
from werkzeug.security import generate_password_hash
from app.config import Config

app = create_app()
app.app_context().push()

admin_email = Config.ADMIN_EMAIL
admin_user = Agent.query.filter_by(email=admin_email).first()

if not admin_user:
    admin_user = Agent(name='admin', email=admin_email, password_hash=generate_password_hash('password'), is_admin=True)
    db.session.add(admin_user)
else:
    admin_user.is_admin = True

db.session.commit()
print(f'Admin user with email {admin_email} created/updated successfully.')