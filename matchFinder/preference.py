from flask import (
	Blueprint, Flask, redirect, render_template, request, url_for)
from . import database_helper
from . import limiter
import json
from matchFinder.models import praeferenz_model
from matchFinder.models import teilnehmer_model
import hashlib


bp = Blueprint('preference', __name__, url_prefix='/preference')

@bp.route('<verteilung_id>')
def set_preference(verteilung_id):
	verteilung = database_helper.get_verteilung_by_hashed_id(verteilung_id)
	if verteilung != None:
		return render_template('validate.html', id=verteilung_id,
			protected=True if verteilung.protected else False)
	else:
		return render_template('validate.html', id=verteilung_id,
			error="Keine gültige Verteilung!")


@bp.route('/validate/', methods=['POST'])
@limiter.limit("5 per minute", error_message="Too many requests! Try again later.")
def validate():
	data = request.form.get('data', None)
	obj = json.loads(data)
	hashed_verteilung_id = obj['id']
	protected = obj["protected"]
	if protected == "True":
		matr_nr = request.form.get('matr_nr', None)
		error, verteilung, teilnehmer = check_user_for_protected(matr_nr,
											hashed_verteilung_id)
		if error:
			return render_template('validate.html', id=verteilung_id,
					protected=protected, error=error)
		else:
			themen = database_helper.get_thema_list_by_id(verteilung.thema_list_id).themen
			return render_template("preference.html", teilnehmer=teilnehmer,
					themen=themen, verteilung_id=verteilung.id,
					veto_allowed=verteilung.veto_allowed, min_votes = verteilung.min_votes)
	else:
		first_name = request.form.get('first_name', None)
		last_name = request.form.get('last_name', None)
		last_name = "" if last_name == "" else last_name
		verteilung = database_helper.get_verteilung_by_hashed_id(hashed_verteilung_id)
		if verteilung != None:
			teilnehmer = teilnehmer_model.Teilnehmer(first_name=first_name, matr_nr=0,
				last_name=last_name, list_id=verteilung.teilnehmer_list_id)
			database_helper.insert_teilnehmer(teilnehmer)
			themen = database_helper.get_thema_list_by_id(verteilung.thema_list_id).themen
			return render_template("preference.html", teilnehmer=teilnehmer,
					themen=themen, verteilung_id=verteilung.id,
					veto_allowed=verteilung.veto_allowed, min_votes = verteilung.min_votes)
		return render_template('validate.html', id = hashed_verteilung_id,
			protected=False, error="error")



@bp.route('save', methods=['POST'])
def save():
	information_object = request.form.get('information', None)

	obj = json.loads(information_object)
	verteilung_id = obj["verteilung_id"]
	teilnehmer_id = obj["teilnehmer_id"]
	verteilung = database_helper.get_verteilung_by_id(verteilung_id)
	number_of_themen_in_verteilung = len(verteilung.thema_list.themen)
	preference_string = ""
	for index in range(number_of_themen_in_verteilung):
		preference = request.form.get(str(index + 1), None)
		if preference == "Keine Präferenz":
			preference = ""
		if preference == "Veto":
			preference = "2000"
		preference_string = preference_string + preference + ","
	preference_string = preference_string[:-1]
	praeferenz = praeferenz_model.Praeferenz(
		teilnehmer_id=teilnehmer_id,
		verteilung_id=verteilung_id,
		praeferenzen=preference_string)
	database_helper.insert_praeferenz(praeferenz)
	return redirect(url_for('home.index_with_message',
		message="Deine Präferenzen wurden gespeichert!"))

def check_user_for_protected(matr_nr, hashed_verteilung_id):
	if matr_nr != None and matr_nr.isdigit():
		verteilung, teilnehmer = database_helper.check_membership(hashed_verteilung_id, matr_nr)
		if verteilung != None and teilnehmer != None:
			return None, verteilung, teilnehmer
		else:
			return "Matrikelnummer ungültig!", None, None
	else:
		return "Matrikelnummer muss eine Zahl sein!", None, None