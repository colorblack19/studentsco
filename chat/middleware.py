from django.utils import timezone
from .models import UserStatus

class UserOnlineMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            status, _ = UserStatus.objects.get_or_create(user=request.user)
            status.is_online = True
            status.last_seen = timezone.now()
            status.save(update_fields=["is_online", "last_seen"])
        return self.get_response(request)
