from django.urls import path, include
from .views import UserRegistrationView, UserDetail, UserUpdate
from .authtoken_views import CustomObtainAuthToken
from .views import UserRegistrationView, activate

user_url = [
    path('profile', UserDetail.as_view(), name='user-profile'),
    path('update', UserUpdate.as_view(), name = 'user-update'),
    path('activate/<uidb64>/<token>', activate, name='user-activate')
]


urlpatterns = [
    path('register', UserRegistrationView.as_view(), name='user-register'),
    path('login', CustomObtainAuthToken.as_view(), name='user-login'),
    path('user/', include(user_url))
]