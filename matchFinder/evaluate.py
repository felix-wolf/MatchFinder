from flask import (
    Blueprint, render_template, request, redirect, url_for,
    send_file, after_this_request, current_app as app)
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
        praeferenz = database_helper.get_praeferenz_by_teilnehmer_id_verteilung_id(teil.id, verteilung.id)
        if (praeferenz == None):
            praeferenzen = list(map(lambda x: "Keine Präferenz", thema_list.themen))
            praeferenz = helper.convert_preferences(praeferenzen)
        else:
            praeferenz = praeferenz.praeferenzen
        praeferenz = praeferenz.split(',')
        local_teilnehmer_pref = helper.duplicate_teilnehmer_praefs(
            [teil.first_name + " " + teil.last_name] + praeferenz, max_per)
        teilnehmer_pref.append(local_teilnehmer_pref)
    assignments = matchCalculator.calculate_from_db(teilnehmer_pref, themen)
    assignments = helper.sort_by_median(assignments)
    return render_template('results.html', data=assignments, name=verteilung.name)

@bp.route('csv_upload', methods=['POST'])
def csv_upload():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        name, file_ext = os.path.splitext(filename)
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        assignments = matchCalculator.calculateFromCSV(uploaded_file)
        assignments = helper.sort_by_median(assignments)
    return render_template('results.html', data=assignments, name=name)


@bp.route('export', methods=['GET', 'POST'])
def export():
    data_string = request.form.get('data', None)
    if data_string != None:
        data_string = data_string.replace('\'', '\"')
        data_json = json.loads(data_string)
        name = data_json["name"]
        data = data_json["data"]
        filename = "auswertung_von_" + name
        with open("verteilung.txt", 'w') as f:
            if data_json["type"] == "csv":
                filename += ".csv"
                f.write(helper.create_csv(data["studis"]))
            else:
                filename += ".txt"
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
        return send_file(path, attachment_filename=filename, as_attachment=True)
    return redirect(url_for("home.index"))