from flask import (
    Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for, abort, current_app as app)
from . import db

bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.route('/')
def index():
    from matchFinder.models import teilnehmer_list
    from matchFinder.models import thema_list
    members = teilnehmer_list.Teilnehmer_List.query.all()
    topics = thema_list.Thema_List.query.all()
    return render_template('upload.html', members=members, topics=topics)