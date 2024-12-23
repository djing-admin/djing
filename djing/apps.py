from django.apps import AppConfig

from djing.inertia_application import InertiaApplication


class DjingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"

    name = "djing"

    def ready(self):
        inertia_application = InertiaApplication()

        inertia_application.add_middleware("djing.djing_middleware.DjingMiddleware")

        inertia_application.run()
