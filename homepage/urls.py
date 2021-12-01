"""
urls for homepage
"""
import django
from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r"^", include("profiles.urls", namespace="profiles")),
    url(r"^admin/", include("applications.admin_urls", namespace="admin")),
    url(r"^django/admin/", admin.site.urls),
    # url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r"^requests/", include("applications.requests_urls", namespace="requests")),
    url(r"^documents/", include("documents.urls", namespace="documents")),
    url(r"^", include("applications.urls", namespace="applications")),
    url(r'^settings/$', views.user_settings, name='user_settings'),
    url(r'^resources/$', views.user_resources, name='user_resources'),
    url(r"^settings/", include("applications.settings_urls", namespace="settings")),



    url(r'^password-reset/$', django.contrib.auth.views.password_reset, name='password_reset'),

    url(r'^password-reset/done/$', django.contrib.auth.views.password_reset_done, name='password_reset_done'),

    url(r'^password-reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        django.contrib.auth.views.password_reset_confirm, name='password_reset_confirm'),

    url(r'^password-reset/complete/$', django.contrib.auth.views.password_reset_complete,
        name='password_reset_complete'),
]
