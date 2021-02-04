from flask_sqlalchemy import *
from .. import db

class Praeferenz(db.Model):
	"""
	Database scheme for the Präferenzen table.
	Holds references to a single teilnehmer and a verteilung,
	stores the präferenzen as comma seperated values.
	"""

	__tablename__ = "praeferenzen"
	id = db.Column(db.Integer, primary_key=True)
	teilnehmer_id = db.Column(db.Integer, db.ForeignKey("teilnehmer.id"), nullable=False)
	verteilung_id = db.Column(db.Integer, db.ForeignKey("verteilungen.id"), nullable=False)
	praeferenzen = db.Column(db.String, nullable=False)