from flask import (
    Blueprint, Flask, render_template, request, current_app as app)
from werkzeug.utils import secure_filename
import os
from . import database_helper
from . import matchCalculator
from . import helper


bp = Blueprint('evaluate', __name__, url_prefix='/evaluate')

@bp.route('/')
def index():
	verteilungen = database_helper.get_all_verteilungen()
	return render_template('evaluate.html', verteilungen=verteilungen)

@bp.route('/from_db', methods=['POST'])
def from_db():
    verteilung_id = request.form.get('verteilung', None)
    verteilung = database_helper.get_verteilung_by_id(verteilung_id)
    teilnehmer = verteilung.teilnehmer.teilnehmer
    thema_list = database_helper.get_thema_list_by_id(verteilung.thema_list_id)
    themen = []
    for thema in thema_list.themen:
        themen.append(thema.thema_name)
    teilnehmer_pref = []
    for teil in teilnehmer:
        praeferenz = database_helper.get_praeferenz_by_teilnehmer_id(teil.id)
        if (praeferenz == None):
            praeferenz = ""
            for index in range(len(thema_list.themen) - 1):
                praeferenz += ","
        else:
            praeferenz = praeferenz.praeferenzen
        local_teilnehmer_pref = []
        local_teilnehmer_pref.append(teil.first_name + " " + teil.last_name)
        praeferenz = praeferenz.split(',')
        for praef in praeferenz:
            converted_praef = helper.convert_praef_to_num(praef)
            local_teilnehmer_pref.append(converted_praef)
        teilnehmer_pref.append(local_teilnehmer_pref)
        print(local_teilnehmer_pref)
    assignments = matchCalculator.calculate_from_db(teilnehmer_pref, themen)
    assignments = helper.sort_by_median(assignments)
    return render_template('results.html', data=assignments)

@bp.route('csv_upload', methods=['POST'])
def csv_upload():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        assignments = matchCalculator.calculateFromCSV(uploaded_file)
        assignments = helper.sort_by_median(assignments)
    return render_template('results.html', data=assignments)
