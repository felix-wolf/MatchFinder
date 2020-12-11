from flask import (
    Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for, abort, current_app as app)
from . import db
from . import database_helper

bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.route('/')
def index():
    members = database_helper.get_all_teilnehmer_lists()
    topics = database_helper.get_all_thema_lists()
    return render_template('upload.html', members=members, topics=topics)