from flask import (
    Blueprint, redirect, render_template, request, session, url_for)
from flask_limiter.util import get_remote_address
from flask_limiter import Limiter
from . import database_helper
from . import password_helper
from . import limiter
import hashlib

# blueprint for /auth subpage

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/')
def index():
	"""
	renders the html template
	"""

	return render_template('auth.html')

@bp.route('/validate', methods=['POST'])
@limiter.limit("5 per minute",
	error_message="Too many requests! Try again later.")
def validate():
	"""
	Called when a password is entered.
	the function checks if the entered password
	matches a password in the database.
	If true, the user is marked as authenticated via the session
	cookie.
	"""

	entered_pw = request.form.get('password', None)
	passwords = database_helper.get_all_passwords()
	if len(passwords) == 0:
		return render_template('auth.html', no_pws_found=True)
	validPasswords = list(filter(
		lambda x: password_helper.check_password(entered_pw, x.password),
		passwords))
	if len(validPasswords) == 1:
		session['is_authenticated'] = True
		return redirect(url_for('home.index_with_message',
			message="Authentifizierung erfolgreich!"))
	return render_template('auth.html', is_valid=False)

@bp.route('/logout')
def logout():
	"""
	Called when 'ausloggen' is clicked,
	marks the user as unauthorized via the session cookie
	"""
	session['is_authenticated'] = False
	return redirect(url_for('home.index_with_message',
		message="Du wurdest erfolgreich ausgeloggt!"))