from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from django.db import transaction
from django.db import Error as DatabaseError
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import View

from .forms import PostForm
from .forms import ThreadForm
from .models import Forum
from .models import Post
from .models import Thread


User = get_user_model()


def _get_user_lazy_login(request, login_form):
    is_authenticated = request.user.is_authenticated()
    if not login_form.is_valid():
        return None

    username = login_form.cleaned_data['username']
    password = login_form.cleaned_data['password']

    if is_authenticated and username == request.user.username:
        return request.user
    elif is_authenticated and username != request.user.username:
        logout(request)

    # if we haven't returned early, login_form is valid and
    # we need to attempt user authentication
    user = authenticate(username=username, password=password)
    if user is None:
        msg = 'That user/password combination is not recognized'
        login_form.add_error(None, msg)
    elif not user.is_active:
        msg = 'Your account is disabled.'
        login_form.add_error(None, msg)
    elif user.is_active:
        login(request, user)
    return user


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
        if request.user.is_authenticated():
            thread_form = ThreadForm(
                initial={'username': request.user.username})
        else:
            thread_form = ThreadForm()
        context = {
            'forum': forum,
            'threads': threads,
            'thread_form': thread_form,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, forum_slug, *args, **kwargs):
        forum = get_object_or_404(Forum, slug=forum_slug)
        # we only need `threads` if the form isn't valid.
        # this is inefficient in the common case
        threads = forum.threads.filter(is_deleted=False)[:100]
        thread_form = ThreadForm(request.POST)
        context = {
            'forum': forum,
            'threads': threads,
            'thread_form': thread_form,
        }
        user = _get_user_lazy_login(request, thread_form)
        if user is None:
            return render(request, self.template_name, context=context)
        if thread_form.is_valid():
            try:
                with transaction.atomic():
                    new_thread = thread_form.save(commit=False)
                    new_thread.author = request.user
                    new_thread.post_count = 1
                    new_thread.forum = forum
                    forum.post_count = F('post_count') + 1
                    new_thread.save()

                    content = thread_form.cleaned_data['content']
                    new_post = Post()
                    new_post.content = content
                    new_post.author = request.user
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
        if request.user.is_authenticated():
            post_form = PostForm(initial={'username': request.user.username})
        else:
            post_form = PostForm()
        context = {
            'forum': forum,
            'thread': thread,
            'posts': posts,
            'post_form': post_form,
        }
        return render(request, self.template_name, context=context)

    def post(self, request, forum_slug, thread_id, *args, **kwargs):
        forum = get_object_or_404(Forum, slug=forum_slug)
        thread = get_object_or_404(forum.threads, id=thread_id)
        # we only need `posts` if the form isn't valid.
        # this is inefficient in the common case
        posts = thread.posts.all()
        post_form = PostForm(request.POST)
        context = {
            'forum': forum,
            'thread': thread,
            'posts': posts,
            'post_form': post_form,
        }
        user = _get_user_lazy_login(request, post_form)
        if user is None:
            return render(request, self.template_name, context)
        try:
            with transaction.atomic():
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
