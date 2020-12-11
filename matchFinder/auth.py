from flask import (
    Blueprint, Flask, flash, g, redirect, render_template, request, session, url_for, abort, current_app as app)
import hashlib
from . import db
from matchFinder.models import password
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from . import limiter
from . import password_helper


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/')
def index():
	return render_template('auth.html')

@bp.route('/validate', methods=['POST'])
@limiter.limit("5 per minute", error_message="Too many requests! Try again later.")
def validate():
	entered_pw = request.form.get('password', None)
	passwords = password.Password.query.all()
	if len(passwords) == 0:
		return render_template('auth.html', no_pws_found=True)
	for pw in passwords:
		if password_helper.check_password(entered_pw, pw.password):
			session['is_authenticated'] = True
			return render_template('home.html', is_valid=True)
	return render_template('auth.html', is_valid=False)

@bp.route('/logout')
def logout():
	session.clear()
	return render_template('home.html')