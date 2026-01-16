from django.contrib import admin
from .models import ClassLevel, Timetable
from students.models import Subject


@admin.register(ClassLevel)
class ClassLevelAdmin(admin.ModelAdmin):
    list_display = ("name", "school_level")
    list_filter = ("school_level",)


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ("class_level", "subject", "teacher", "day", "start_time")
    list_filter = ("class_level", "day")
    search_fields = ("teacher__username",)
