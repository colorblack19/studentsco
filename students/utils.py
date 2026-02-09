from django.shortcuts import redirect
from django.contrib import messages

def require_admin_approval(request):
    if request.user.is_superuser:
        return True

    if request.session.get("admin_approved"):
        return True

    request.session["next_url"] = request.path
    return False


def subject_performance(report):
    subjects = report.subjects.all()
    if not subjects:
        return None

    best = max(subjects, key=lambda s: s.marks)
    worst = min(subjects, key=lambda s: s.marks)

    return {
        "best": best,
        "worst": worst,
    }
