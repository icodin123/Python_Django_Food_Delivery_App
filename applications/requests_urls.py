from django.conf.urls import url
from . import views

app_name = 'applications'

urlpatterns = [
    # urls for school requests - user side
    url(r"^$", views.requests_list, name="requests"),
    url(r"new", views.new_request, name="createRequest"),
    url(r"edit/(?P<id>[0-9]+)/", views.edit_request, name="edit"),
]
