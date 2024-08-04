import uuid
from django.db import models

# Create your models here.
from useraccount.models import User


class Conversation(models.Model):
    # the conversation model here represents a convesation activity
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # from this side , this is all the users that have taken part in this particular conversation
    # we can use the related name to get all the conversations that a user is part of from user model
    users = models.ManyToManyField(User, related_name="conversations")
    # when we add this conversation this is set
    created_at = models.DateTimeField(auto_now_add=True)
    # everytime we save
    modified_at = models.DateTimeField(auto_now=True)


class ConversationMessage(models.Model):
    # this model represents conversation messages from a conversation
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    body = models.TextField()
    sent_to = models.ForeignKey(
        User, related_name="received_messages", on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        User, related_name="sent_messages", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
