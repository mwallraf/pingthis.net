from flask import request, Blueprint, send_from_directory, stream_with_context, Response, current_app, redirect, url_for, g, send_file
from flask.templating import render_template
import pexpect
import sys
from extensions import limiter
from .decorators import validate_cookie, validate_stream
from flask_limiter.util import get_remote_address
import uuid
import os

bp_public = Blueprint('public',__name__, static_folder='../static', template_folder='../templates')


@bp_public.before_request
def before_request():
    # store the remote user IP address
    g.remote_address = get_remote_address()





@bp_public.route('/test')
@limiter.exempt
def test():
    return render_template('test/test.html')

@bp_public.route('/test2')
@limiter.exempt
def test2():
    return render_template('test/test2.html')




@bp_public.route('/')
@limiter.exempt
def index():
    return redirect(url_for('public.ping')), 302

@bp_public.route('/ping')
@limiter.exempt
def ping():
    return render_template('tools/ping.html')

@bp_public.route('/traceroute')
@limiter.exempt
def traceroute():
    return render_template('tools/traceroute.html')

@bp_public.route('/portcheck')
@limiter.exempt
def portcheck():
    return render_template('tools/portcheck.html')

@bp_public.route('/uuid')
@limiter.exempt
def uuidv4():
    uuid4 = str(uuid.uuid4())
    return render_template('tools/uuid.html',
                           uuid=uuid4
        )

# TODO: set limiter
@bp_public.route('/speedtest')
def speedtest():
    return render_template('tools/speedtest.html')


"""
returns the remote ip - used by custom speedtest
"""
@bp_public.route('/speedtest2/remoteip')
def remoteip():
    return g.remote_address


"""
returns the remote ip - used by custom speedtest
"""
# TODO: set limiter
@bp_public.route('/speedtest2/empty', methods = [ "GET", "POST" ])
@limiter.exempt
def empty():
    print(request.values)
    return Response(headers={
                    "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
                    "Pragma": "no-cache",
                    "Connection": "keep-alive"
        })

"""
returns a randomly generated big file
"""
# TODO: set limiter
@bp_public.route('/speedtest2/bigfile')
@limiter.exempt
def bigfile():
    ckSize = int(request.values.get("ckSize", 20))
    def _generate_data():
        i = 0
        while i < ckSize:
            yield os.urandom(1048576)
            i += 1

    return Response(_generate_data(),
                       mimetype="application/octet-stream",
                       headers={"Content-Disposition": "attachment; filename=random.dat",
                                "Content-Description": "File Transfer",
                                "Content-Type": "application/octet-stream",
                                "Content-Transfer-Encoding": "binary",
                                "Cache-Control": "no-store, no-cache, must-revalidate, max-age=0",
                                "Pragma": "no-cache"
                                    })


@bp_public.route('/robots.txt')
def static_from_root():
    return send_from_directory(bp_public.static_folder, request.path[1:])


"""
Generator that yields the result of a pexpect spawn command line by line
input:
  pexp = pexpect.spawn(cmd) object
  cmd = command (ex. ping, traceroute, ..) used for logging only
"""
def _stream_generator(pexp, cmd):
    while True:
        line = pexp.readline().decode('unicode_escape')
        if not line: break

        current_app.logger.info("{} line received: {}".format(cmd, line))

        yield str("data: {}\n\n".format(line))
    yield str("data: END STREAM\n\n")


@bp_public.route('/ping/<string:ipaddress>')
@validate_cookie
@validate_stream
def streamed_response_ping(ipaddress=None):
        
    cmd = (current_app.config.get('SHELL_PING')).format(ipaddress)
    child = pexpect.spawn(cmd)

    resp = Response(stream_with_context(_stream_generator(child, "PING")), mimetype='text/event-stream')
    resp.headers['X-Accel-Buffering'] = 'no'
    return resp


@bp_public.route('/traceroute/<string:ipaddress>')
@validate_cookie
@validate_stream
def streamed_response_traceroute(ipaddress=None):

    cmd = (current_app.config.get('SHELL_TRACEROUTE')).format(ipaddress)
    current_app.logger.debug('spawning traceroute command: {}'.format(cmd))
    child = pexpect.spawn(cmd)

    resp = Response(stream_with_context(_stream_generator(child, "TRACEROUTE")), mimetype='text/event-stream')
    resp.headers['X-Accel-Buffering'] = 'no'
    return resp


@bp_public.route('/portcheck/<string:ipaddress>/<string:port>')
@validate_cookie
@validate_stream
def streamed_response_portcheck(ipaddress=None, port=None):

    cmd = (current_app.config.get('SHELL_NMAP')).format(port, ipaddress)
    current_app.logger.debug('spawning nmap command: {}'.format(cmd))
    child = pexpect.spawn(cmd)

    resp = Response(stream_with_context(_stream_generator(child, "NMAP")), mimetype='text/event-stream')
    resp.headers['X-Accel-Buffering'] = 'no'
    return resp



