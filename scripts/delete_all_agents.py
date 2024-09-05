# delete_all_agents.py
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import Agent

app = create_app()
app.app_context().push()

# Delete all records in the agents table
db.session.query(Agent).delete()
db.session.commit()

print("All records in the agents table have been deleted.")