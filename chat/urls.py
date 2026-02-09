from django.urls import path
from .views import chat_home

urlpatterns = [
    path("chat/", chat_home, name="chat_home"),
    path("chat/<int:user_id>/", chat_home, name="chat_with_user"),
    
]
