from django.urls import path
from django.shortcuts import redirect
from . import views


urlpatterns = [
    # Redirect homepage → dashboard
    path('', lambda request: redirect('dashboard')),

    # Dashboard page
    path("dashboard/", views.dashboard, name="dashboard"),
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

    path("brand/", views.brand_intro, name="brand_intro"),


]




