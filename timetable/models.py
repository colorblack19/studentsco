from students.models import Student
from django.contrib.auth.models import User
from django.db import models

class Timetable(models.Model):
    DAYS = [
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
    ]

    CLASS_LEVELS = Student.CLASS_LEVELS  # 🔥 reuse existing system

    class_level = models.CharField(
        max_length=50,
        choices=CLASS_LEVELS
    )

    subject = models.ForeignKey(
        "students.Subject",
        on_delete=models.CASCADE
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    day = models.CharField(max_length=3, choices=DAYS)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.class_level} - {self.subject} ({self.day})"
