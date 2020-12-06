from flask import (
    Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for, abort, current_app as app)
from . import db
from . import database_helper

bp = Blueprint('share', __name__, url_prefix='/share')

#make database entry, give link to enter site
@bp.route('/', methods=['GET', 'POST'])
def index():
	teilnehmer_list_name = request.form.get('members', None)
	thema_list_name = request.form.get('topics', None)
	id = database_helper.save_verteilung(teilnehmer_list_name, thema_list_name)

	return render_template('share.html', id=id)