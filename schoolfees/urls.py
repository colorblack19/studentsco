"""
URL configuration for schoolfees project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from students.views import brand_intro
from accounts.views import home_dashboard

urlpatterns = [

    # 🔥 MAIN DASHBOARD (AFTER LOGIN)
    path("", home_dashboard, name="home_dashboard"),

    # 🔹 BRAND / LANDING PAGE
    path("brand/", brand_intro, name="home"),

    # 🔹 CHAT SYSTEM
    path("chat/", include("chat.urls")),

    # 🔹 EVENTS
    path("events/", include("events.urls")),

    # 🔹 AUTH
    path("accounts/", include("accounts.urls")),

    # 🔹 STUDENTS
    path("students/", include("students.urls")),

    # 🔹 TIMETABLE
    path("timetable/", include("timetable.urls")),

    # 🔹 ADMIN
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
