from flask import (
	Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for, abort, current_app as app)
import os
from werkzeug.utils import secure_filename
from . import matchCalculator
from . import results
from . import txt_parser
from . import database_helper


bp = Blueprint('preference', __name__, url_prefix='/preference')

@bp.route('/')
def index():
    return render_template('preference.html')

@bp.route('<verteilung_id>')
def set_preference(verteilung_id):
    return render_template('preference.html')