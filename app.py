import os
from flask import *
from markupsafe import escape
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSION = {'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)

@app.route('/docs/<page>/')
def doc(page):
	return 'hello, you are on page {}'.format(escape(page))

@app.route('/upload/')
def upload():
	return 'upload'

@app.errorhandler(404)
def pageNotFound(e):
	return render_template('404.html') #redirect(url_for('home'))