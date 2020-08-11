from django.urls import path
from .views import UserRegistrationView, UserDetail
from .authtoken_views import CustomObtainAuthToken


urlpatterns = [
    path('register', UserRegistrationView.as_view()),
    path('login', CustomObtainAuthToken.as_view()),
    path('user/profile', UserDetail.as_view())
]