from flask import Blueprint, request, jsonify
from models.user import User  # Changed from relative to absolute import
from utils.database import db
from utils.security import hash_password, verify_password, create_jwt_token
from models.user import User          # ← Absolute
from utils.security import hash_password  # ← Absolute

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ['full_name', 'email', 'password', 'role']):
        return jsonify({'error': 'Missing fields'}), 400
    
 
    # Check if user exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 409
    
    # Create user
    new_user = User(
        full_name=data['full_name'],
        email=data['email'],
        password_hash=hash_password(data['password']),
        role='renter',  # Default role
        is_verified=True  # Auto-verify for now
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    user = User.query.filter_by(email=data['email']).first()
    if not user or not verify_password(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = create_jwt_token(user.id)
    return jsonify({'token': token, 'role': user.role}), 200