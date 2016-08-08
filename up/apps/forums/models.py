from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.conf import settings
from django.db import models

from common import models as common_models


class Forum(common_models.BaseModel):
    name = models.CharField(max_length=50, unique=True)
    tagline = models.CharField(max_length=140)
    post_count = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=50, unique=True)

    def __repr__(self):
        return '<Forum: {}>'.format(self.name)


class Thread(common_models.BaseModel):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    forum = models.ForeignKey(Forum, related_name='threads')
    is_sticky = models.BooleanField(default=False)
    post_count = models.PositiveIntegerField(default=0)


class Post(common_models.BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    thread = models.ForeignKey(Thread, related_name='posts')

    class Meta:
        ordering = ['created']

    def __repr__(self):
        return '<Post: {}>'.format(self.pk)
