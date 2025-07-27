# chats/filters.py
import django_filters
from .models import Message

class MessageFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name="sender__username", lookup_expr='icontains')
    start = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='gte')
    end = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr='lte')

    class Meta:
        model = Message
        fields = ['user', 'start', 'end']
