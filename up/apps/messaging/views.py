from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import Error as DatabaseError
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View

from .forms import MessageForm
from .forms import NewMessageForm
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
        context = {
            'conversations': conversations,
            'new_msg_form': NewMessageForm(),
        }
        return render(request, self.template_name, context=context)

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        inbox = get_object_or_404(Inbox, pk=request.user.inbox.pk)
        new_msg_form = NewMessageForm(request.POST)
        context = {
            'new_message_form': new_msg_form,
        }

        if new_msg_form.is_valid():
            try:
                sender = request.user.inbox
                recipient = new_msg_form.cleaned_data['send_to'].inbox
                subject = new_msg_form.cleaned_data['subject']
                content = new_msg_form.cleaned_data['content']
                new_msg = Message.compose_new(
                    sender, recipient, subject, content)
                return redirect(
                    'get-conversation-detail',
                    conversation_id = new_msg.conversation.id)
            except DatabaseError:
                msg = 'Hmm, there seems to be a problem. Please try later.'
                msg_form.add_error(None, msg)
        # either something failed to validate or db barfed
        return render(request, self.template_name, context=context)



class ConversationView(View):
    template_name = 'messaging/conversation.html'

    @method_decorator(login_required)
    def get(self, request, conversation_id, *args, **kwargs):
        inbox = get_object_or_404(Inbox, pk=request.user.inbox.pk)
        inbox_convos = inbox.get_conversations()
        conversation = get_object_or_404(
            inbox_convos.prefetch_related(
                'messages',
                'messages__sender',
                'messages__sender__owner'
            ),
            pk=conversation_id)
        context = {'conversation': conversation}
        return render(request, self.template_name, context=context)
