from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Message
from django.views.decorators.cache import cache_page

@cache_page(60)
def list_messages(request):
    messages = Message.objects.all()
    return render(request, 'messages.html', {'messages': messages})


def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('home')

# Recursive helper
def get_threaded_messages(message):
    replies = message.replies.all()
    return {
        'message_id': message.id,
        'content': message.content,
        'replies': [get_threaded_messages(reply) for reply in replies]
    }

def conversation_thread_view(request, message_id):
    # ✅ Optimized query
    message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver')
                       .prefetch_related('replies'),
        id=message_id
    )

    data = get_threaded_messages(message)
    return JsonResponse(data, safe=False)