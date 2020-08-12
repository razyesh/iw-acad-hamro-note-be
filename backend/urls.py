from django.contrib import admin
<<<<<<< HEAD
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/blog',include('blog.api.urls')),
=======
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls', namespace='account')),
    path('', include('posts.urls', namespace='posts'))
>>>>>>> f90bd630ab6adc41d925f6ce3731a39351ae7f4f
]
