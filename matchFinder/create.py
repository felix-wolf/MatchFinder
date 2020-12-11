from flask import (
	Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for, abort, current_app as app)
import os
from werkzeug.utils import secure_filename
from . import matchCalculator
from . import results
from . import txt_parser
from . import database_helper
from matchFinder.forms import thema_form as themen_form


bp = Blueprint('create', __name__, url_prefix='/create')


@bp.before_request
def load_logged_in_user():
    if session.get('is_authenticated') != True:
        return redirect(url_for('home'))


@bp.route('/')
def index():
    return render_template('create.html')


@bp.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    if (validate_file(uploaded_file)):
        teilnehmer_name = request.form.get('teilnehmer_name', None)
        themen_name = request.form.get('themen_name', None)
        if themen_name == None:
            teilnehmer = txt_parser.array_from_teilnehmer(uploaded_file)
            rtn = database_helper.save_teilnehmer(teilnehmer, teilnehmer_name)
        elif teilnehmer_name == None:
            themen = txt_parser.array_from_themen(uploaded_file)
            rtn = database_helper.save_themen(themen, themen_name)
        return redirect(url_for('create.index', items_saved=rtn))
    else:
        abort(400)
    return redirect(url_for('create.index', items_saved=False))


@bp.route('/themen_manually', methods=['POST'])
def themen_manually():
    themenform = themen_form.ThemenForm()
    if themenform.validate_on_submit():
        # form is filled out and valid

        rtn = database_helper.save_themen(
            themenform.themen.data,
            themenform.themen_name.data)
        return redirect(url_for('create.index', items_saved=rtn))


    number_of_themen = request.form.get('number_themen', None)
    if number_of_themen != None and int(number_of_themen) > 0:
        for i in range(int(number_of_themen)):
            thema_form = themen_form.ThemaEntryForm()
            themenform.themen.append_entry(thema_form)
        return render_template('create_themen.html', form=themenform)
    return redirect(url_for('create.index'))


def validate_file(file):
    filename = secure_filename(file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return False
        return True
    return False