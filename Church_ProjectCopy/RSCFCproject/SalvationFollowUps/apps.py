from django.apps import AppConfig


class SalvationfollowupsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'SalvationFollowUps'

    def ready(self):
        import SalvationFollowUps.signals
