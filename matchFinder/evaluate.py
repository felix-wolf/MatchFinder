from flask import (
    Blueprint, Flask, render_template)
from . import database_helper

bp = Blueprint('evaluate', __name__, url_prefix='/evaluate')

@bp.route('/')
def index():
    return render_template('evaluate.html')