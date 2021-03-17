from flask import (Blueprint, redirect, render_template, request, session, url_for)
from . import database_helper
from io import BytesIO
from PIL import Image
import hashlib
import qrcode
import base64

bp = Blueprint('share', __name__, url_prefix='/share')

@bp.before_request
def check_status():
	"""
	If the user is unauthenticated,
	this method redirects to the homepage.
	Called before each request to this subdomain
	"""
	if session.get('is_authenticated') != True:
		return redirect(url_for('home.index'))

@bp.route('/', methods=['POST'])
def index():
	"""
	gathers information about the verteilung,
	sends them to the database helper to be saved.
	hashes the verteilungs_id. this is simply to stop users from guessing
	the underlying mechanics of referencing verteilungen.
	"""

	data = {}
	data["teilnehmer_list_id"] = request.form.get('teilnehmer', None)
	data["name"] = request.form.get('name', None)
	data["thema_list_id"] = request.form.get('thema', None)
	protected = request.form.get('protected', False)
	editable = request.form.get('editable', False)
	data["max_per_thema"] = request.form.get('max_per', 1)
	data["min_votes"] = request.form.get('min_votes', 1)
	veto_allowed = request.form.get('veto_allowed', True)
	data["protected"] = True if protected == "on" else False
	data["editable"] = True if editable == "on" else False
	data["veto_allowed"] = True if veto_allowed == "on" else False

	id, error = database_helper.save_verteilung(data)
	if error == None:
		hashed_verteilung_id = hashlib.sha256(str(id).encode()).hexdigest()
		return redirect(url_for('share.show', verteilung_id=hashed_verteilung_id))
	else:
		return redirect(url_for('create.index', error=error))

@bp.route('/show/<verteilung_id>')
def show(verteilung_id):
	"""
	generates a QR-Code to a verteilung,
	passes it with the template to be rendered.
	"""

	root_url = request.url_root
	url = root_url + 'preference/' + str(verteilung_id)
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_H,
		box_size=4,
		border=4)

	qr.add_data(url)
	qr.make(fit=True)
	img = qr.make_image()

	buffered = BytesIO()
	img.save(buffered, format="PNG")
	img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
	return render_template('share.html', id=verteilung_id, img=img_str)
