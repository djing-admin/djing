import os

from typing import Any
from django.http import FileResponse, Http404, JsonResponse
from Illuminate.Exceptions.RouteNotFoundException import RouteNotFoundException
from djing.core.Http.Requests.ResourceDownloadRequest import ResourceDownloadRequest


class FieldDownloadController:
    def __call__(self, request: ResourceDownloadRequest) -> Any:
        try:
            resource = request.find_resource_or_fail()

            resource.authorize_to_update(request)

            field = resource.downloadable_fields(request).first(
                lambda field: field.attribute == request.route_param("field")
            )

            if not field:
                raise RouteNotFoundException("Field not found")

            download_url = field.to_download_response(request, resource)

            if not os.path.exists(download_url):
                return Http404("File not found.")

            response = FileResponse(open(download_url, "rb"), as_attachment=True)

            response["Content-Disposition"] = (
                f'attachment; filename="{os.path.basename(download_url)}"'
            )

            return response
        except Exception as e:
            return JsonResponse({"data": str(e)}, status=500)
