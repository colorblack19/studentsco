from django.db import models
from django.utils import timezone


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


class FeeStructure(models.Model):
    class_name = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.class_name} - {self.amount}"


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)

        # when record created
    created_at = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50, default='Cash')

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

    def __str__(self):
        return f"{self.student.first_name} - {self.amount_paid} - {self.status}"


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