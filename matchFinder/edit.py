from flask import (
	Blueprint, Flask, redirect, render_template, request, session, url_for)
from . import db
from matchFinder.models import teilnehmer_list
from matchFinder.models import teilnehmer
from matchFinder.models import thema_list
from matchFinder.models import thema
import json


bp = Blueprint('edit', __name__, url_prefix='/edit')


@bp.before_request
def load_logged_in_user():
    if session.get('is_authenticated') != True:
        return redirect(url_for('home'))


@bp.route('/')
def index():

	teilnehmer_list_entries = teilnehmer_list.Teilnehmer_List.query.all()
	teilnehmer_all = teilnehmer.Teilnehmer.query.all()
	thema_list_entries = thema_list.Thema_List.query.all()
	thema_all = thema.Thema.query.all()
	print(thema_all)

	return render_template(
		'edit.html',
		teilnehmer_lists=teilnehmer_list_entries,
		teilnehmer=teilnehmer_all,
		thema_lists=thema_list_entries,
		themen=thema_all,
		)

@bp.route('/delete', methods=["POST"])
def delete():

	id = request.form.get('id', None)
	obj = json.loads(id)
	if obj["type"] == "teilnehmer":
		teilnehmer_to_delete = teilnehmer_list.Teilnehmer_List.query.filter_by(id=obj["id"]).first()
		db.session.delete(teilnehmer_to_delete)
		db.session.commit()

	if obj["type"] == "thema":
		thema_to_delete = thema_list.Thema_List.query.filter_by(id=obj["id"]).first()
		db.session.delete(thema_to_delete)
		db.session.commit()


	return redirect(url_for("edit.index"))