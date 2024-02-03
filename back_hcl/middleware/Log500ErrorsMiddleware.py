import logging
import traceback

from django.http import JsonResponse

from back_hcl.utils.Global import error_message
from shared.models import ErrorLog


class Log500ErrorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        tb_info = traceback.extract_tb(exception.__traceback__)
        file_name_error = "--"
        if tb_info:
            file_name_error = tb_info[-1].filename

        ErrorLog.objects.create(
            tipo=type(exception).__name__,
            mensaje=str(exception),
            url=request.get_full_path(),
            archivo=file_name_error
        )
        return JsonResponse({
            "tipo": type(exception).__name__,
            "message": exception.__str__(),
            "field_errors": {},
            "url": request.get_full_path(),
        }, status=500)