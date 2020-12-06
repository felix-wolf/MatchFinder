from flask_sqlalchemy import *
from .. import db

class Thema(db.Model):
	__tablename__ = "thema"
	id = db.Column(db.Integer, primary_key=True)
	stine_id = db.Column(db.Integer, nullable=False)
	list_id = db.Column(db.Integer, db.ForeignKey("thema_lists.id"), nullable=False)
	topic_name = db.Column(db.String(80), nullable=False)
	max_participants = db.Column(db.Integer, nullable=False, default=1)
	tutor_last_name = db.Column(db.String(80))
	tutor_first_name = db.Column(db.String(80))