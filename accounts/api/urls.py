from django.urls import path
from .views import UserRegistrationView, UserDetail, UserUpdate
from .authtoken_views import CustomObtainAuthToken
from .views import UserRegistrationView

urlpatterns = [
    path('register', UserRegistrationView.as_view()),
    path('login', CustomObtainAuthToken.as_view()),
    path('user/profile', UserDetail.as_view()),
    path('user/update', UserUpdate.as_view()),
]