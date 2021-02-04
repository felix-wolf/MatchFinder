from flask import (
    Blueprint, render_template, session, redirect, url_for)
from . import database_helper

# blueprint for /create subpage

bp = Blueprint('create', __name__, url_prefix='/create')

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
	"""
	Renders the template, passes all teilnehmerLists
	and themenLists to the template to be displayed
	Of the teilnehmerLists, only those that are for the protected verteilungen
	are passed.
	"""
	teilnehmer = database_helper.get_all_teilnehmer_lists()
	themen = database_helper.get_all_thema_lists()
	valid_teilnehmer = list(filter(lambda x: x.is_for_unprotected == False, teilnehmer))
	return render_template('create.html', teilnehmer=valid_teilnehmer, themen=themen)