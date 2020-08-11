from django.contrib.auth import get_user_model
from django.core import serializers

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import (CreateAPIView,
                                        RetrieveAPIView,
                                        UpdateAPIView)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .serializers import (UserRegisterSerializer,
                             UserProfileSerializer,
                             UserUpdateSerializer)
from accounts.models.profile import Profile
from accounts.models.education import Education


User = get_user_model()


class UserDetail(RetrieveAPIView):
    """
    API end point to retrieve the user object
    who is currently active
    """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        """
        returns the user detail
        :return: JSON response of user detail
        """
        user = User.objects.get(id=request.user.id)
        user_data = UserRegisterSerializer(user)
        return Response(user_data.data)

class UserUpdate(UpdateAPIView):
    """
    API end point to update the user object
    who is currently active
    """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserUpdateSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = User.objects.get(id = request.user.id)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class UserRegistrationView(CreateAPIView):
    """API view for User Registration"""
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """accepting post request and serializer validation"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'success': True,
            'message': "User successfully created"
        }
        return Response(response, status=status.HTTP_201_CREATED)
