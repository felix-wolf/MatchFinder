from flask import current_app
from flask_sqlalchemy import *
from .. import db

class Member(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	list_id = db.Column(db.Integer, nullable=False)
	first_name = db.Column(db.String(80), nullable=False)
	last_name = db.Column(db.String(80), nullable=False)
	matr_nr = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return '<User %r' % self.username