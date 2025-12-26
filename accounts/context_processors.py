def user_role(request):
    if request.user.is_authenticated:
        return {
            "is_teacher": request.user.groups.filter(
                name="Teacher - Basic"
            ).exists(),
            "is_admin": request.user.is_staff,
        }
    return {}

