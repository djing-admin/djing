import re

from django.conf import settings
from django.db.models import Model
from django.db.models.fields.files import FileField, ImageField
from django.forms.models import model_to_dict
from djing.core.Http.Requests.DjingRequest import DjingRequest
from djing.core.Facades.Djing import Djing


class Util:
    @classmethod
    def is_email_address(cls, s: str) -> bool:
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        return bool(re.match(email_regex, s))

    @classmethod
    def username_field(cls):
        return settings.USERNAME_FIELD

    @classmethod
    def auth_user_model(cls):
        return settings.AUTH_USER_MODEL

    @classmethod
    def is_djing_request(cls, request: DjingRequest):
        request_path = request.get_url()

        path = Djing.path().strip("/") or "/"

        result = (
            re.match(rf"^/{path}/?$", request_path)
            or re.match(rf"^/{path}/.*$", request_path)
            or re.match(r"^/djing-api/.*$", request_path)
            or re.match(r"^/djing-vendor/.*$", request_path)
        )

        return result is not None

    @classmethod
    def is_djing_api_request(cls, request: DjingRequest):
        request_path = request.get_url()

        result = re.match(r"^/djing-api/.*$", request_path) or re.match(
            r"^/djing-vendor/.*$", request_path
        )

        return result is not None

    @classmethod
    def is_dev_mode(cls, debug=None) -> bool:
        debug = debug if debug else settings.DEBUG

        if isinstance(debug, bool):
            return debug

        if isinstance(debug, (str, int)):
            return int(debug) == 1

        return False

    @classmethod
    def get_key_name(cls, resource: Model):
        return resource._meta.pk.name

    @classmethod
    def model_to_dict(cls, instance, fields=None, exclude=None):
        data = model_to_dict(instance, fields=fields, exclude=exclude)

        for field in instance._meta.fields:
            if isinstance(field, (FileField, ImageField)):
                file_field = getattr(instance, field.name)
                data[field.name] = file_field.url if file_field else None

        return data
