from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name', 'phone_number', 'role']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Nested sender info (read-only)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)  # Nested messages

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

# Serializer for creating/updating Conversation with participants as IDs:
class ConversationCreateSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Conversation
        fields = ['participants']

# Serializer for creating Messages, sender passed via view (not in payload)
class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['conversation', 'message_body']
