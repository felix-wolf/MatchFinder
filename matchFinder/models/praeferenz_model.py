from flask_sqlalchemy import *
from .. import db

class Praeferenz(db.Model):
	__tablename__ = "praeferenzen"
	id = db.Column(db.Integer, primary_key=True)
	teilnehmer_id = db.Column(db.Integer, db.ForeignKey("teilnehmer.id"), nullable=False)
	verteilung_id = db.Column(db.Integer, db.ForeignKey("verteilungen.id"), nullable=False)
	praeferenzen = db.Column(db.String, nullable=False)