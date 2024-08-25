from flask import Blueprint

# Import the blueprint from routes.py
from app.main.routes import main

# Ensure the blueprint is available for import
__all__ = ['main']