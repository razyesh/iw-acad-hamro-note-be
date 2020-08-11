from django.urls import path
from .views import UserRegistrationView, UserDetail
from .authtoken_views import CustomObtainAuthToken
from .views import UserRegistrationView

urlpatterns = [
    path('register', UserRegistrationView.as_view(), name='user-register'),
    path('login', CustomObtainAuthToken.as_view(), name='user-login'),
    path('user/profile', UserDetail.as_view(), name='user-profile')
]