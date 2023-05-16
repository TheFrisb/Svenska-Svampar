from django.apps import AppConfig


class ShopmanagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shopmanager'

    def ready(self):
        import shopmanager.signals
