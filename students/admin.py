from django.contrib import admin
from .models import Student, FeeStructure, Payment
from django.utils.html import format_html
from .models import Attendance  



admin.site.register(Student)

admin.site.register(FeeStructure)

@admin.register(Payment)

class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'amount_paid',
        'colored_status',
        'method',
        'date_paid',
    )

    list_filter = (
        'status',
        'method',
        'date_paid',
    )

    search_fields = (
        'student__first_name',
        'student__last_name',
    )

    ordering = ('-date_paid',)


    def colored_status(self, obj):
        colors = {
            "PAID": "green",
            "PENDING": "orange",
            "FAILED": "red",
        }
        return format_html(
            '<b style="color:{}">{}</b>',
            colors.get(obj.status, "black"),
            obj.status
        )

    colored_status.short_description = "Status"



@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "teacher",
        "date",
        "status",
        "is_locked",
    )

    list_filter = (
        "date",
        "status",      # ⭐ MUHIMU
        "is_locked",
        "teacher",     # ⭐ MUHIMU
    )

    search_fields = (
        "student__first_name",
        "student__last_name",
    )

    actions = ["unlock_attendance"]

    def unlock_attendance(self, request, queryset):
        queryset.update(is_locked=False)

    unlock_attendance.short_description = "🔓 Unlock selected attendance"
