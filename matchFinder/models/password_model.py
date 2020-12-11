from flask_sqlalchemy import *
from .. import db

class Password(db.Model):
	__tablename__ = "passwords"
	id = db.Column(db.Integer, primary_key=True)
	password = db.Column(db.String(80), nullable=False)