from django.contrib import admin

# Register your models here.
from .models import Team #UserProfileInfo, Question

# admin.site.register(Question)
admin.site.register(Team)
# admin.site.register(UserProfileInfo)