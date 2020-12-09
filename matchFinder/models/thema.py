from flask_sqlalchemy import *
from .. import db

class Thema(db.Model):
	__tablename__ = "thema"
	id = db.Column(db.Integer, primary_key=True)
	list_id = db.Column(db.Integer, db.ForeignKey("thema_lists.id"), nullable=False)
	thema_name = db.Column(db.String(80), nullable=False)
	tutor = db.Column(db.String(80))
	uhrzeit = db.Column(db.String(80))