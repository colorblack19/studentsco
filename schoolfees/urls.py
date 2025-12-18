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

urlpatterns = [
    path('admin/', admin.site.urls),

    # BRAND INTRO (HOME PAGE)
    path('', brand_intro, name='home'),

    # AUTH (LOGIN / REGISTER / DASHBOARD)
    path('accounts/', include('accounts.urls')),

    # STUDENTS / SYSTEM
    path('students/', include('students.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
