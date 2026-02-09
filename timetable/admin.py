from django.contrib import admin
from .models import Timetable


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = (
        "class_level",
        "subject",
        "teacher",
        "day",
        "start_time",
        "end_time",
    )

    list_filter = (
        "class_level",
        "day",
        "teacher",
    )

    search_fields = (
        "teacher__username",
        "subject__name",
    )
