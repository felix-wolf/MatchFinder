from flask import (
	Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for, abort, current_app as app)
import os
from werkzeug.utils import secure_filename
from . import matchCalculator
from . import results
from . import txt_parser
from . import database_helper


bp = Blueprint('edit', __name__, url_prefix='/edit')


@bp.before_request
def load_logged_in_user():
    if session.get('is_authenticated') != True:
        return redirect(url_for('home'))


@bp.route('/')
def index():
    return render_template('edit.html')