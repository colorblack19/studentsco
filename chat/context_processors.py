from .models import Message

def chat_context(request):
    user = request.user

    is_teacher = (
        user.is_authenticated and
        hasattr(user, "teacherprofile")
    )

    can_see_chat = (
        user.is_authenticated and
        (user.is_superuser or is_teacher)
    )

    if can_see_chat:
        unread_count = Message.objects.filter(
            receiver=user,
            is_read=False
        ).count()
    else:
        unread_count = 0

    return {
        "can_see_chat": can_see_chat,
        "unread_count": unread_count,
    }
