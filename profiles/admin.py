from django.contrib import admin
from profiles.models import Profile
from profiles.models import BasicUser

admin.site.register(Profile)
admin.site.register(BasicUser)
