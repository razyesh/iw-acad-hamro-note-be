from django.contrib import admin
from .models import Profile
from .models import Education
from .models import University
from .models import Faculty
from .models import College


admin.site.register(Profile)
admin.site.register(Education)
admin.site.register(University)
admin.site.register(Faculty)
admin.site.register(College)