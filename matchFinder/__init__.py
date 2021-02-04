from flask import (Flask, session, render_template, abort,
    request, redirect, url_for, current_app as app)
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
import os

# database reference
db = SQLAlchemy()
# initializes Flask-limiter
limiter = Limiter(key_func=get_remote_address)
# array holding all blacklisted ip addresses
blocked_ip = []


def create_app(test_config=None):
    """
    initlializes the flask app, loads configurations,
    registers blueprints, provides an endpoint for 404 errors.
    """


    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    limiter.init_app(app)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.before_request
    def block_ips():
        """
        before each request the app checks whether the users
        ip address is block from the service
        """

        if session.get('ip_blocked') == True:
            abort(403)
        elif session.get('ip_blocked') == False:
            return
        if any(request.environ.get('REMOTE_ADDR') in entry for entry in blocked_ip):
            session['ip_blocked'] = True
            abort(403)
        else:
            session['ip_blocked'] = False

    @app.errorhandler(404)
    def page_not_found(e):
        """
        generic error handler
        """

        return render_template('404.html')

    @app.route('/')
    def index():
        """
        redirects call to index page to /home
        """

        return redirect(url_for('home.index'))

    from . import home
    app.register_blueprint(home.bp)

    from . import upload
    app.register_blueprint(upload.bp)

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

    from . import evaluate
    app.register_blueprint(evaluate.bp)

    db.init_app(app)

    from . import txt_parser
    blocked_ip = txt_parser.load_values_from_file('list_of_blocked_ips.txt')

    return app

with create_app().app_context():
    """
    initializes the database
    """

    from . import database_helper
    database_helper.init_db()