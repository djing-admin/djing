import os
import inertia

from pathlib import Path
from django.conf import settings as django_settings
from inertia.settings import settings as inertia_settings
from dotenv import load_dotenv

load_dotenv()


class InertiaApplication:
    def __init__(self):
        self.package_path = Path(__file__).resolve().parent

        self.middlewares = [
            "inertia.middleware.InertiaMiddleware",
        ]

    def add_middleware(self, middleware):
        if middleware not in self.middlewares:
            self.middlewares.append(middleware)

        return self

    def run(self):
        try:
            merged_settings = self.__get_merged_settings()

            for key, value in merged_settings.items():
                setattr(django_settings, key, value)

            django_settings.TEMPLATES[0]["DIRS"].extend(self.get_template_dirs())

            django_settings.STATICFILES_DIRS.extend(self.get_static_dirs())

            for middleware in self.middlewares:
                if middleware not in django_settings.MIDDLEWARE:
                    django_settings.MIDDLEWARE.append(middleware)
        except Exception as e:
            raise Exception(e)

    def key_exist(self, key) -> bool:
        return (
            hasattr(django_settings, key) and getattr(django_settings, key) is not None
        )

    def __get_merged_settings(self):
        merged_settings = {}

        for key, value in self.django_breeze_settings.items():
            if key in ["INERTIA", "DJANGO_VITE"]:
                for sub_key, sub_value in value.items():
                    sub_key = f"{key}_{sub_key}"
                    if not self.key_exist(sub_key):
                        merged_settings[sub_key] = sub_value
            else:
                merged_settings[key] = value

        return merged_settings

    def get_template_dirs(self) -> list:
        return [
            self.package_path / "templates",
            Path(inertia.__file__).resolve().parent / "templates/",
        ]

    def get_static_dirs(self) -> list:
        DJANGO_VITE_ASSETS_PATH = getattr(django_settings, "DJANGO_VITE_ASSETS_PATH")

        dirs = [
            DJANGO_VITE_ASSETS_PATH,
        ]

        components_path = Path(os.path.join(os.getcwd(), "djing_components/dist"))

        if components_path.exists():
            dirs.append(components_path)

        return dirs

    @property
    def django_breeze_settings(self):
        return {
            "INERTIA": {
                "LAYOUT": "index.html",
                "SSR_URL": inertia_settings.INERTIA_SSR_URL,
                "SSR_ENABLED": inertia_settings.INERTIA_SSR_ENABLED,
                "JSON_ENCODER": inertia_settings.INERTIA_JSON_ENCODER,
            },
            "DJANGO_VITE": {
                "DEV_MODE": os.getenv("DJING_DEBUG") == "true",
                "SERVER_PROTOCOL": "http",
                "DEV_SERVER_HOST": "localhost",
                "DEV_SERVER_PORT": 5183,
                "WS_CLIENT_URL": "@vite/client",
                "ASSETS_PATH": self.package_path / "dist",
                "STATIC_URL_PREFIX": "",
                "LEGACY_POLYFILLS_MOTIF": "legacy-polyfills",
            },
            "CSRF_HEADER_NAME": "HTTP_X_XSRF_TOKEN",
            "CSRF_COOKIE_NAME": "XSRF-TOKEN",
        }
