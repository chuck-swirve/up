from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.db import transaction
from django.db import Error as DatabaseError
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import View

from .forms import LoginForm
from .forms import PostForm
from .forms import ThreadForm
from .models import Forum
from .models import Thread


User = get_user_model()


class ForumListView(View):
    template_name = 'forums/home.html'

    def get(self, request, *args, **kwargs):
        forums = Forum.objects.filter(is_deleted=False)
        context = {'forums': forums}
        return render(request, self.template_name, context=context)


class ForumDetailView(View):
    template_name = 'forums/forum.html'

    def get(self, request, forum_slug, *args, **kwargs):
        forum = get_object_or_404(Forum, slug=forum_slug)
        threads = Thread.objects.filter(
            forum_id=forum.pk
        ).filter(is_deleted=False)[:100]
        context = {
            'forum': forum,
            'threads': threads,
            'thread_form': ThreadForm(),
            'post_form': PostForm(),
            'login_form': LoginForm(),
        }
        return render(request, self.template_name, context=context)

    def post(self, request, forum_slug, *args, **kwargs):
        user = User.objects.first()
        forum = get_object_or_404(Forum, slug=forum_slug)
        # we only need `threads` if the form isn't valid.
        # this is inefficient in the common case
        threads = forum.threads.filter(is_deleted=False)[:100]
        thread_form = ThreadForm(request.POST)
        post_form = PostForm(request.POST)
        login_form = LoginForm()
        context = {
            'forum': forum,
            'threads': threads,
            'thread_form': thread_form,
            'post_form': post_form,
            'login_form': login_form,
        }
        if thread_form.is_valid() and post_form.is_valid():
            try:
                with transaction.atomic():
                    new_thread = thread_form.save(commit=False)
                    new_thread.author = user
                    new_thread.post_count = 1
                    new_thread.forum = forum
                    forum.post_count = F('post_count') + 1
                    new_thread.save()

                    new_post = post_form.save(commit=False)
                    new_post.author = user
                    new_post.thread = new_thread

                    new_post.save()
                    forum.save()

                    # Happy path
                    return redirect(
                        'get-forum-detail',
                        forum_slug=forum_slug)
            except DatabaseError:
                msg = "Hmm, there seems to be a problem. Please try later."
                thread_form.add_error(None, msg)
        # either something failed to validate or the db barfed
        return render(request, self.template_name, context=context)


class ThreadDetailView(View):
    template_name = 'forums/thread.html'

    def get(self, request, forum_slug, thread_id, *args, **kwargs):
        forum = get_object_or_404(Forum, slug=forum_slug)
        thread = get_object_or_404(forum.threads, pk=thread_id)
        posts = thread.posts.all()
        context = {
            'forum': forum,
            'thread': thread,
            'posts': posts,
            'post_form': PostForm(),
            'login_form': LoginForm(),
        }
        return render(request, self.template_name, context=context)

    def post(self, request, forum_slug, thread_id, *args, **kwargs):
        user = User.objects.first()
        forum = get_object_or_404(Forum, slug=forum_slug)
        thread = get_object_or_404(forum.threads, id=thread_id)
        # we only need `posts` if the form isn't valid.
        # this is inefficient in the common case
        posts = thread.posts.all()
        post_form = PostForm(request.POST)
        login_form = LoginForm()
        context = {
            'forum': forum,
            'thread': thread,
        }
        try:
            with transaction.atomic():
                thread.refresh_from_db()
                if thread.post_count >= 100:
                    post_form.add_error(None, 'Your bacon was preempted.')
                elif post_form.is_valid():
                    new_post = post_form.save(commit=False)
                    new_post.author = user
                    new_post.thread = thread
                    thread.post_count = F('post_count') + 1
                    forum.post_count = F('post_count') + 1

                    new_post.save()
                    thread.save()
                    forum.save()

                    # Happy path
                    return redirect(
                        'get-thread-detail',
                        forum_slug=forum_slug,
                        thread_id=thread_id)
        except DatabaseError:
            msg = 'Hmm, there seems to be a problem. Please try later.'
            post_form.add_error(None, msg)
        # either something failed to validate or db barfed
        return render(request, self.template_name, context=context)
