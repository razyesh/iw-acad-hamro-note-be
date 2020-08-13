from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.core.mail import EmailMessage

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import (CreateAPIView,
                                     RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from .serializers import UserRegisterSerializer, UserUpdateSerializer
from .tokens import account_activation_token

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
        return Response(user_data.data, status=status.HTTP_302_FOUND)


class UserUpdate(UpdateAPIView):
    """
    API end point to update the user object
    who is currently active
    """
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    serializer_class = UserUpdateSerializer

    def update(self, request, *args, **kwargs):
        """partially updating the user"""

        partial = kwargs.pop('partial', False)
        instance = User.objects.get(id=request.user.id)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.profile_pic = request.FILES.get('profile_pic')
        print(request.FILES)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegistrationView(CreateAPIView):
    """API view for User Registration"""
    serializer_class = UserRegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """accepting post request and serializer validation"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        current_site = get_current_site(self.request)
        mail_subject = "Activate your Hamro Note Account"
        message = render_to_string('account_activate_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        })
        to_email = serializer.validated_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        response = {
            'success': True,
            'message': "Please Activate your account before proceeding"
        }
        return Response(response, status=status.HTTP_201_CREATED)


@api_view(('GET',))
def activate(request, uidb64, token):
    """User activation function"""
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        response = {
            'status': 'Success',
            'message': "User successfully activated. Please login now"
        }
        return Response(response, status=status.HTTP_200_OK)
    else:
        response = {
            'status': 'Failed',
            'message': "Either the token is expired or you are not registered yet"
        }
        return Response(response, status=status.HTTP_401_UNAUTHORIZED)
