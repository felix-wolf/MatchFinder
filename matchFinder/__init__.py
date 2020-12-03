import os

from flask import Flask, render_template, redirect, url_for

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'matchFinder.sqlite'),
    )

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

    from . import db
    db.init_app(app)

    from . import preference
    app.register_blueprint(preference.bp)

    from . import upload
    app.register_blueprint(upload.bp)

    from . import docs
    app.register_blueprint(docs.bp)

    from . import results
    app.register_blueprint(results.bp)

    return app