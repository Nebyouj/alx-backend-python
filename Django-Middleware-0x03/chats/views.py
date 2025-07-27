from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, filters
from rest_framework.exceptions import APIException
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .filters import MessageFilter

from .permissions import IsParticipantOfConversation
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer,
    ConversationCreateSerializer,
    MessageSerializer,
    MessageCreateSerializer,
)
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'participants__username']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ConversationCreateSerializer
        return ConversationSerializer

    def perform_create(self, serializer):
        # Optionally, add current user to participants if not included
        participants = serializer.validated_data.get('participants', [])
        if self.request.user not in participants:
            participants = list(participants) + [self.request.user]
        serializer.save(participants=participants)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    permission_classes = [IsAuthenticated,IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter]
    filterset_class = MessageFilter
    search_fields = ['content', 'sender__username']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MessageCreateSerializer
        return MessageSerializer

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
    
    def get_queryset(self):
       
        conversation_id = self.kwargs['conversation_pk']
        conversation = get_object_or_404(Conversation, pk=conversation_id)

       
        if self.request.user not in conversation.participants.all():
            raise APIException(detail="You are not a participant in this conversation.", code=HTTP_403_FORBIDDEN)
        return Message.objects.filter(conversation=conversation)

