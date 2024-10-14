# app/utils.py
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from .models import User

def role_required(roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if not user or user.role not in roles:
                return jsonify({"message": "Accès refusé : rôle insuffisant"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator
