from django.conf.urls import url
from . import views

urlpatterns = [
    # urls for school requests - user side
    url(r"^user/(?P<id>[0-9]+)/update/name/$", views.settings_update_name, name="settings_update_name"),
    url(r"^user/(?P<id>[0-9]+)/update/email/$", views.settings_update_email, name="settings_update_email"),
    url(r"^user/(?P<id>[0-9]+)/update/password/$", views.settings_update_password, name="settings_update_password"),
    url(r"^user/(?P<id>[0-9]+)/add/admin/$", views.settings_add_admins, name="settings_add_admins"),

]
