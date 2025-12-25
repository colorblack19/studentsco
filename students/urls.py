from django.urls import path
from django.shortcuts import redirect
from . import views
from .views import (
    teacher_students,
    teacher_dashboard,
    mark_attendance,
)

urlpatterns = [
    path("", lambda request: redirect("dashboard")),

    # MAIN
    path("dashboard/", views.dashboard, name="dashboard"),

    # TEACHER
    path("teacher/dashboard/", teacher_dashboard, name="teacher_dashboard"),
    path("teacher/students/", teacher_students, name="teacher_students"),
    path("teacher/attendance/", mark_attendance, name="teacher_attendance"),
    path("teacher/attendance/history/", views.attendance_history,name="attendance_history"),
    path("teacher/performance/at-risk/", views.at_risk_students,name="at_risk_students"),
    path("teacher/attendance/summary/",views.monthly_attendance_summary,name="monthly_attendance_summary"),








    path("students/", views.students_list, name="students_list"),
    path("payments/", views.payments_list, name="payments_list"),
    path('add/', views.student_add, name='student_add'),
    

    # Student Profile page
    path("student_profile/<int:pk>/", views.student_profile, name="student_profile"),
    path("add_payment/<int:pk>/", views.add_payment, name="add_payment"),  # ← ADD 
    path('edit_student/<int:pk>/', views.edit_student, name='edit_student'),
    path("download_receipt/<int:payment_id>/", views.download_receipt, name="download_receipt"),
    path("student_statement/<int:student_id>/", views.student_statement_pdf, name="student_statement_pdf"),
    path("edit_payment/<int:payment_id>/", views.edit_payment, name="edit_payment"),

    path("delete_payment/<int:payment_id>/", views.delete_payment, name="delete_payment"),
    path("api/payment/<int:payment_id>/", views.api_payment_details),
    path("delete_student/<int:student_id>/", views.delete_student, name="delete_student"),
    path("students/", views.students_list, name="student_list"),
    path("add-feestructure-popup/", views.add_feestructure_popup, name="add_feestructure_popup"),
    path('fees/', views.feestructure_list, name='feestructure_list'),
    path('feestructure/delete/<int:pk>/', views.feestructure_delete, name='feestructure_delete'),
    path('feestructure/edit/<int:pk>/', views.feestructure_edit, name='feestructure_edit'),
    path('student/<int:student_id>/mpesa/',views.mpesa_payment,name='mpesa_payment'),
    path("mpesa/callback/", views.mpesa_callback, name="mpesa_callback"),

    path("alerts/<int:alert_id>/reviewed/",views.mark_alert_reviewed,name="mark_alert_reviewed"),




    path("brand/", views.brand_intro, name="brand_intro"),


]




