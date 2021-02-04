from flask import (
	Blueprint, redirect, render_template, request, url_for)

bp = Blueprint('home', __name__, url_prefix='/home')

@bp.route('/')
def index():
	return render_template('home.html')

@bp.route('/<message>')
def index_with_message(message):
	"""
	passes a message to the template to indicate success of certain
	operations
	"""

	return render_template('home.html', message=message)