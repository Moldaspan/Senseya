import json
from io import BytesIO
from django.utils.timezone import now
from django.http import QueryDict
from .models import DiaryEntry


class DiaryLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.body:
            request._body = request.body

        response = self.get_response(request)

        if request.user.is_authenticated:
            self.log_action(request, response)

        return response

    def log_action(self, request, response):
        allowed_endpoints = ["/api/chat/query/", "/api/users/profile/"]
        # print(request.path)
        # print(allowed_endpoints)
        if request.path not in allowed_endpoints:
            return  # Skip logging for other endpoints

        try:
            DiaryEntry.objects.create(
                user=request.user,
                action=self.get_action(request),
                timestamp=now(),
                request_method=request.method,
                endpoint=request.path,
                request_data=self.get_request_data(request),
                response_data=self.get_response_data(response),
            )
        except Exception as e:
            print(f"Error logging action: {e}")

    def get_action(self, request):
        if request.path == "/api/chat/query/" and request.method == "POST":
            return "USER_QUERY"
        elif request.path == "/api/users/profile/" and request.method == "GET":
            return "VIEW_PROFILE"
        return f"{request.method} {request.path}"

    def get_request_data(self, request):
        try:
            if hasattr(request, "_body"):
                body = request._body
            else:
                body = request.body

            if request.content_type == "application/json":
                return json.loads(body) if body else {}
            elif request.content_type == "application/x-www-form-urlencoded":
                return QueryDict(body).dict()
            return {}
        except Exception as e:
            print(f"Error parsing request data: {e}")
            return {}

    def get_response_data(self, response):
        try:
            return json.loads(response.content) if response.content else {}
        except json.JSONDecodeError:
            return {}
