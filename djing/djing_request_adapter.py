import json

from urllib.parse import parse_qs
from django.http import HttpRequest
from django.http.multipartparser import MultiPartParser
from Illuminate.Http.RequestAdapter import RequestAdapter


class DjingRequestAdapter(RequestAdapter):
    def __init__(self, request: HttpRequest):
        self.request: HttpRequest = request

        self.__cached_multipart_data: dict = {}

    def get_host(self):
        return self.request.get_host()

    def get_url(self):
        return self.request.path

    def get_full_url(self):
        return self.request.get_full_path()

    def get_method(self):
        return self.request.method

    def get_user(self):
        return self.request.user

    def query_data(self):
        return self.request.GET.dict()

    def post_data(self):
        return self.request.POST.dict()

    def files_data(self):
        return self.request.FILES.dict()

    def form_data(self):
        content_type = self.request.META.get("CONTENT_TYPE", "")

        if "multipart/form-data" in content_type:
            data = self.multipart_data()
        elif "application/x-www-form-urlencoded" in content_type:
            data = self.urlencoded_data()
        else:
            data = self.json_data()

        return data

    def multipart_data(self):
        try:
            if self.__cached_multipart_data:
                return self.__cached_multipart_data

            parser = MultiPartParser(
                self.request.META, self.request, self.request.upload_handlers
            )

            form_data, files_data = parser.parse()

            def map_data(value):
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value

            form = {key: map_data(value) for key, value in form_data.items()}

            files = {
                key: values[0] if len(values) == 1 else values
                for key, values in files_data.items()
            }

            self.__cached_multipart_data = {**form, **files}

            return self.__cached_multipart_data
        except Exception as e:
            print("multipart_data error", e)

    def urlencoded_data(self):
        decoded = self.request.body.decode("utf-8")

        data = parse_qs(decoded)

        return {
            key: values[0] if len(values) == 1 else values
            for key, values in data.items()
        }

    def json_data(self):
        try:
            decoded = self.request.body.decode("utf-8")

            return json.loads(decoded)
        except json.JSONDecodeError:
            return {}

    def headers_data(self):
        return {key: value for key, value in self.request.headers.items()}

    def sessions_data(self):
        return {key: value for key, value in self.request.session.items()}

    def cookies_data(self):
        return {key: value for key, value in self.request.COOKIES.items()}
