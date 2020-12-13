from flask import (
    Blueprint, Flask, render_template)
from . import database_helper

bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.route('/')
def index():
    teilnehmer = database_helper.get_all_teilnehmer_lists()
    themen = database_helper.get_all_thema_lists()
    valid_teilnehmer = []
    for teil in teilnehmer:
    	if teil.is_for_unprotected == False:
    		valid_teilnehmer.append(teil)
    return render_template('upload.html', teilnehmer=valid_teilnehmer, themen=themen)