from flask import (
	Blueprint, redirect, render_template, session, url_for)
from . import database_helper
import hashlib
import json

bp = Blueprint('edit', __name__, url_prefix='/edit')

@bp.before_request
def check_status():
	"""
	If the user is unauthenticated,
	this method redirects to the homepage.
	Called before each request to this subdomain
	"""
	if session.get('is_authenticated') != True:
		return redirect(url_for('home.index'))

@bp.route('/')
def index():

	teilnehmer_list_entries = database_helper.get_all_teilnehmer_lists()
	teilnehmer_all = database_helper.get_all_teilnehmer()
	thema_list_entries = database_helper.get_all_thema_lists()
	thema_all = database_helper.get_all_themen()
	verteilungen_all = database_helper.get_all_verteilungen()

	return render_template(
		'edit.html',
		teilnehmer_lists=teilnehmer_list_entries,
		teilnehmer=teilnehmer_all,
		thema_lists=thema_list_entries,
		themen=thema_all,
		verteilungen=verteilungen_all)

@bp.route('/delete/<int:id>/<type>', methods=["GET"])
def delete(id, type):

	if type == "teilnehmer":
		database_helper.delete_teilnehmer_list_by_id(id)

	if type == "thema":
		database_helper.delete_thema_list_by_id(id)

	return redirect(url_for("edit.index"))

@bp.route('/action/<int:verteilung_id>/<action>', methods=["GET"])
def action(verteilung_id, action):

	if action == 'löschen':
		database_helper.delete_verteilung_by_id(verteilung_id)

	if action == 'teilen':
		hashed_verteilung_id = hashlib.sha256(str(verteilung_id).encode()).hexdigest()
		return redirect(url_for('share.show', verteilung_id=hashed_verteilung_id))

	return redirect(url_for("edit.index"))