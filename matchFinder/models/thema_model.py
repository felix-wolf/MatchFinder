from flask_sqlalchemy import *
from .. import db

class Thema(db.Model):
	"""
	Database scheme for the thema table.
	It references the list of teilnehmer it belongs to via the list_id.
	"""

	__tablename__ = "thema"
	id = db.Column(db.Integer, primary_key=True)
	list_id = db.Column(db.Integer, db.ForeignKey("thema_lists.id"), nullable=False)
	thema_name = db.Column(db.String(80), nullable=False)
	betreuer = db.Column(db.String(80))
	zeit = db.Column(db.String(80))