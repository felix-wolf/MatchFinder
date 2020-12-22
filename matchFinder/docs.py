import functools
from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for)
import markdown
import os

bp = Blueprint('docs', __name__, url_prefix='/docs')

@bp.route('/')
def index():
	repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
	file = os.path.join(repo_path, 'README.md')
	with open(file, 'r') as f:
		html = markdown.markdown(f.read())
	return render_template('docs_overview.html', html = html)

@bp.route('/documentation')
def documentation():
	repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../documentation'))
	file = os.path.join(repo_path, 'dokumentation.md')
	with open(file, 'r') as f:
		html = markdown.markdown(f.read())
	return render_template('documentation.html', title="Dokumentation", html = html)

@bp.route('/specification')
def specification():
	repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../documentation'))
	file = os.path.join(repo_path, 'spezifikation.md')
	with open(file, 'r') as f:
		html = markdown.markdown(f.read())
	return render_template('documentation.html', title="Spezifikation", html = html)

@bp.route('/installation')
def installation():
	repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../documentation'))
	file = os.path.join(repo_path, 'installation.md')
	with open(file, 'r') as f:
		html = markdown.markdown(f.read())
	return render_template('documentation.html', title="Installation", html = html)