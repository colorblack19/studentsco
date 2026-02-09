from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Timetable
from students.models import Subject
from students.models import Student



# ================= PERMISSION =================
def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


# ================= ADMIN =================

@login_required
@user_passes_test(is_admin)
def admin_timetable(request):
    timetables = (
        Timetable.objects
        .select_related("teacher", "subject")
        .order_by("teacher", "day", "start_time")
    )

    return render(request, "timetable/admin_timetable.html", {
        "timetables": timetables
    })



@login_required
@user_passes_test(is_admin)
def add_timetable(request):
    subjects = Subject.objects.all()
    teachers = User.objects.filter(groups__name="Teacher")
    class_levels = Student.CLASS_LEVELS

    if request.method == "POST":
        Timetable.objects.create(
            class_level=request.POST.get("class_level"),
            day=request.POST.get("day"),
            start_time=request.POST.get("start_time"),
            end_time=request.POST.get("end_time"),
            subject_id=request.POST.get("subject"),
            teacher_id=request.POST.get("teacher"),
        )
        return redirect("admin_timetable")

    return render(request, "timetable/add_timetable.html", {
        "subjects": subjects,
        "teachers": teachers,
        "class_levels": class_levels,
    })


@login_required
@user_passes_test(is_admin)
def edit_timetable(request, id):
    timetable = get_object_or_404(Timetable, id=id)
    subjects = Subject.objects.all()
    teachers = User.objects.filter(groups__name="Teacher")

    if request.method == "POST":
        timetable.day = request.POST.get("day")
        timetable.start_time = request.POST.get("start_time")
        timetable.end_time = request.POST.get("end_time")
        timetable.subject_id = request.POST.get("subject")
        timetable.teacher_id = request.POST.get("teacher")
        timetable.save()

        return redirect("admin_timetable")

    return render(request, "timetable/edit_timetable.html", {
        "timetable": timetable,
        "subjects": subjects,
        "teachers": teachers,
    })


@login_required
@user_passes_test(is_admin)
def delete_timetable(request, id):
    timetable = get_object_or_404(Timetable, id=id)
    timetable.delete()
    return redirect("admin_timetable")


# ================= TEACHER =================

@login_required
def teacher_timetable(request):
    timetables = (
        Timetable.objects
        .filter(teacher=request.user)
        .select_related("subject", "teacher")  # ⚠️ class_level IMETOLEWA
        .order_by("day", "start_time")
        
    )

    return render(request, "timetable/teacher_timetable.html", {
        "timetables": timetables
    })
