from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Event
from .forms import EventForm

# ADMIN LIST
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from django.contrib import messages
from django.utils.timezone import now


def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def add_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("admin_events")
    else:
        form = EventForm()

    return render(request, "events/add_event.html", {
        "form": form
    })


# PUBLIC (Parents & Students)


def public_events(request):
    events = Event.objects.filter(
        is_active=True,
        start_date__gte=now()
    ).order_by("start_date")

    return render(request, "events/public_events.html", {
        "events": events
    })


def calendar_events(request):
    events = Event.objects.filter(is_active=True)

    calendar_events = []
    for e in events:
        calendar_events.append({
            "title": e.title,
            "start": e.start_date.isoformat(),
        })

    return render(request, "events/calendar_events.html", {
        "calendar_events": calendar_events
    })


# ADMIN LIST
@staff_member_required
def admin_events(request):
    events = Event.objects.all().order_by("-start_date")
    return render(request, "events/admin_events.html", {
        "events": events
    })




def delete_event(request, id):
    event = get_object_or_404(Event, id=id)

    if request.method == "POST":
        event.delete()
        messages.success(request, "✅ Event deleted successfully.")
        return redirect("admin_events")

    return render(request, "events/delete_event.html", {"event": event})


# ADD EVENT
@staff_member_required
def add_event(request):
    form = EventForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect("admin_events")

    return render(request, "events/add_event.html", {
        "form": form
    })



# EDIT EVENT
@staff_member_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect("admin_events")
    else:
        form = EventForm(instance=event)

    return render(request, "events/event_form.html", {
        "form": form,
        "title": "Edit Event"
    })

