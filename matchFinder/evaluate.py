from flask import (
    Blueprint, Flask, render_template, request, current_app as app)
from werkzeug.utils import secure_filename
import os
from . import database_helper
from . import matchCalculator
from statistics import median
from operator import itemgetter

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
        local_teilnehmer_pref = []
        local_teilnehmer_pref.append(teil.first_name + " " + teil.last_name)
        praeferenz = praeferenz.praeferenzen.split(',')
        for praef in praeferenz:
            local_teilnehmer_pref.append(convert_praef_to_num(praef))
        teilnehmer_pref.append(local_teilnehmer_pref)
    assignments = matchCalculator.calculate_from_db(teilnehmer_pref, themen)
    assignments = sort_by_median(assignments)
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
        assignments = sort_by_median(assignments)
    return render_template('results.html', data=assignments)

def convert_praef_to_num(praef):
    if praef == "Erstwahl":
        return 1
    if praef == "Zweitwahl":
        return 2
    if praef == "Drittwahl":
        return 3
    if praef == "Viertwahl":
        return 4
    if praef == "Fünftwahl":
        return 5
    if praef == "Sechstwahl":
        return 6
    if praef == "Siebtwahl":
        return 7
    if praef == "Achtwahl":
        return 8
    if praef == "Neuntwahl":
        return 9
    if praef == "Zehntwahl":
        return 10
    return 1000

def sort_by_median(assignments):
    medians = []
    for index, item in enumerate(assignments):
        list = []
        median_with_index = []
        for studi in item["studis"]:
            list.append(studi[2])
        local_median = median(list)
        median_with_index.append(local_median)
        median_with_index.append(index)
        medians.append(median_with_index)
    medians = sorted(medians, key=itemgetter(0))
    index_of_items_sorted_by_medians = []
    for med in medians:
        index_of_items_sorted_by_medians.append(med[1])
    sorted_assignments = []
    for index in index_of_items_sorted_by_medians:
        sorted_assignments.append(assignments[index])
    return sorted_assignments




