from flask import (
	Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for, abort, current_app as app)
import os
from werkzeug.utils import secure_filename
from . import matchCalculator
from . import results
from . import txt_parser
from . import database_helper
from . import db


bp = Blueprint('edit', __name__, url_prefix='/edit')


@bp.before_request
def load_logged_in_user():
    if session.get('is_authenticated') != True:
        return redirect(url_for('home'))


@bp.route('/')
def index():

	from matchFinder.models import teilnehmer_list
	from matchFinder.models import thema_list
	from matchFinder.models import teilnehmer
	teilnehmer_list_entries = teilnehmer_list.Teilnehmer_List.query.all()
	teilnehmer_all = teilnehmer.Teilnehmer.query.all()
	thema_list_entries = thema_list.Thema_List.query.all()

	return render_template(
		'edit.html',
		teilnehmer_lists=teilnehmer_list_entries,
		teilnehmer=teilnehmer_all
		)