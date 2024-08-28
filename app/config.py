import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:your_new_password@localhost:3306/trial'
    SQLALCHEMY_TRACK_MODIFICATIONS = False