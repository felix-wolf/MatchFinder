from flask import (
    Blueprint, render_template, session, redirect, url_for)
from . import database_helper

bp = Blueprint('create', __name__, url_prefix='/create')

@bp.before_request
def load_logged_in_user():
    if session.get('is_authenticated') != True:
        return redirect(url_for('home.index'))

@bp.route('/')
def index():
    teilnehmer = database_helper.get_all_teilnehmer_lists()
    themen = database_helper.get_all_thema_lists()
    valid_teilnehmer = list(filter(lambda x: x.is_for_unprotected == False, teilnehmer))
    return render_template('create.html', teilnehmer=valid_teilnehmer, themen=themen)