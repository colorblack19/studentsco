from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Message
from .models import UserStatus
from django.db.models import Count, Q

@login_required
@login_required
def chat_home(request, user_id=None):
    user = request.user

    # USERS LIST
    if user.is_superuser:
        users = User.objects.filter(
            teacherprofile__isnull=False
        ).exclude(id=user.id)

    elif hasattr(user, "teacherprofile"):
        users = User.objects.filter(is_superuser=True)

    else:
        users = User.objects.none()

    users = users.annotate(
        unread_count=Count(
            "sent_messages",
            filter=Q(
                sent_messages__receiver=user,
                sent_messages__is_read=False
            )
        )
    )

    other_user = None
    messages = []
    other_status = None

    if user_id:
        other_user = get_object_or_404(User, id=user_id)

        messages = Message.objects.filter(
            sender__in=[user, other_user],
            receiver__in=[user, other_user]
        ).order_by("timestamp")

        Message.objects.filter(
            receiver=user,
            sender=other_user,
            is_read=False
        ).update(is_read=True)

        other_status = UserStatus.objects.filter(user=other_user).first()

        # ✅ POST LOGIC IKO HAPA NDANI
        if request.method == "POST":
            text = request.POST.get("message")
            file = request.FILES.get("file")

            if text or file:
                Message.objects.create(
                    sender=user,
                    receiver=other_user,
                    content=text or "",
                    file=file
                )
                return redirect("chat_with_user", user_id=other_user.id)

    return render(request, "chat/chat_home.html", {
        "users": users,
        "other_user": other_user,
        "messages": messages,
        "other_status": other_status,
    })



