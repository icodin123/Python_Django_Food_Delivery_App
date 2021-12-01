from . import settings
from applications.models import Notification

class NotificationsGetter:

    def __init__(self, get_response):
        self.get_response = get_response

    # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        self.process_request(request)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def get_top_notifications(self, threshold, request):
        try:
            if(request.user.user_type == 'BSC'):
                return []
            new_notifications = Notification.objects.filter(is_dismissed=0).order_by('-created_at')[0:threshold]
            return new_notifications
        except:
            print("not logged in")
            return []

    def process_request(self, request):
        notifications = self.get_top_notifications(settings.NOTIFICATION_THRESHOLD, request)
        request.notifications = notifications
        request.num_notifications = len(notifications)
