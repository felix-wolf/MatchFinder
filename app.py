import os
from flask import *
from markupsafe import escape
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'many random bytes'

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)

@app.route('/docs/<page>/')
def doc(page):
	return 'hello, you are on page {}'.format(escape(page))

@app.route('/upload/', methods=['GET', 'POST'])
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
	return '''
		<!doctype html>
    	<title>Upload new File</title>
    	<h1>Upload new File</h1>
    	<form method=post enctype=multipart/form-data>
      		<input type=file name=file>
			<input type=submit value=Upload>
    	</form>
    '''

@app.errorhandler(404)
def pageNotFound(e):
	return render_template('404.html')


def allowedFile(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




