from flask_sqlalchemy import *
from .. import db

class Thema_List(db.Model):
	__tablename__ = "thema_lists"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	themen = db.relationship("Thema", cascade="all,delete", backref="list", lazy=True)