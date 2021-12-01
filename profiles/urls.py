from django.conf.urls import url
from . import views

app_name = 'profiles'

urlpatterns = [
    url(r'^login', views.login_function, name='user_login'),
    url(r"^logout", views.logout_function, name="logout"),
    url(r'^signup', views.signup_function, name='register'),
]
