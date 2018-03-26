# -*- coding: utf-8 -*-
"""Click commands."""
import os
from glob import glob
from subprocess import call

import click
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


@click.command()
def nginx():
    """
    Generate example nginx config file
    """
    config = ProdConfig

    conf_file = """

# redirect www.pingthis.net -> pingthis.net
server {
listen 80;
server_name www.pingthis.net;
return 301 $scheme://pingthis.net;
}

# redirect ping.pingthis.net -> pingthis.net/ping
server {
listen 80;
server_name ping.pingthis.net;
return 301 $scheme://pingthis.net/ping;
}

# redirect trace.pingthis.net or traceroute.pingthis.net -> pingthis.net/traceroute
server {
listen 80;
server_name trace.pingthis.net traceroute.pingthis.net;
return 301 $scheme://pingthis.net/traceroute;
}

# redirect portcheck.pingthis.net -> pingthis.net/portcheck
server {
listen 80;
server_name portcheck.pingthis.net;
return 301 $scheme://pingthis.net/portcheck;
}

# redirect uuid.pingthis.net -> pingthis.net/uuid
server {
listen 80;
server_name uuid.pingthis.net;
return 301 $scheme://pingthis.net/uuid;
}

# redirect speedtest.pingthis.net -> pingthis.net/speedtest
server {
listen 80;
server_name speedtest.pingthis.net;
return 301 $scheme://pingthis.net/speedtest;
}

server {
listen 80;
real_ip_header X-Forwarded-For;
set_real_ip_from 127.0.0.1;
server_name pingthis.net;

location / {
include uwsgi_params;
uwsgi_pass unix:/opt/pingthis.net/socket.sock;
uwsgi_modifier1 30;
}

error_page 404 /404.html;
location = /404.html {
root /usr/share/nginx/html;
}

error_page 500 502 503 504 /50x.html;
location = /50x.html {
root /usr/share/nginx/html;
}

}

"""

    output_file = os.path.join(config.PROJECT_ROOT, "nginx-your_site.conf")
    F = open(output_file, 'w')
    F.write(conf_file)
    F.close

    print("New file create: {}".format(os.path.join(config.PROJECT_ROOT, "nginx-your_site.conf")))
