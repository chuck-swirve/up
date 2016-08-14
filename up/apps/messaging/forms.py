from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django import forms
from django.contrib.auth import get_user_model

from . import models


User = get_user_model()


class MessageForm(forms.ModelForm):

    class Meta:
        model = models.Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': '10', 'cols': '50'}),
        }
        labels = {
            'content': 'Your Message',
        }


class NewMessageForm(MessageForm):
    subject = forms.CharField(max_length=150)
    send_to = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        label='To')
