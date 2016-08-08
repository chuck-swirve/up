from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ['-updated']

    def __repr__(self):
        return '<{}: {}>'.format(self.__class__.__name__, self.pk)
