from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

import django
from django.conf import settings
from django.conf import Settings
from django.core.management import call_command


if __name__ == '__main__':
    settings.configure(Settings('up.settings'), DEBUG=True)
    django.setup()
    site_apps = [a for a in os.listdir(settings.APPS_DIR) if a != 'common']
    # do common first
    call_command('loaddata', 'initial_data.json', app='common')
    for site_app in site_apps:
        call_command('loaddata', 'initial_data.json', app=site_app)
