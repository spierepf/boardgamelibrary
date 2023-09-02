from django.apps import AppConfig


class TestOnlyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'test_only'
