import traceback
from django.http import JsonResponse
from shared.models import ErrorLog
from shared.utils.Global import ERROR_MESSAGE, LOGGING_SAVE


class Log500ErrorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        LOGGING_SAVE(exc=exception, url=request.get_full_path())
        exception_attrs = vars(exception)
        return JsonResponse(
            ERROR_MESSAGE(
                tipo=type(exception).__name__,
                message=exception.__str__(),
                fields_errors={},
                url=request.get_full_path(),
            ),
            status=500,
        )
