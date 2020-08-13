from django.contrib import admin
from .models import User, Profile, Education, University, Faculty, College

admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Education)
admin.site.register(University)
admin.site.register(Faculty)
admin.site.register(College)