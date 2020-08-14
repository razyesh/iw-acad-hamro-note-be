from django.contrib import admin

from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/blog',include('blog.api.urls')),
    path('', include('accounts.urls', namespace='account')),
    path('posts/', include('posts.urls', namespace='posts'))
]

admin.site.site_header = 'Hamro Notes'