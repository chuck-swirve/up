from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Forum, Post, Thread


def get_forum_list(request):
    forums = Forum.objects.filter(is_deleted=False)
    context = {'forums': forums}
    return render(request, 'forums/home.html', context=context)


def get_forum_detail(request, forum_slug):
    forum = get_object_or_404(Forum, slug=forum_slug)
    threads = Thread.objects.filter(
        forum_id=forum.pk
    ).filter(is_deleted=False)[:100]
    context = {'forum': forum, 'threads': threads}
    return render(request, 'forums/forum.html', context=context)


def get_thread_detail(request, forum_slug, thread_id):
    forum = get_object_or_404(Forum, slug=forum_slug)
    thread = get_object_or_404(forum.threads, pk=thread_id)
    posts = Post.objects.filter(
        thread_id=thread.pk
    ).filter(is_deleted=False)
    context = {'forum': forum, 'thread': thread, 'posts': posts}
    return render(request, 'forums/thread.html', context=context)


@login_required
def make_thread(request, forum_slug):
    return ''


@login_required
def make_thread_post(request, forum_slug, thread_id):
    return ''
