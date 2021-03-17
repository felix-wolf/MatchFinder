from flask_sqlalchemy import *
from .. import db

class Verteilung(db.Model):
	"""
	Database scheme for the verteilung table.
	It references the teilnehmer and themen by their primary keys, has a convenience backref
	to the präferenzen
	"""

	__tablename__ = "verteilungen"
	id = db.Column(db.Integer, primary_key=True)
	min_votes = db.Column(db.Integer, default=1)
	name = db.Column(db.String(80), nullable=False, unique=True)
	editable = db.Column(db.Boolean, default=False)
	protected = db.Column(db.Boolean, default=True)
	veto_allowed = db.Column(db.Boolean, default=True)
	max_teilnehmer_per_thema = db.Column(db.Integer, default=1)
	thema_list_id = db.Column(db.Integer, db.ForeignKey("thema_lists.id"), nullable=False)
	teilnehmer_list_id = db.Column(db.Integer, db.ForeignKey("teilnehmer_lists.id"), nullable=False)
	praeferenzen = db.relationship("Praeferenz", cascade="all,delete", backref="verteilung", lazy=True)