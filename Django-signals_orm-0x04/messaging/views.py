from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Message
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required

@cache_page(60)
def list_messages(request):
    messages = Message.objects.all()
    return render(request, 'messages.html', {'messages': messages})


def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('home')

def get_replies_recursive(message):
    """Recursively fetch replies for a message."""
    replies = Message.objects.filter(parent_message_id=message.parent_id)
    return [
        {
            "id": reply.id,
            "sender": reply.sender.username,
            "receiver": reply.receiver.username,
            "content": reply.content,
            "timestamp": reply.timestamp,
            "replies": get_replies_recursive(reply),  # Recursive call
        }
        for reply in replies
    ]

@login_required
def user_messages_view(request):
    """Fetch user messages with threaded replies and optimized queries."""
    messages = (
        Message.objects
        .filter(sender=request.user, parent_message__isnull=True)  # ✅ required
        .select_related('sender', 'receiver')  # ✅ foreign key optimization
        .prefetch_related('replies')  # ✅ replies optimization
    )

    data = []
    for msg in messages:
        data.append({
            "id": msg.id,
            "sender": msg.sender.username,
            "receiver": msg.receiver.username,
            "content": msg.content,
            "timestamp": msg.timestamp,
            "replies": get_replies_recursive(msg),  # ✅ recursive query
        })

    return JsonResponse(data, safe=False)

def conversation_thread_view(request, message_id):
    # ✅ Optimized query
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver')
                       .prefetch_related('replies'),
        id=message_id
    )

    data = get_replies_recursive(message)
    return JsonResponse(data, safe=False)


@login_required
def unread_messages_view(request):
    """Display only unread messages for the logged-in user."""
    unread_msgs = Message.unread.unread_for_user(request.user).only('id', 'sender', 'content', 'timestamp')
    
    data = [
        {
            "id": msg.id,
            "sender": msg.sender.username,
            "content": msg.content,
            "timestamp": msg.timestamp,
        }
        for msg in unread_msgs
    ]
    return JsonResponse(data, safe=False)