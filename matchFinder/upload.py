from flask import (
    Blueprint, Flask, render_template)
from . import database_helper

bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.route('/')
def index():
    teilnehmer = database_helper.get_all_teilnehmer_lists()
    themen = database_helper.get_all_thema_lists()
    return render_template('upload.html', teilnehmer=teilnehmer, themen=themen)