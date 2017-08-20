from flask import request, Blueprint, send_from_directory, stream_with_context, Response, current_app, redirect, url_for
from flask.templating import render_template
import pexpect
import sys

bp_public = Blueprint('public',__name__, static_folder='../static', template_folder='../templates')

@bp_public.route('/')
def index():
    return redirect(url_for('public.ping')), 302

@bp_public.route('/ping')
def ping():
    return render_template('ping.html',
                           client_info={'ip': request.remote_addr}
                            )

@bp_public.route('/traceroute')
def traceroute():
    return render_template('traceroute.html',
                           client_info={'ip': request.remote_addr}
                            )

@bp_public.route('/portcheck')
def portcheck():
    return render_template('portcheck.html',
                           client_info={'ip': request.remote_addr}
                            )


@bp_public.route('/robots.txt')
def static_from_root():
    return send_from_directory(bp_public.static_folder, request.path[1:])



@bp_public.route('/ping/<string:ipaddress>')
def streamed_response_ping(ipaddress=None):

    if not ipaddress: return None
    
    cmd = '/bin/bash -c "/sbin/fping -A -c 5 {} 2>&1"'.format(ipaddress)
    current_app.logger.debug('spawning ping command: {}'.format(cmd))
    child = pexpect.spawn(cmd)

    def generate():
        while True:
            line = child.readline().decode('unicode_escape')
            if not line: break

            current_app.logger.info("PING line received: {}".format(line))

            yield str("data: {}\n\n".format(line))
        yield str("data: END STREAM\n\n")

    resp = Response(stream_with_context(generate()), mimetype='text/event-stream')
    resp.headers['X-Accel-Buffering'] = 'no'
    return resp


@bp_public.route('/traceroute/<string:ipaddress>')
def streamed_response_traceroute(ipaddress=None):

    if not ipaddress: return None

    cmd = '/bin/bash -c "/bin/traceroute -4 -n -A {} 2>&1"'.format(ipaddress)
    current_app.logger.debug('spawning traceroute command: {}'.format(cmd))
    child = pexpect.spawn(cmd)

    def generate():
        while True:
            line = child.readline().decode('unicode_escape')
            if not line: break

            current_app.logger.info("traceroute line received: {}".format(line))

            yield str("data: {}\n\n".format(line))
        yield str("data: END STREAM\n\n")

    resp = Response(stream_with_context(generate()), mimetype='text/event-stream')
    resp.headers['X-Accel-Buffering'] = 'no'
    return resp


@bp_public.route('/portcheck/<string:ipaddress>/<string:port>')
def streamed_response_portcheck(ipaddress=None, port=None):

    if not ipaddress or not port: return None

    cmd = '/bin/bash -c "/bin/nmap -p {} {} 2>&1"'.format(port, ipaddress)
    current_app.logger.debug('spawning nmap command: {}'.format(cmd))
    child = pexpect.spawn(cmd)

    def generate():
        while True:
            line = child.readline().decode('unicode_escape')
            if not line: break

            current_app.logger.info("nmap line received: {}".format(line))

            yield str("data: {}\n\n".format(line))
        yield str("data: END STREAM\n\n")

    resp = Response(stream_with_context(generate()), mimetype='text/event-stream')
    resp.headers['X-Accel-Buffering'] = 'no'
    return resp



