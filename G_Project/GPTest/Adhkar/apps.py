from django.apps import AppConfig

class AdhkarConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Adhkar' 

    def ready(self):
        import Adhkar.signals 