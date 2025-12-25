from django.apps import AppConfig
from pathlib import Path


class StudentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'students'
    path = Path(__file__).resolve().parent
