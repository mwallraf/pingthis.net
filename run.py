import os

import warnings
from flask.exthook import ExtDeprecationWarning
warnings.simplefilter('ignore', ExtDeprecationWarning)

from app import create_app
try:
	from conf.local_settings import DevConfig, ProdConfig
except:
    from conf.settings import DevConfig, ProdConfig

## override the startup behavior by running start.sh
## or by setting the environment variables:
##    PINGTHIS_ENV (prod or antyhing else)
##    PINGTHIS_SHELL_PING
##    PINGTHIS_SHELL_TRACEROUTE
##    PINGTHIS_SHELL_NMAP

CONFIG = ProdConfig if os.environ.get('PINGTHIS_ENV') == 'prod' else DevConfig

app = create_app(CONFIG)
