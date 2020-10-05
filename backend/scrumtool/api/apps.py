from django.apps import AppConfig


class ApiConfig(AppConfig):
    name = 'api'

# import signals
    def ready(self):
        import api.signals
