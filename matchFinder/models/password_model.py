from flask_sqlalchemy import *
from .. import db

class Password(db.Model):
	"""
	Database scheme for a passwords table.
	Sets its name to 'passwords', the columns consist of an id and a password.
	The password is stored as a string but is always hashed by bcrypt before
	being stored in the database.
	"""

	__tablename__ = "passwords"
	id = db.Column(db.Integer, primary_key=True)
	password = db.Column(db.String(80), nullable=False)