from django.apps import AppConfig
from pathlib import Path


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    path = Path(__file__).resolve().parent
