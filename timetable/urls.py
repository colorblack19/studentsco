from django.urls import path
from . import views

urlpatterns = [
    path("my/", views.teacher_timetable, name="teacher_timetable"),
    path("admin/", views.admin_timetable, name="admin_timetable"),

   
    path("admin/", views.admin_timetable, name="admin_timetable"),
    path("add/", views.add_timetable, name="add_timetable"),
    path("edit/<int:id>/", views.edit_timetable, name="edit_timetable"),
    path("delete/<int:id>/", views.delete_timetable, name="delete_timetable"),


]
