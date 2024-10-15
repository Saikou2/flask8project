# create_users.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User # type: ignore
from werkzeug.security import generate_password_hash

# Initialiser l'application et le contexte de la base de données
app = create_app()
app.app_context().push()

# Vérifiez si les utilisateurs admin et manager existent déjà
admin_user = User.query.filter_by(username='admin').first()
manager_user = User.query.filter_by(username='manager').first()

# Si l'administrateur n'existe pas, le créer
if not admin_user:
    admin_user = User(
        username='admin',
        email='admin@gmail.com',
        password=generate_password_hash('adminpassword'),  # Hacher le mot de passe
        role='admin'
    )
    db.session.add(admin_user)
    print("Administrateur créé avec succès.")

# Si le manager n'existe pas, le créer
if not manager_user:
    manager_user = User(
        username='manager',
        email='manager@gmail.com',
        password=generate_password_hash('managerpassword'),
        role='manager'
    )
    db.session.add(manager_user)
    print("Manager créé avec succès.")

# Valider les modifications dans la base de données
db.session.commit()
