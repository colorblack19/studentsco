from django.contrib import admin
from .models import Student, FeeStructure, Payment


admin.site.register(Student)

admin.site.register(FeeStructure)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount_paid', 'date_paid', 'method')
    search_fields = ('student__first_name', 'student__last_name')
    list_filter = ('method', 'date_paid')


# Register Payment with PaymentAdmin
admin.site.register(Payment, PaymentAdmin)

