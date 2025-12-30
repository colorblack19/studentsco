from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import add_teacher 
from .views import group_list, group_edit

from .views import after_login_redirect

urlpatterns = [
    
 
    path('', views.login_user, name='login'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),

    

    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_user, name='logout'),
    path("admin/add-teacher/", add_teacher, name="add_teacher"),
    # USERS
    path("users/", views.user_list, name="user_list"),
    path("users/add/", views.user_add, name="user_add"),
    path("users/<int:id>/edit/", views.user_edit, name="user_edit"),
    path("users/<int:id>/delete/", views.user_delete, name="user_delete"),


    path("groups/", group_list, name="group_list"),
    path("groups/<int:id>/edit/", group_edit, name="group_edit"),







   # --- PASSWORD RESET SYSTEM ---
     path('password-reset/',
     auth_views.PasswordResetView.as_view(
         template_name='accounts/password_reset.html'
     ),
     name='password_reset'),


    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name='password_reset_complete'),


    path("redirect/", after_login_redirect, name="after_login_redirect"),
    path("about/", views.about_us, name="about"),
    
]
