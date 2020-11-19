from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for)

bp = Blueprint('upload', __name__, url_prefix='/upload')

@bp.route('/', methods=['GET', 'POST'])
def upload():
	if request.method == 'POST':
		if 'file' not in request.files:
			flash('Not file part')
			return redirect(url_for('home'))
		file = request.files['file']
		if file.filename == '':
			flash('No selected File')
			return redirect(url_for('home'))
		if file and allowedFile(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], file))
			return redirect(url_for('home'))
		else:
			flash('Filetype not allowed')
			return redirect(url_for('home'))

	return render_template('upload.html')