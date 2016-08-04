from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django import forms

from . import models


class ThreadForm(forms.ModelForm):
    class Meta:
        model = models.Thread
        fields = ['title']


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['content']
