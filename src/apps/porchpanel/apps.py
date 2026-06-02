from django.apps import AppConfig


class PorchpanelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.apps.porchpanel'

    def ready(self):
        import src.apps.porchpanel.signals
