import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app, db
from app.models import Location

"""script to add locations"""

app = create_app()

with app.app_context():
    locations = [
        'Eldoret',
        'Kiambu',
        'Nakuru',
        'Kitale',
        'Lamu',
        'Malindi'
    ]

    for location in locations:
        if not  Location.query.filter_by(name=location).first():
            location = Location(name=location)
            db.session.add(location)

    db.session.commit()
    print('Locations added successfully')