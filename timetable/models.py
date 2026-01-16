from django.db import models
from django.contrib.auth.models import User


class SchoolLevel(models.TextChoices):
    PRIMARY = "PRIMARY", "Primary"
    HIGH = "HIGH", "High School"


class ClassLevel(models.Model):
    name = models.CharField(max_length=20)
    school_level = models.CharField(
        max_length=12,
        choices=SchoolLevel.choices
    )

    def __str__(self):
        return f"{self.name} ({self.school_level})"


class Timetable(models.Model):
    DAYS = [
        ("MON", "Monday"),
        ("TUE", "Tuesday"),
        ("WED", "Wednesday"),
        ("THU", "Thursday"),
        ("FRI", "Friday"),
    ]

    # ✅ CLASS (FOREIGN KEY – MUHIMU)
    class_level = models.ForeignKey(
        ClassLevel,
        on_delete=models.CASCADE,
        related_name="timetables"
    )

    # ✅ SUBJECT (kutoka students app)
    subject = models.ForeignKey(
        "students.Subject",
        on_delete=models.CASCADE
    )

    # ✅ TEACHER
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    # ✅ TIME INFO
    day = models.CharField(max_length=3, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.class_level} - {self.subject} ({self.day})"

