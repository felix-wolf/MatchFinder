from flask import (
    Blueprint, Flask, render_template, request, redirect, url_for, send_file, after_this_request, current_app as app)
from werkzeug.utils import secure_filename
import os
from . import database_helper
from . import matchCalculator
from . import helper
import json


bp = Blueprint('evaluate', __name__, url_prefix='/evaluate')

@bp.route('/')
def index():
	verteilungen = database_helper.get_all_verteilungen()
	return render_template('evaluate.html', verteilungen=verteilungen)

@bp.route('/from_db', methods=['POST'])
def from_db():
    verteilung_id = request.form.get('verteilung', None)
    verteilung = database_helper.get_verteilung_by_id(verteilung_id)
    max_per = verteilung.max_teilnehmer_per_thema
    teilnehmer = verteilung.teilnehmer.teilnehmer
    thema_list = database_helper.get_thema_list_by_id(verteilung.thema_list_id)
    themen = list(map(lambda x: x.thema_name, thema_list.themen))
    themen = helper.duplicate_themen(themen, max_per)
    teilnehmer_pref = []
    for teil in teilnehmer:
        praeferenz = database_helper.get_praeferenz_by_teilnehmer_id(teil.id)
        if (praeferenz == None):
            # TODO: check if this works
            praeferenzen = []
            for index in range(len(thema_list.themen)):
                praeferenzen.append("Keine Präferenz")
            praeferenz = helper.convert_preferences(praeferenzen)
        else:
            praeferenz = praeferenz.praeferenzen
        praeferenz = praeferenz.split(',')
        local_teilnehmer_pref = helper.duplicate_teilnehmer_praefs(
            [teil.first_name + " " + teil.last_name] + praeferenz, max_per)
        teilnehmer_pref.append(local_teilnehmer_pref)
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


@bp.route('export', methods=['GET', 'POST'])
def export():
    data_string = request.form.get('data', None)
    if data_string != None:
        data_string = data_string.replace('\'', '\"')
        data_json = json.loads(data_string)
        data = data_json["data"]
        with open("verteilung.txt", 'w') as f:
            if data_json["type"] == "csv":
                f.write(helper.create_csv(data["studis"]))
            else:
                f.write(helper.create_txt(data["studis"]))
        path = "../verteilung.txt"
        @after_this_request
        def remove_file(response):
            try:
                dirname = os.path.dirname(__file__)
                filename = os.path.join(dirname, path)
                os.remove(filename)
            except Exception as error:
                print("Error removing or closing downloaded file handle", error)
            return response
        return send_file(path, attachment_filename="verteilung.csv")
    return redirect(url_for("home.index"))