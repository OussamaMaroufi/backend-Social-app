from django.contrib import admin
from .models import UserProfile, OnlineUser


admin.site.register(UserProfile)
admin.site.register(OnlineUser)
