from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$',
        views.get_forum_list,
        name='get-forum-list'),
    url(r'^boards/(?P<forum_slug>[-\w]+)/$',
        views.get_forum_detail,
        name='get-forum-detail'),
    url(r'^boards/(?P<forum_slug>[-\w]+)/(?P<thread_id>[0-9])/$',
        views.get_thread_detail,
        name='get-thread-detail'),
]
