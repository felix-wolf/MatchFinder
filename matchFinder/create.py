from flask import (
	Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for, abort, current_app as app)
import os
from werkzeug.utils import secure_filename
from . import matchCalculator
from . import results
from . import txt_parser
from . import database_helper


bp = Blueprint('create', __name__, url_prefix='/create')


@bp.before_request
def load_logged_in_user():
    if session.get('is_authenticated') != True:
        return redirect(url_for('home'))


@bp.route('/')
def index():
    return render_template('create.html')

@bp.route('/teilnehmer', methods=['POST'])
def teilnehmer():
    uploaded_file = request.files['file']
    if (validate_file(uploaded_file)):
        list_name = request.form.get('list_name', 'error')
        teilnehmer = txt_parser.array_from_teilnehmer(uploaded_file)
        rtn = database_helper.save_teilnehmer(teilnehmer, list_name)
        if rtn:
            return redirect(url_for('create.index', items_saved=rtn))
        else:
            return redirect(url_for('create.index', items_saved=False))
    else:
        abort(400)
    return redirect(url_for('create.index', items_saved=False))

@bp.route('/themen', methods=['POST'])
def themen():
    uploaded_file = request.files['file']
    if (validate_file(uploaded_file)):
        list_name = request.form.get('themen_name', 'error')
        max_teilnehmer = request.form.get('max_teilnehmer', None)
        if max_teilnehmer == '':
            max_teilnehmer = None
        themen = txt_parser.array_from_themen(uploaded_file)
        rtn = database_helper.save_themen(themen, list_name, max_teilnehmer)
        if rtn:
            return redirect(url_for('create.index', items_saved=rtn))
        else:
            return redirect(url_for('create.index', items_saved=False))
    else:
        abort(400)
    return redirect(url_for('create.index', items_saved=False))

@bp.route('/themen_manually', methods=['POST'])
def themen_manually():
    number_of_themen = request.form.get('number_themen', None)
    if number_of_themen != None and int(number_of_themen) > 0:
        print(number_of_themen)

def validate_file(file):
    filename = secure_filename(file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return False
        return True
    return False