from django.contrib import admin
from .models import CustomUser, Posts, Friendship, TagsOfInterest, UserInterestTags


admin.site.register(CustomUser)
admin.site.register(Posts)
admin.site.register(Friendship)
admin.site.register(TagsOfInterest)
admin.site.register(UserInterestTags)