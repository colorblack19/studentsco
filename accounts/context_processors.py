def user_role(request):
    if request.user.is_authenticated:
        return {
            "is_teacher": hasattr(request.user, "teacherprofile"),
            "is_admin": request.user.is_staff,
        }
    return {}

