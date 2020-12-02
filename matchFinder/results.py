from flask import (
	Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for, abort)
import json
import numpy as np


app = Flask(__name__)

bp = Blueprint('results', __name__, url_prefix='/results')

@bp.route('/')
def index():
	return render_template('404.html')

@bp.route('present/<assignments>')
def present(assignments):
    print(assignments)
    #assignments = [1, 2, 3]
    assignments = np.array(list(assignments))
    return render_template('results.html', data=map(json.dumps, assignments))