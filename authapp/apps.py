from django.apps import AppConfig


class AuthappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authapp'

    # Для того, чтобы сигналы подгрузились из отдельного файла signals.py
    def ready(self):
        import authapp.signals
