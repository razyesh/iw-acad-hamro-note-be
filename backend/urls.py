from django.contrib import admin

from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/blog',include('blog.api.urls')),
    path('', include('accounts.urls', namespace='account')),
    path('', include('posts.urls', namespace='posts')),
]
