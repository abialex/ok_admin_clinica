import traceback

from django.http import JsonResponse


class Log500ErrorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        return JsonResponse({
            "tipo": type(exception).__name__,
            "message": exception.__str__(),
            "field_errors": {},
            "url": request.get_full_path(),
        }, status=500)