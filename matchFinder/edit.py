from flask import (
	Blueprint, Flask, redirect, render_template, request, session, url_for)
from . import database_helper
import json


bp = Blueprint('edit', __name__, url_prefix='/edit')


@bp.before_request
def load_logged_in_user():
    if session.get('is_authenticated') != True:
        return redirect(url_for('home'))


@bp.route('/')
def index():

	teilnehmer_list_entries = database_helper.get_all_teilnehmer_lists()
	teilnehmer_all = database_helper.get_all_teilnehmer()
	thema_list_entries = database_helper.get_all_thema_lists()
	thema_all = database_helper.get_all_themen()

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
		database_helper.delete_teilnehmer_list_by_id(obj["id"])

	if obj["type"] == "thema":
		database_helper.delete_thema_list_by_id(obj["id"])

	return redirect(url_for("edit.index"))