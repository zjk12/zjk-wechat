from django.http import JsonResponse


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.username in ["zjkd"] and (not request.path.startswith("/admin")):
            return JsonResponse({"result": False, "message":"You're banned for 30 days "})

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response