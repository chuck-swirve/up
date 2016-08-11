from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View

from .models import Conversation
from .models import Inbox
from .models import Message


User = get_user_model()


class InboxView(View):
    template_name = 'messaging/inbox.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        inbox = get_object_or_404(Inbox, pk=request.user.inbox.pk)
        conversations = inbox.get_conversations().prefetch_related(
            'participants', 'messages')
        context = {'conversations': conversations}
        return render(request, self.template_name, context=context)
