from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import transaction
from django.db.models import F
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render

from .forms import PostForm, ThreadForm
from .models import Forum, Post, Thread


User = get_user_model()


def get_forum_list(request):
    forums = Forum.objects.filter(is_deleted=False)
    context = {'forums': forums}
    return render(request, 'forums/home.html', context=context)


def get_forum_detail(request, forum_slug):
    forum = get_object_or_404(Forum, slug=forum_slug)
    if request.method == 'GET':
        threads = Thread.objects.filter(
            forum_id=forum.pk
        ).filter(is_deleted=False)[:100]
        context = {
            'forum': forum,
            'threads': threads,
            'thread_form': ThreadForm(),
            'post_form': PostForm(),
        }
        return render(request, 'forums/forum.html', context=context)
    elif request.method == 'POST':
        a_user = User.objects.first()
        thread_form = ThreadForm(request.POST)
        post_form = PostForm(request.POST)
        if thread_form.is_valid() and post_form.is_valid():
            with transaction.atomic():
                new_thread = thread_form.save(commit=False)
                new_thread.author = a_user
                new_thread.post_count = 1
                new_thread.forum = forum
                forum.post_count = F('post_count') + 1
                new_thread.save()

                new_post = post_form.save(commit=False)
                new_post.author = a_user
                new_post.thread = new_thread

                new_thread.save()
                new_post.save()
                forum.save()

            return HttpResponseRedirect(
                reverse(
                    'get-forum-detail',
                    kwargs={'forum_slug': forum_slug})
            )
    return HttpResponseNotAllowed('')


def get_thread_detail(request, forum_slug, thread_id):
    forum = get_object_or_404(Forum, slug=forum_slug)
    thread = get_object_or_404(Thread, pk=thread_id)
    if request.method == 'GET':
        posts = thread.posts.filter(is_deleted=False)
        context = {
            'forum': forum,
            'thread': thread,
            'posts': posts,
            'post_form': PostForm()
        }
        return render(request, 'forums/thread.html', context=context)
    elif request.method == 'POST':
        a_user = User.objects.first()
        post_form = PostForm(request.POST)
        with transaction.atomic():
            thread.refresh_from_db()
            if post_form.is_valid() and thread.post_count < 100:
                new_post = post_form.save(commit=False)
                new_post.author = a_user
                new_post.thread = thread
                thread.post_count = F('post_count') + 1
                forum.post_count = F('post_count') + 1

                new_post.save()
                thread.save()
                forum.save()

                return HttpResponseRedirect(
                    reverse(
                        'get-thread-detail',
                        kwargs={
                            'forum_slug': forum_slug,
                            'thread_id': thread_id})
                )
    return HttpResponseNotAllowed('')
