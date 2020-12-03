from flask import current_app as app
from flask_sqlalchemy import *
from app import db

Base = declarative_base()
#db = SQLAlchemy(app)

class Member(Base):
	id = Column(Integer, primary_key=True)
	list_id = Columm(Integer, nullable=False)
	first_name = Columm(String(80), nullable=False)
	last_name = Columm(String(80), nullable=False)
	matr_nr = Columm(Integer, nullable=False)

	def __repr__(self):
		return '<User %r' % self.username