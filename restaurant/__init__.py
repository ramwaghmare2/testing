from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('restaurant.config.Config')

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from . import models, routes  # Import routes and models
        db.create_all()  # Create database tables for our data models

        return app
