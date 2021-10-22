from django.contrib import admin
from .models import CustomUser, Posts, Friendship


admin.site.register(CustomUser)
admin.site.register(Posts)
admin.site.register(Friendship)