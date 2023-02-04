import logging
import time

from flask import Flask
from flask import g, request
from flask.logging import default_handler
from app.extensions import db

from app.config import Config
from app.main import bp_app_routes
from .logger import get_handler


def create_app(config_class=Config):
    app = Flask(__name__)
    
    app.config.from_object(config_class)

    # Initialize logger
    app.logger.removeHandler(default_handler)
    app.logger.addHandler(get_handler())
    if not app.debug:
        app.logger.setLevel(logging.INFO)
    else:
        app.logger.setLevel(logging.DEBUG)

    # Initialize Flask extensions here
    db.init_app(app)

    # Register blueprints here
    app.register_blueprint(bp_app_routes)

    # setup shell context
    @app.shell_context_processor
    def make_shell_context():
        return {"db": db}

    # setup request hooks
    @app.before_request
    def before_req():
        g.start = time.time()

    @app.after_request
    def after_req(response):
        ms_passed = (time.time() - g.start) * 1000
        path = f'{response.status_code} "{request.method} {request.path}"'
        log = f"{request.remote_addr} ===> {path}  🕒 {ms_passed:.2f} ms"
        app.logger.info(log)
        return response

    return app
