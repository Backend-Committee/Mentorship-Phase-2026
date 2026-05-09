from django.apps import AppConfig

class RackingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'racking'

    def ready(self):
        import racking.signals 