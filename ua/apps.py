from django.apps import AppConfig

class UaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ua'

    def ready(self):  # ✅ Dapat nasa loob ng UaConfig class
        import ua.signals
