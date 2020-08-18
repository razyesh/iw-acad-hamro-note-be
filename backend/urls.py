from django.contrib import admin

from django.urls import path, include
from .views import index

urlpatterns = [
    path('',index),
    path('admin/', admin.site.urls),
    path('api/blog/',include('blog.api.urls')),
    path('api/accounts/', include('accounts.urls', namespace='account')),
    path('api/posts/', include('posts.urls', namespace='posts')),
]

admin.site.site_header = 'Hamro Notes'
