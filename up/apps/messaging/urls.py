from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',
        views.InboxView.as_view(),
        name='get-inbox-detail'),
    url(r'^conversations/(?P<conversation_id>[0-9]+)/$',
        views.ConversationView.as_view(),
        name='get-conversation-detail'),
]
