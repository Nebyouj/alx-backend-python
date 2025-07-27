from rest_framework import serializers
from .models import User, Conversation, Message
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name', 'phone_number', 'role']


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.SerializerMethodField()  # Using SerializerMethodField

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_name', 'content', 'timestamp']

    def get_sender_name(self, obj):
        return obj.sender.username

class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    title = serializers.CharField()  # Using CharField

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'participants', 'messages']

    def validate_title(self, value):  # Using ValidationError
        if not value:
            raise serializers.ValidationError("Title cannot be empty")
        return value


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
