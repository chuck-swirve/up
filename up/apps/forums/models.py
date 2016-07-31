from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.conf import settings
from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        ordering = ['-updated']


class Forum(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __repr__(self):
        return '<Forum: {}>'.format(self.name)


class Thread(BaseModel):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    forum = models.ForeignKey(Forum, related_name='threads')
    is_sticky = models.BooleanField(default=False)

    def __repr__(self):
        return '<Thread: {}>'.format(self.title)


class Post(BaseModel):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    content = models.TextField()
    thread = models.ForeignKey(Thread, related_name='posts')

    class Meta:
        ordering = ['created']

    def __repr__(self):
        return '<Post: {}>'.format(self.pk)
