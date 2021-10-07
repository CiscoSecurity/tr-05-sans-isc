import json
import os

from __version__ import VERSION


class Config:
    settings = json.load(open('container_settings.json', 'r'))
    VERSION = settings['VERSION']
    #SECRET_KEY = os.environ.get('SECRET_KEY', None)
    SECRET_KEY = None


    # Supported types with rules
    CCT_OBSERVABLE_TYPES = {
        'ip': {}
    }

    CTR_HEADERS = {
        'User-Agent': ('SecureX Threat Response Integrations '
                       '<tr-integrations-support@cisco.com>')
    }
