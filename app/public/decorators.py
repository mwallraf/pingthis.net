from flask import current_app, request, Response
from functools import wraps

"""
Decorator to validate the streaming endpoints, see if a cookie exists.
This is not really secure and should be changed by a real authentication method.
"""
def validate_cookie(f):
    cookie = "pingthis"
    @wraps(f)
    def decorated(*args, **kwargs):
        current_app.logger.debug("validate cookie '{}'".format(cookie))
        if not request.cookies.get(cookie):
            return Response(), 403
        return f(*args, **kwargs)
    return decorated


"""
Decorator to validate the streaming endpoints to provide basic security:

Parameters: 
   ipv4=<ip>            => validate if ipv4 ip address is provided
   tcpport=<port>       => validate if TCP port is provided
   cookie=<cookie name> => validate if cookie is present
"""
def validate_stream(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'ipaddress' in kwargs:
            current_app.logger.debug("Validate IPv4 ip address")
            if not kwargs['ipaddress']:
                return Response(), 400

        if 'port' in kwargs:
            current_app.logger.debug("Validate TCP port")
            if not kwargs['port']:
                return Response(), 400

        return f(*args, **kwargs)
    return decorated

