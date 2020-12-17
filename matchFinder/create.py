from flask import (
    Blueprint, Flask, render_template, session, redirect, url_for)
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
    valid_teilnehmer = []
    for teil in teilnehmer:
    	if teil.is_for_unprotected == False:
    		valid_teilnehmer.append(teil)
    return render_template('create.html', teilnehmer=valid_teilnehmer, themen=themen)