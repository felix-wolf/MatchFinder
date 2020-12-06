from flask import (
	Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for, abort, current_app as app)
import os
from werkzeug.utils import secure_filename
from . import matchCalculator
from . import results
from . import txt_parser
from . import database_helper


bp = Blueprint('create', __name__, url_prefix='/create')

@bp.route('/')
def index():
    return render_template('create.html')

@bp.route('/csv', methods=['POST'])
def csv():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        assignments = matchCalculator.calculateFromCSV(uploaded_file)
    return redirect(url_for('results.present', assignments=assignments))


@bp.route('/participants', methods=['POST'])
def participants():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        participants = txt_parser.array_from_participants(uploaded_file)
        items_saved = database_helper.insert_participants(participants)
        print(items_saved)
    return redirect(url_for('upload.index', msg=items_saved))

@bp.route('/topics', methods=['POST'])
def topics():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            abort(400)
        assignments = matchCalculator.calculateFromCSV(uploaded_file)
    return redirect(url_for('results.present', assignments=assignments))

@bp.route('/create_assignment', methods=['POST'])
def create_assignment():
    print("create")