from flask import (
    Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for, abort, current_app as app)
import hashlib
from . import db
from matchFinder.models import password
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from . import limiter


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/')
def index():
	return render_template('auth.html')

@bp.route('/validate', methods=['POST'])
@limiter.limit("5 per minute", error_message="Too many requests! Try again later.")
def validate():
	pw = request.form.get('password', None)
	passwords = password.Password.query.all()
	m = hashlib.sha256()
	m.update(pw.encode('utf-8'))
	pw_hash = m.hexdigest()
	for pw_for in passwords:
		if pw_hash == pw_for.password:
			session['is_authenticated'] = True
			return render_template('auth.html' , is_valid=True)
	return render_template('auth.html', is_valid=False)

@bp.route('/logout')
def logout():
	session.clear()
	return render_template('auth.html')