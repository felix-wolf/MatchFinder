from flask import Flask, session, render_template, abort, request, redirect, url_for, current_app as app
from flask_sqlalchemy import SQLAlchemy
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


db = SQLAlchemy()
limiter = Limiter(key_func=get_remote_address)
blocked_ip = []

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

    @app.before_request
    def block_ips():
        if session.get('ip_blocked') == True:
            abort(403)
        elif session.get('ip_blocked') == False:
            return
        if any(request.environ.get('REMOTE_ADDR') in entry for entry in blocked_ip):
            session['ip_blocked'] = True
            abort(403)
        else:
            session['ip_blocked'] = False

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

    from . import edit
    app.register_blueprint(edit.bp)

    db.init_app(app)

    from . import txt_parser
    blocked_ip = txt_parser.load_ips()

    return app

with create_app().app_context():
    #db.drop_all()
    db.create_all()

    from . import password_helper
    #password_helper.create_passwords()
