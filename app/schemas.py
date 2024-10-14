# app/schemas.py
from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    email = fields.Str()
    role = fields.Str()

class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    author = fields.Str(required=True)
    loans = fields.Nested('LoanSchema', many=True, exclude=('book',))

class LoanSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()  # Associe l'emprunt à l'utilisateur par ID
    book_id = fields.Int()
    issue_date = fields.DateTime()
    return_date = fields.DateTime()
    user = fields.Nested(UserSchema)
    book = fields.Nested('BookSchema', only=['id', 'title', 'author']) 