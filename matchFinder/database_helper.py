#from . import db
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy

def insert_participants(participants):
	db = SQLalchemy(app)
	#database = db.get_db()
	#cursor = database.cursor()
	#cursor.execute(
	#	'INSERT INTO member_list (name) VALUES (?)',
	#	(["test"])
	#)
	#id = cursor.lastrowid

	#for member in participants:
	#	matr_nr = member['matr_nr']
	#	last_name = member['last_name']
	#	first_name = member['first_name']
	#	cursor.execute(
	#		'INSERT INTO member (list_id, matr_nr, last_name, first_name) VALUES (?, ?, ?, ?)',
	#		(id, matr_nr, last_name, first_name)
	#		)
	#database.commit()
	return len(participants)