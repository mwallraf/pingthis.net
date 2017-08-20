# -*- coding: utf-8 -*-
"""Click commands."""
import os
from glob import glob
from subprocess import call

import click
from flask import current_app
from flask.cli import with_appcontext
from werkzeug.exceptions import MethodNotAllowed, NotFound
from conf.settings import ProdConfig


@click.command()
def clean():
    """
    Remove *.pyc and *.pyo files recursively starting at current directory.
    Borrowed from Flask-Script, converted to use Click.
    """
    for dirpath, dirnames, filenames in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.pyc') or filename.endswith('.pyo'):
                full_pathname = os.path.join(dirpath, filename)
                click.echo('Removing {}'.format(full_pathname))
                os.remove(full_pathname)

@click.command()
def uwsgi():
    """
    Create uwsgi.conf demo file
    """
    config = ProdConfig

    conf_file = """
[uwsgi]
base = {}
app = run
module = %(app)
callable = app

; spawn 2 offload threads
;offload-threads = 2

home = %(base)/venv
pythonpath = %(base)

socket = %(base)/socket.sock
chmod-socket = 777
vacuum = true

master = true
processes = 5

;threads = 5

logto = %(base)/log/%n.log

die-on-term = true
harakiri = 15

""".format(config.PROJECT_ROOT)

    output_file = os.path.join(config.PROJECT_ROOT, "uwsgi.ini")
    F = open(output_file, 'w')
    F.write(conf_file)
    F.close

    print("New file create: {}".format(os.path.join(config.PROJECT_ROOT, "uwsgi.ini")))


