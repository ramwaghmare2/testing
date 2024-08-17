from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from .models import User, Restaurant, Menu, Review
from . import create_app

app = create_app()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    is_admin = data.get('is_admin', False)

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 409

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, is_admin=is_admin)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity={'username': user.username, 'is_admin': user.is_admin})
    return jsonify({'access_token': access_token}), 200

@app.route('/restaurants', methods=['POST'])
@jwt_required()
def create_restaurant():
    identity = get_jwt_identity()
    if not identity.get('is_admin'):
        return jsonify({'message': 'Admin access required'}), 403

    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    new_restaurant = Restaurant(name=name, description=description)
    db.session.add(new_restaurant)
    db.session.commit()

    return jsonify({'message': 'Restaurant created successfully'}), 201

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    result = [{'id': r.id, 'name': r.name, 'description': r.description} for r in restaurants]
    return jsonify(result), 200

# Define similar routes for Menu and Review

if __name__ == '__main__':
    app.run(debug=True)
