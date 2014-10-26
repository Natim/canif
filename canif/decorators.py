"""
Taken from:  https://gist.github.com/1094140
"""

from functools import wraps
from flask import request, current_app

from six import text_type


def jsonp(func):
    """Wraps JSONified output for JSONP requests."""
    @wraps(func)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            data = func(*args, **kwargs).data
            content = "%s (%s)" % (text_type(callback), data.decode('utf-8'))
            mimetype = 'application/javascript'
            return current_app.response_class(content, mimetype=mimetype)
        else:
            return func(*args, **kwargs)
    return decorated_function
