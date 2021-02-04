from flask_sqlalchemy import *
from .. import db

class Teilnehmer_List(db.Model):
	"""
	Database scheme for the teilnehmerList table.
	Has an id, a name and a boolean indicating whether the list
	is for an unprotected verteilung.
	TeilnehmerLists are referenced by entities of teilnehmer and verteilungen,
	this table definitions has backreferences for convenience, allowing to
	call teilnehmer_list.teilnehmer to access all teilnehmer that reference
	this particular list.
	"""

	__tablename__ = "teilnehmer_lists"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	teilnehmer = db.relationship("Teilnehmer", cascade="all,delete", backref="list", lazy=True)
	verteilungen = db.relationship("Verteilung", cascade="all,delete", backref="teilnehmer", lazy=True)
	is_for_unprotected = db.Column(db.Boolean, default=False)