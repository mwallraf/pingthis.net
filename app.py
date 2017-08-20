# -*- coding: utf-8 -*-

from flask import Flask, render_template, url_for
from conf.settings import ProdConfig

from extensions import  cache, mail, debug_toolbar
from public.views import bp_public
import logging
import commands


def create_app(config_object=ProdConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)
    register_logging(app)
    register_commands(app)

    ## OVERRIDE URL_FOR to support themes for static files
    """
    ## same as url_for but if the global app parameters THEME_ACTIVE and THEME_NAME
    ## are known then the THEME_NAME is appended after the 'static' endpoint
    ## extra parameter: 
    ##   theme=<theme>  which overrides THEME_NAME and THEME_ACTIVE
    """
    @app.context_processor
    def override_url_for():
        return dict(url_for=_generate_url_for_theme)

    def _generate_url_for_theme(endpoint, **values):
        if endpoint == 'static':
            filename = values.get('filename', '')
            themename = values.get('theme', None)
            if not themename:
                if app.config.get('THEME_ACTIVE', False) and app.config.get('THEME_NAME', None):
                    themename = app.config.get('THEME_NAME')
            if themename:
                filename = "%s/%s" % (themename, filename)
                values['filename'] = filename
            values.pop("theme", None)
        return url_for(endpoint, **values)
    ## END OVERRIDE

    return app

def register_extensions(app):
    cache.init_app(app)
    mail.init_app(app)
    debug_toolbar.init_app(app)
    return None

def register_blueprints(app):    
    app.register_blueprint(bp_public)
    return None

def register_errorhandlers(app):
    def render_error(error):
        error_code = getattr(error, 'code', 500)
        return render_template("errors/{0}.html".format(error_code)), error_code

    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None

def register_logging(app):
    fileHandler = logging.FileHandler(app.config['LOG_FILE'])
    formatter = logging.Formatter(app.config['LOG_FORMAT'])
    fileHandler.setLevel(app.config['LOG_LEVEL'])
    fileHandler.setFormatter(formatter)
    app.logger.addHandler(fileHandler)
    return None

def register_commands(app):
    """Register Click commands."""
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.uwsgi)
