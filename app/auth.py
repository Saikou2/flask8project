# app/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from .models import db, User

auth = Blueprint('auth', __name__)

# Inscription d'un utilisateur
@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "L'utilisateur existe déjà"}), 400

    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],  # Le mot de passe est haché lors de la création de l'utilisateur
        # role=data.get('role', 'user')  # Par défaut, le rôle est 'user'
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Utilisateur créé avec succès"}), 201

# Connexion de l'utilisateur
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print("Données reçues :", data)

    user = User.query.filter_by(email=data['email']).first()
    print("Utilisateur trouvé :", user)

    if not user  or not user.check_password(data['password']):
        print("Échec de la connexion : Nom d'utilisateur ou mot de passe incorrect")
        return jsonify({"message": "Nom d'utilisateur ou mot de passe incorrect"}), 401

    # Création du jeton JWT
    access_token = create_access_token(identity=user.id)
    print("Connexion réussie pour l'utilisateur :", user.username)
    return jsonify({"access_token": access_token, "role": user.role}), 200


# Route protégée par JWT pour obtenir le profil
@auth.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "Utilisateur non trouvé"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }), 200
