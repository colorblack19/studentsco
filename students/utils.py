from django.shortcuts import redirect
from django.contrib import messages

def require_admin_approval(request):
    if request.user.is_superuser:
        return True

    if request.session.get("admin_approved"):
        return True

    request.session["next_url"] = request.path
    return False
