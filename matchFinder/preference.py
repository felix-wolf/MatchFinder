from flask import (
	Blueprint, Flask, redirect, render_template, request, url_for)
from . import database_helper
from . import limiter
import json
from matchFinder.models import praeferenz_model


bp = Blueprint('preference', __name__, url_prefix='/preference')

@bp.route('<int:verteilung_id>')
def set_preference(verteilung_id):
	verteilung = database_helper.get_verteilung_by_id(verteilung_id)
	if verteilung != None:
		return render_template('validate.html', id=verteilung_id)
	else:
		return render_template('validate.html', id=verteilung_id, error="Keine gültige Verteilung!")


@bp.route('/validate/', methods=['POST'])
@limiter.limit("5 per minute", error_message="Too many requests! Try again later.")
def validate():
	verteilung_id = request.form.get('id', None)
	matr_nr = request.form.get('matr_nr', None)
	if matr_nr.isdigit():
		if verteilung_id != "":
			verteilung, teilnehmer = database_helper.check_membership(verteilung_id, matr_nr)
			if verteilung != None and teilnehmer != None:
				themen = database_helper.get_thema_list_by_id(verteilung.thema_list_id).themen
				return render_template(
					"preference.html",
					teilnehmer=teilnehmer,
					themen=themen,
					verteilung_id=verteilung_id)
			else:
				return redirect(url_for("preference.set_preference", verteilung_id=verteilung_id))
		else:
			return render_template(
				'validate.html',
				id=verteilung_id,
				error="Verteilung nicht gefunden!"
				)

	return render_template(
		'validate.html',
		id=verteilung_id,
		error="Matrikelnummer muss eine Zahl sein!"
		)

@bp.route('save', methods=['POST'])
def save():
	information_object = request.form.get('information', None)

	obj = json.loads(information_object)
	verteilung_id = obj["verteilung_id"]
	teilnehmer_id = obj["teilnehmer_id"]
	verteilung = database_helper.get_verteilung_by_id(verteilung_id)
	number_of_themen_in_verteilung = len(verteilung.thema_list.themen)
	preference_string=""
	for index in range(number_of_themen_in_verteilung):
		preference = request.form.get(str(index + 1), None)
		if preference == "Keine Präferenz":
			preference = ""
		preference_string = preference_string + preference + ","
	preference_string = preference_string[:-1]
	praeferenz = praeferenz_model.Praeferenz(
		teilnehmer_id=teilnehmer_id,
		verteilung_id=verteilung_id,
		praeferenzen=preference_string
		)
	database_helper.insert_praeferenz(praeferenz)
	return render_template('home.html')











