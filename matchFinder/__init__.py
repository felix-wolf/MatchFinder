import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, session, render_template, redirect, url_for, current_app as app
import hashlib
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


db = SQLAlchemy()
limiter = Limiter()

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    limiter.init_app(app)

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

    from . import create
    app.register_blueprint(create.bp)

    from .import share
    app.register_blueprint(share.bp)

    from . import preference
    app.register_blueprint(preference.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    db.init_app(app)

    return app

with create_app().app_context():
    from matchFinder.models import teilnehmer
    from matchFinder.models import teilnehmer_list
    from matchFinder.models import thema
    from matchFinder.models import thema_list
    from matchFinder.models import verteilung
    from matchFinder.models import password
    #db.drop_all()
    db.create_all()

    #keys = ["1234", "test"]
    #for key in keys:
    #    m = hashlib.sha256()
    #    m.update(key.encode('utf-8'))
    #    pw = password.Password(password=m.hexdigest())
    #    db.session.add(pw)
    #db.session.commit()

