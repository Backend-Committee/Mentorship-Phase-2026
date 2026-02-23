from django.utils.timezone import activate as activate_time_zone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (
            request.user.is_authenticated
            and request.user.profile is not None
            and request.user.profile.timezone is not None
        ):
            activate_time_zone(request.user.profile.timezone)

        response = self.get_response(request)

        return response
