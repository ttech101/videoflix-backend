from django.apps import AppConfig


class StorageConfig(AppConfig):
    """
    AppConfig class for the 'storage' app.
    This class defines configuration options for the 'storage' app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'storage'

    def ready(self):
        """
        Method called when the app is ready.
        This method imports signals module to ensure signal handling is set up when the app is ready.
        """
        from . import signals
