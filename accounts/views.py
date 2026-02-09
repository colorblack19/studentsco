from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User, Group
from .models import TeacherProfile

from django.db.models import Q

from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔥 ADMIN (SUPERUSER / STAFF)
            if user.is_superuser or user.is_staff:
                return redirect("dashboard")

            # 🔥 TEACHER
            if user.groups.filter(name="Teacher").exists():
                return redirect("teacher_dashboard")

            # 🔥 STUDENT / PARENT
            return redirect("home_dashboard")

        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login_19.html')


@login_required
def after_login_redirect(request):
    user = request.user

    if user.is_superuser:
        return redirect("home_dashboard")  # 👈 badilisha hapa

    if user.is_staff or user.groups.filter(name="Teacher").exists():
        return redirect("teacher_dashboard")

    return redirect("home_dashboard")




def logout_user(request):
    logout(request)
    return redirect('login')


def register_user(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'accounts/register_19.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')






@login_required
def add_teacher(request):

    if not request.user.is_staff:
        return render(request, "403.html")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("add_teacher")

        user = User.objects.create_user(
            username=username,
            password=password
        )

        # GROUP = ROLE
        group, _ = Group.objects.get_or_create(name="Teacher")
        user.groups.add(group)


        # (OPTIONAL) create profile if you still want it
        TeacherProfile.objects.get_or_create(user=user)

        messages.success(request, f"Teacher {username} created successfully")
        return redirect("dashboard")

    return render(request, "accounts/add_teacher.html")





@login_required
def group_list(request):
    if not request.user.is_staff:
        return render(request, "403.html")

    groups = Group.objects.all().order_by("name")
    return render(request, "accounts/group_list.html", {
        "groups": groups
    })




@login_required
def group_edit(request, id):
    if not request.user.is_staff:
        return render(request, "403.html")

    group = get_object_or_404(Group, id=id)
    permissions = Permission.objects.all().order_by("content_type__app_label")

    if request.method == "POST":
        group.permissions.set(request.POST.getlist("permissions"))
        return redirect("group_list")

    return render(request, "accounts/group_edit.html", {
        "group": group,
        "permissions": permissions,
    })





@login_required
def user_list(request):
    if not request.user.is_staff:
        return render(request, "403.html")

    users = (
        User.objects
        .filter(
            Q(groups__name__icontains="Teacher") | Q(is_staff=True)
        )                       # ✅ Teacher AU Staff
        .exclude(is_superuser=True)  # ❌ Ondoa SYSTEM@SCHOOL
        .exclude(id=request.user.id) # ❌ Ondoa wewe admin ulielogin
        .order_by("-date_joined")
        .distinct()
    )

    return render(request, "accounts/list.html", {
        "users": users
    })




@login_required
def user_add(request):
    if not request.user.is_staff:
        return render(request, "403.html")

    groups = Group.objects.all()

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        is_staff = request.POST.get("is_staff") == "on"
        group_ids = request.POST.getlist("groups")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("user_add")

        user = User.objects.create_user(
            username=username,
            password=password,
            is_staff=is_staff
        )

        user.groups.set(group_ids)

        messages.success(request, "User created successfully")
        return redirect("user_list")

    return render(request, "accounts/add.html", {
        "groups": groups
    })




@login_required
def user_edit(request, id):
    if not request.user.is_staff:
        return render(request, "403.html")

    user = get_object_or_404(User, id=id)
    groups = Group.objects.all()

    if request.method == "POST":
        user.is_staff = request.POST.get("is_staff") == "on"
        user.groups.set(request.POST.getlist("groups"))
        user.save()

        messages.success(request, "User updated successfully")
        return redirect("user_list")

    return render(request, "accounts/edit.html", {
        "user_obj": user,
        "groups": groups
    })



@login_required
def user_delete(request, id):
    if not request.user.is_staff:
        return render(request, "403.html")

    user = get_object_or_404(User, id=id)

    if request.method == "POST":
        user.delete()
        messages.success(request, "User deleted")
        return redirect("user_list")

    return render(request, "accounts/delete.html", {
        "user_obj": user
    })



def home_dashboard(request):
    return render(request, "home.html")





def about_us(request):
    return render(request, "accounts/about.html")




def is_admin(user):
    return user.groups.filter(name='Admin').exists()



from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

@login_required
def upload_teacher_photo(request):
    if request.method == "POST":
        profile = request.user.teacherprofile

        if "photo" in request.FILES:
            profile.photo = request.FILES["photo"]
            profile.save()

    return redirect(request.META.get("HTTP_REFERER", "/"))
