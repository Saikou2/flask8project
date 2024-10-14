# app/routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User, Book, Loan  # Utilisez le chemin relatif
from . import db
from .schemas import UserSchema, BookSchema, LoanSchema
from .utils import role_required


main = Blueprint('main', __name__)

# Route pour obtenir la liste des utilisateurs (accessible aux administrateurs)
@main.route('/admin/users', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_all_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    return jsonify(user_schema.dump(users)), 200

# Route pour créer un livre (accessible aux administrateurs et aux managers)
@main.route('/admin/create-book', methods=['POST'])
@jwt_required()
@role_required(['admin', 'manager'])
def create_book():
    """
    Créer un nouveau livre
    ---
    """
    data = request.get_json()

    if 'title' not in data or 'author' not in data:
        return jsonify({"message": "Titre et auteur sont requis."}), 400

    new_book = Book(
        title=data['title'],
        author=data['author']
    )
    db.session.add(new_book)
    db.session.commit()
    book_schema = BookSchema()
    return jsonify(book_schema.dump(new_book)), 201

# Route pour obtenir la liste des livres
@main.route('/books', methods=['GET'])
@jwt_required()
def get_books():
    """
    Obtenir la liste de tous les livres
    ---
    """
    books = Book.query.all()
    book_schema = BookSchema(many=True)
    return jsonify(book_schema.dump(books)), 200

@main.route('/loans', methods=['POST'])
@jwt_required()
def create_loan():
    """
    Créer un nouvel emprunt de livre
    ---
    """
    data = request.get_json()
    try:
        current_user_id = get_jwt_identity()  # Obtenir l'ID de l'utilisateur connecté
        new_loan = Loan(
            user_id=current_user_id,  # Associer l'emprunt à l'utilisateur
            book_id=data['book_id'],
            issue_date=data['issue_date'],
        )
        db.session.add(new_loan)
        db.session.commit()
        loan_schema = LoanSchema()
        return jsonify(loan_schema.dump(new_loan)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# Route pour retourner un livre
@main.route('/loans/return/<int:loan_id>', methods=['PUT'])
@jwt_required()
def return_loan(loan_id):
    """
    Retourner un livre emprunté
    ---
    """
    loan = Loan.query.get_or_404(loan_id)
    loan.return_date = request.json.get('return_date')  # Vous pouvez définir la date de retour
    db.session.commit()
    loan_schema = LoanSchema()
    return jsonify(loan_schema.dump(loan)), 200

@main.route('/loans/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_loans(user_id):
    """
    Obtenir la liste des emprunts pour un utilisateur spécifique
    ou tous les emprunts si l'utilisateur est un admin ou manager
    ---
    """
    current_user_id = get_jwt_identity()
    
    # Récupérer l'utilisateur actuel
    current_user = User.query.get(current_user_id)

    # Si l'utilisateur est un admin ou manager, retourner tous les emprunts
    if current_user.role in ['admin', 'manager']:
        loans = Loan.query.all()
    else:
        # Vérifier si l'utilisateur connecté correspond à l'utilisateur demandé
        if current_user_id != user_id:
            return jsonify({"message": "Accès refusé"}), 403
        loans = Loan.query.filter_by(user_id=user_id).all()
    
    loan_schema = LoanSchema(many=True)
    return jsonify(loan_schema.dump(loans)), 200
