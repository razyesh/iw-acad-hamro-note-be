from django.contrib import admin
from . import models

education_models = [models.Education, models.University, models.College, models.Faculty]
user_models = [models.Profile, models.UserFollow]

admin.site.register(education_models)
admin.site.register(user_models)
