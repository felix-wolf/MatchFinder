from flask import (
	Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for, abort, current_app as app)
import os
from werkzeug.utils import secure_filename
from . import matchCalculator
from . import results
from . import txt_parser
from . import database_helper
from . import limiter


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
				return render_template("preference.html", teilnehmer=teilnehmer, themen=themen)
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

@bp.route('save')
def save():
	return render_template('home.html')