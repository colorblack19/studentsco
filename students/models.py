from django.db import models
from django.utils import timezone

from django.conf import settings

from django.contrib.auth.models import User


class Student(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    CLASS_LEVELS = (
        ('Grade1', 'Grade1'),
        ('Grade2', 'Grade2'),
        ('Grade3', 'Grade3'),
        ('Grade4', 'Grade4'),
        ('Grade5', 'Grade5'),
        ('Grade6', 'Grade6'),
        ('Grade7', 'Grade7'),
        ('Grade8', 'Grade8'),
        ('Form1', 'Form1'),
        ('Form2', 'Form2'),
        ('Form3', 'Form3'),
        ('Form4', 'Form4'),
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.IntegerField()

    parent_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    parent_id_number = models.CharField(max_length=50, blank=True, null=True)

    class_level = models.CharField(max_length=50, choices=CLASS_LEVELS)
    date_registered = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
    feestructure = models.ForeignKey("FeeStructure",on_delete=models.SET_NULL,null=True,blank=True)
    photo = models.ImageField(upload_to='student_photos/', blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
   

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students"
    )
    # UNIQUE ADMISSION NO FROM DATABASE
    admission_number = models.CharField(max_length=10, unique=True, blank=True, null=True)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def class_name(self):
        return self.class_level

    @property
    def parent_phone(self):
        return self.phone_number

    # CLEAN: AUTO-GENERATED ADMISSION NUMBER
    @property
    def admission_number(self):
        return f"STU{self.id:04d}"

    def total_paid(self):
        payments = self.payment_set.filter(status="PAID")
        return sum(p.amount_paid for p in payments)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

    # ✅ ATTENDANCE MODEL (IKO NJE YA STUDENT)
class Attendance(models.Model):
    STATUS_CHOICES = (
        ("Present", "Present"),
        ("Absent", "Absent"),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendances"
    )

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    date = models.DateField()


    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )
    is_locked = models.BooleanField(default=False)
    class Meta:
        unique_together = ("student", "date")

    def __str__(self):
        return f"{self.student.full_name} - {self.date} - {self.status}"
    


class AttendanceAlert(models.Model):
    STATUS_CHOICES = (
        ("new", "New"),
        ("reviewed", "Reviewed"),
    )

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        "Student",
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("teacher", "student")

    def __str__(self):
        return f"{self.student} - {self.status}"



class FeeStructure(models.Model):
    class_name = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

        # 🔥 NEW FIELDS
    opening_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    deadline = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.class_name} - {self.amount}"


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)

        # when record created
    created_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, default='Cash')
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)


    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("PAID", "Paid"),
        ("FAILED", "Failed"),
    )

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="PAID"   
    )

    notes = models.CharField(max_length=255, blank=True)




def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    # 🚫 Update balance ONLY if payment is PAID
    if self.status != "PAID":
        return

    total_paid = self.student.total_paid()

    fee = FeeStructure.objects.filter(
        class_name=self.student.class_level
    ).first()

    if fee:
        self.student.balance = fee.amount - total_paid
    else:
        self.student.balance = 0

    self.student.save()

def __str__(self):
        return f"{self.student.first_name} - {self.amount_paid} - {self.status}"

class AdminActionLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.action}"


class AcademicReport(models.Model):
    TERM_CHOICES = [
        ("MID", "Mid Term"),
        ("END", "End Term"),
    ]

    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    term = models.CharField(max_length=3, choices=TERM_CHOICES)
    total_score = models.IntegerField()
    grade = models.CharField(max_length=5)
    teacher_comment = models.TextField()
    headteacher_remark = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    status = models.CharField(
    max_length=20,
    choices=[("DRAFT", "Draft"), ("PUBLISHED", "Published")],
    default="DRAFT"
         )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.get_term_display()}"


class ReportSubject(models.Model):
    report = models.ForeignKey(
        AcademicReport,
        related_name="subjects",
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        "students.Subject",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    name = models.CharField(
        max_length=100,
        blank=True
    )  # 🔒 legacy support

    marks = models.IntegerField()
    grade = models.CharField(max_length=5)
    teacher_comment = models.TextField(blank=True)

    def __str__(self):
        return self.subject.name if self.subject else self.name



# students/models.py
class Subject(models.Model):
    name = models.CharField(max_length=100)
    class_level = models.CharField(
        max_length=50,
        choices=Student.CLASS_LEVELS
    )

    class Meta:
        unique_together = ("name", "class_level")

    def __str__(self):
        return f"{self.name} ({self.class_level})"


