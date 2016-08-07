from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$',
        views.ForumListView.as_view(),
        name='get-forum-list'),
    url(r'^boards/(?P<forum_slug>[-\w]+)/$',
        views.ForumDetailView.as_view(),
        name='get-forum-detail'),
    url(r'^boards/(?P<forum_slug>[-\w]+)/(?P<thread_id>[0-9])/$',
        views.ThreadDetailView.as_view(),
        name='get-thread-detail'),
]
