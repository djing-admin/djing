import os
import sys
import django

from django.conf import settings
from Illuminate.Foundation.Application import Application
from djing.core.Foundation.Djing import Djing
from djing.core.Providers.DjingCoreServiceProvider import DjingCoreServiceProvider


def load_django():
    sys.path.insert(0, os.getcwd())

    project_name = os.getenv("DJANGO_PROJECT_NAME", "myproject")

    settings_module = f"{project_name}.settings"

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

    django.setup()

    if not settings.configured:
        settings.configure()


def djing_application():
    if not os.getenv("DJANGO_SETTINGS_MODULE"):
        load_django()

    return (
        Application.configure(base_path=Djing.base_directory())
        .with_providers([DjingCoreServiceProvider])
        .with_routing()
        .with_middleware()
        .with_exceptions()
        .create()
    )
