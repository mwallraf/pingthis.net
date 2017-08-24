# -*- coding: utf-8 -*-
"""Extensions module. Each extension is initialized in the app factory located
in app.py
"""

from flask_cache import Cache
cache = Cache()

from flask_mail import Mail
mail = Mail()

from flask_debugtoolbar import DebugToolbarExtension
debug_toolbar = DebugToolbarExtension()

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(key_func=get_remote_address,
	              default_limits=["200 per day", "50 per hour", "5 per minute"]
)

