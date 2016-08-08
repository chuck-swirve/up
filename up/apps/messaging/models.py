from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from django.conf import settings
from django.db import models
from django.db import transaction

from common import models as common_models


class Inbox(common_models.BaseModel):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL,
                                 related_name='inbox')

    def has_unread_messages(self):
        return self.get_unread_messages().count() > 0

    def get_incoming_messages(self):
        return self.received_messages.filter(
            is_deleted=False
        )

    def get_outgoing_messages(self):
        return self.sent_messages.all()

    def get_unread_messages(self):
        return self.get_incoming_messages().filter(
            is_read=False
        )

    def get_conversations(self):
        messages = self.get_incoming_messages() | self.get_outgoing_messages()
        unread_convo_ids = self.get_unread_messages().values_list(
            'conversation_id', flat=True)
        convos = self.in_conversations.all().annotate(
            has_unread=models.Case(
                models.When(id__in=unread_convo_ids, then=True),
                default=False,
                output_field=models.BooleanField()
            )
        )
        return convos


class Conversation(common_models.BaseModel):
    subject = models.CharField(max_length=150)
    participants = models.ManyToManyField(
        Inbox, related_name='in_conversations')

    def reply(self, from_inbox, content):
        with transaction.atomic():
            to_inbox = self.participants.exclude(id=from_inbox.id).first()
            if to_inbox is None:  # convo with self...
                to_inbox = from_inbox
            new_message = Message()
            new_message.sender = from_inbox
            new_message.recipient = to_inbox
            new_message.content = content
            new_message.conversation = self
            new_message.save()
            self.save()


class Message(common_models.BaseModel):
    sender = models.ForeignKey(Inbox,
                               related_name='sent_messages')
    recipient = models.ForeignKey(Inbox,
                                  related_name='received_messages')
    conversation = models.ForeignKey(Conversation,
                                     related_name='messages')
    content = models.TextField()
    is_read = models.BooleanField(default=False)

    @classmethod
    def compose_new(cls, from_inbox, to_inbox, subject, content):
        with transaction.atomic():
            new_convo = Conversation(subject=subject)
            new_convo.save()
            new_convo.participants.add(from_inbox, to_inbox)
            new_message = Message()
            new_message.sender = from_inbox
            new_message.recipient = to_inbox
            new_message.content = content
            new_message.conversation = new_convo
            new_message.save()
