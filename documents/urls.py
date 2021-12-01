from django.conf.urls import url
from . import views

app_name = 'documents'

urlpatterns = [
    url(r'^$', views.index, name='index')
]