from flask import (
	Blueprint, Flask, redirect, render_template, request, url_for)
from . import database_helper
import qrcode
import base64
from PIL import Image
from io import BytesIO

bp = Blueprint('share', __name__, url_prefix='/share')

#make database entry, give link to enter site
@bp.route('/', methods=['GET', 'POST'])
def index():
	teilnehmer_list_name = request.form.get('teilnehmer', None)
	thema_list_name = request.form.get('thema', None)
	protected = request.form.get('protected', False)
	editable = request.form.get('editable', False)
	protected = True if protected == "on" else False
	editable = True if editable == "on" else False

	id = database_helper.save_verteilung(
		teilnehmer_list_name, thema_list_name,
		protected, editable)
	return redirect(url_for('share.show', verteilung_id=id))

@bp.route('/show/<int:verteilung_id>')
def show(verteilung_id):
	root_url = request.url_root
	url = root_url + 'preference?id=' + str(verteilung_id)
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_H,
		box_size=4,
		border=4,
		)

	qr.add_data(url)
	qr.make(fit=True)
	img = qr.make_image()

	buffered = BytesIO()
	img.save(buffered, format="PNG")
	img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
	return render_template('share.html', id=verteilung_id, img=img_str)
