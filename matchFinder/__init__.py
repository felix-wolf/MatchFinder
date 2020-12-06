import os
#from . import db
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, redirect, url_for


db = SQLAlchemy()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    #from pprint import pprint
    #pprint(app.config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def home():
        return render_template('home.html')

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html')

    from . import upload
    app.register_blueprint(upload.bp)

    from . import docs
    app.register_blueprint(docs.bp)

    from . import results
    app.register_blueprint(results.bp)
    from matchFinder.models import member

    db.init_app(app)

    return app