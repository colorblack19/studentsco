from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import FeeStructure, Student

@receiver(post_save, sender=FeeStructure)
def update_students_fee(sender, instance, created, **kwargs):
    # Get all students in the same class
    students = Student.objects.filter(class_level=instance.class_name)

    for student in students:
        total_paid = student.total_paid()
        student.balance = instance.amount - total_paid
        student.save()


@receiver(post_delete, sender=FeeStructure)
def clear_students_fee(sender, instance, **kwargs):
    students = Student.objects.filter(class_level=instance.class_name)

    for student in students:
        student.feestructure = None
        student.balance = 0
        student.save()
