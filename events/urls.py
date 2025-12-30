from django.urls import path
from . import views

urlpatterns = [
    # public (parents / students)
    path("events/", views.public_events, name="public_events"),

    # admin dashboard (NOT django admin)
    path("dashboard/events/", views.admin_events, name="admin_events"),
    path("dashboard/events/add/", views.add_event, name="add_event"),
    path("dashboard/events/<int:event_id>/edit/", views.edit_event,name="edit_event"),
    path("events/delete/<int:id>/", views.delete_event, name="delete_event"),

]
