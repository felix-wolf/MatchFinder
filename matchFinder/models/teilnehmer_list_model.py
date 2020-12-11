from flask_sqlalchemy import *
from .. import db

class Teilnehmer_List(db.Model):
	__tablename__ = "teilnehmer_lists"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	teilnehmer = db.relationship("Teilnehmer", cascade="all,delete", backref="list", lazy=True)
	verteilungen = db.relationship("Verteilung", cascade="all,delete", backref="teilnehmer", lazy=True)