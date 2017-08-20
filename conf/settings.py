# -*- coding: utf-8 -*-
import os
import logging

os_env = os.environ

class Config(object):
    # app meta info
    APP_TITLE = "Pingthis"

    SECRET_KEY = 'MySecretKey4PingThis'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    DEBUG_TB_PROFILER_ENABLED = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    MONGODB_SETTINGS = {
        'DB': ''
    }

    # THEME SUPPORT for static files, theme name is appended after 'static'
    THEME_ACTIVE = True
    THEME_NAME = 'pingthis'

    #security
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_TRACKABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_PASSWORD_SALT = '2nmsSalty'
    SECURITY_DEFAULT_REMEMBER_ME = True

    SECURITY_POST_REGISTER_VIEW = '/'
    SECURITY_UNAUTHORIZED_VIEW = '/unauthorized'
    #SECURITY_POST_LOGIN_VIEW = '/account'
    #SECURITY_POST_CONFIRM_VIEW = '/account'
    #SECURITY_CHANGE_URL = 
    #SECURITY_RESET_URL =
    #SECURITY_REGISTER_URL =

    # babel settings
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'utc'

    # flask mail settings
    MAIL_SERVER = ''
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = '?R'
    SECURITY_EMAIL_SENDER = ''

    # file logging settings
    LOG_FILE = os.path.abspath(os.path.join(PROJECT_ROOT, 'log', 'application.log'))
    LOG_FORMAT = '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
    LOG_LEVEL = logging.WARNING

    # shell commands
    SHELL_PING = os.environ.get('PINGTHIS_SHELL_PING', '/bin/bash -c "/sbin/fping -A -c 5 {} 2>&1"')
    SHELL_TRACEROUTE = os.environ.get('PINGTHIS_SHELL_TRACEROUTE', '/bin/bash -c "/bin/traceroute -4 -n -A {} 2>&1"')
    SHELL_NMAP = os.environ.get('PINGTHIS_SHELL_NMAP', '/bin/bash -c "/bin/nmap -p {} {} 2>&1"')

    # GOOGLE ANALYTICS TRACKID
    GOOGLE_ANALYTICS_TRACKID = ''


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_ENABLED = True
    DEBUG_TB_PROFILER_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    LOG_LEVEL = logging.DEBUG

    # GOOGLE ANALYTICS TRACKID
    GOOGLE_ANALYTICS_TRACKID = ''

    DEBUG_TB_PANELS = [
        'flask_debugtoolbar.panels.versions.VersionDebugPanel',
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel',
        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
        'flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel',
        'flask_debugtoolbar.panels.logger.LoggingPanel',
        'flask_debugtoolbar.panels.route_list.RouteListDebugPanel',
        'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
        # Add the MongoDB panel
        #'flask_debugtoolbar_mongo.panel.MongoDebugPanel',
    ]    

