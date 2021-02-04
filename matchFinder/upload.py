from flask import (
	Blueprint, redirect, render_template, request,
    session, url_for, abort, current_app as app)
from werkzeug.utils import secure_filename
from matchFinder.forms import themen_form
from matchFinder.forms import teilnehmer_form
from . import database_helper
from . import txt_parser
import os

bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.before_request
def check_status():
    """
    If the user is unauthenticated,
    this method redirects to the homepage.
    Called before each request to this subdomain
    """
    if session.get('is_authenticated') != True:
        return redirect(url_for('home.index'))

@bp.route('/')
def index():
    return render_template('upload.html')

@bp.route('/', methods=['POST'])
def file():
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
        return redirect(url_for('upload.index', items_saved=rtn))
    else:
        abort(400)
    return redirect(url_for('upload.index', items_saved=False))


@bp.route('/themen_manually', methods=['POST'])
def themen_manually():
    themenform = themen_form.ThemenForm()
    if themenform.validate_on_submit():
        # form is filled out and valid

        rtn = database_helper.save_themen(
            themenform.themen.data,
            themenform.themen_name.data)
        return redirect(url_for('upload.index', items_saved=rtn))


    number_of_themen = request.form.get('number_themen', None)
    if number_of_themen != None and int(number_of_themen) > 0:
        for i in range(int(number_of_themen)):
            thema_form = themen_form.ThemaEntryForm()
            themenform.themen.append_entry(thema_form)
        return render_template('upload_themen.html', form=themenform)
    return redirect(url_for('upload.index'))

@bp.route('/teilnehmer_manually', methods=['POST'])
def teilnehmer_manually():
    teilnehmerform = teilnehmer_form.TeilnehmerForm()
    if teilnehmerform.validate_on_submit():
        # form is filled out and valid

        rtn = database_helper.save_teilnehmer(
            teilnehmerform.teilnehmer.data,
            teilnehmerform.teilnehmer_name.data)
        return redirect(url_for('upload.index', items_saved=rtn))

    number_of_teilnehmer = request.form.get('number_teilnehmer', None)
    if number_of_teilnehmer != None and int(number_of_teilnehmer) > 0:
        for i in range(int(number_of_teilnehmer)):
            single_teilnehmer_form = teilnehmer_form.TeilnehmerEntryForm()
            teilnehmerform.teilnehmer.append_entry(single_teilnehmer_form)
        return render_template('upload_teilnehmer.html', form=teilnehmerform)
    return redirect(url_for('upload.index'))


def validate_file(file):
    filename = secure_filename(file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['UPLOAD_EXTENSIONS']:
            return False
        return True
    return False