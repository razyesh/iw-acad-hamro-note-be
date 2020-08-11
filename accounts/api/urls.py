from django.urls import path
from .authtoken_views import CustomObtainAuthToken
from .views import UserRegistrationView

urlpatterns = [
    path('register', UserRegistrationView.as_view()),
    path('login', CustomObtainAuthToken.as_view())
]