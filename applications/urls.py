from django.conf.urls import url
from homepage import views

app_name = 'applications'

urlpatterns = [
    url(r"^apply/$", views.apply, name="apply"),
    url(r"^application/status/$", views.apply_status, name="application_status"),

]
