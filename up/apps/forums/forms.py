from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django import forms

from . import models


class ThreadForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Your Name",
                               required=False)
    password = forms.CharField(max_length=128, label="Your Password",
                               required=False, widget=forms.PasswordInput())
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows': '10', 'cols': '50'}),
        label='Your Message'
    )

    class Meta:
        model = models.Thread
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'size': '20'}),
        }
        labels = {
            'title': 'Topic Name'
        }


class PostForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Your Name",
                               required=False)
    password = forms.CharField(max_length=128, label="Your Password",
                               required=False, widget=forms.PasswordInput())

    class Meta:
        model = models.Post
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': '10', 'cols': '50'}),
        }
        labels = {
            'content': 'Your Message',
        }
