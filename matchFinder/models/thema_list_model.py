from flask_sqlalchemy import *
from .. import db

class Thema_List(db.Model):
	"""
	Database scheme for the themaList table.
	Consists of an id, a name and backref to the themen and verteilungen
	that references this thema_list by its primary key (convenience).
	This allows the call of thema_list.themen to access all themen
	that reference this particular list.
	"""

	__tablename__ = "thema_lists"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	themen = db.relationship("Thema", cascade="all,delete", backref="list", lazy=True)
	verteilungen = db.relationship("Verteilung", cascade="all,delete", backref="thema_list", lazy=True)