from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.apps import AppConfig


class MessagingConfig(AppConfig):
    name = 'messaging'

    def ready(self):
        from . import signals  # NOQA
