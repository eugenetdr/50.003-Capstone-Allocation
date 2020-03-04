from django.contrib import admin

# Register your models here.
from .models import Question, Team, UserProfileInfo

admin.site.register(Question)
admin.site.register(Team)
admin.site.register(UserProfileInfo)