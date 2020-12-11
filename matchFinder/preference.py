from flask import (
	Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for, abort, current_app as app)
import os
from werkzeug.utils import secure_filename
from . import matchCalculator
from . import results
from . import txt_parser
from . import database_helper


bp = Blueprint('preference', __name__, url_prefix='/preference')

@bp.route('<int:verteilung_id>')
def set_preference(verteilung_id):
	return render_template('validate.html', id=verteilung_id)


@bp.route('/validate/', methods=['POST'])
def validate():
	verteilung_id = request.form.get('id', None)
	matr_nr = request.form.get('matr_nr', None)
	if matr_nr.isdigit():
		print(verteilung_id)
		print(matr_nr)
		valid = database_helper.check_membership(verteilung_id, matr_nr)
		return render_template('preference.html')

	return render_template(
		'validate.html',
		id=verteilung_id,
		error="Matrikelnummer muss eine Zahl sein!"
		)
