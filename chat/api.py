from django.http import JsonResponse
from rest_framework.decorators import api_view

from .models import Conversation, ConversationMessage
from .serializers import (
    ConversationListSerializer,
    ConversationDetailSerializer,
    ConversationMessageSerializer,
)
from useraccount.models import User


@api_view(["GET"])
def conversation_list(request):
    serializer = ConversationListSerializer(request.user.conversations.all(), many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(["GET"])
def conversation_detail(request, pk):
    # this method will get all the conversations part of the url id

    conversation = request.user.conversations.get(pk=pk)

    conversation_serializer = ConversationDetailSerializer(conversation, many=False)
    messages_serializer = ConversationMessageSerializer(
        conversation.messages.all(), many=True
    )

    return JsonResponse(
        {
            "conversation": conversation_serializer.data,
            "messages": messages_serializer.data,
        },
        safe=False,
    )


@api_view(["GET"])
def conversations_start(request, user_id):
    # the user id as part of the args is the other user , that you want to start a convo with
    # the request user will be us
    conversations = Conversation.objects.filter(users__in=[user_id]).filter(
        users__in=[request.user.id]
    )

    if conversations.count() > 0:
        # in the situations where we have multiple convos already , we will pick the most recently created ..
        conversation = conversations.order_by("-created_at").first()
        return JsonResponse({"success": True, "conversation_id": conversation.id})
    else:
        # we will need to create a convo
        user = User.objects.get(pk=user_id)
        conversation = Conversation.objects.create()
        conversation.users.add(request.user)
        conversation.users.add(user)
        return JsonResponse({"success": True, "conversation_id": conversation.id})
