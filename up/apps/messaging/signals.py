from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Inbox

@receiver(post_save, sender=settings.AUTH_USER_MODEL,
          dispatch_uid='create_user_inbox')
def handler(sender, instance, created, **kwargs):
    if created:
        new_inbox = Inbox(owner=instance)
        new_inbox.save()
