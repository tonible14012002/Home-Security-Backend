from django.apps import AppConfig
from django.core.signals import request_finished


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    def ready(self):
            # Implicitly connect signal handlers decorated with @receiver.
            import accounts.signals