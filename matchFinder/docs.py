import functools
from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for)

from matchFinder.db import get_db
import markdown
import os

bp = Blueprint('docs', __name__, url_prefix='/docs')

@bp.route('/')
def docs():
	repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
	file = os.path.join(repo_path, 'README.md')
	with open(file, 'r') as f:
		html = markdown.markdown(f.read())
	return render_template('docs.html', html = html)