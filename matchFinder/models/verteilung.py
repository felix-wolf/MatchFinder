from flask_sqlalchemy import *
from .. import db

class Verteilung(db.Model):
	__tablename__ = "verteilungen"
	id = db.Column(db.Integer, primary_key=True)
	thema_list_id = db.Column(db.Integer, db.ForeignKey("thema_lists.id"), nullable=False)
	teilnehmer_list_id = db.Column(db.Integer, db.ForeignKey("teilnehmer_lists.id"), nullable=False)