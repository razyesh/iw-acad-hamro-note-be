from rest_framework.authtoken.views import ObtainAuthToken
from .authtoken_serializer import AuthTokenSerializer


class CustomObtainAuthToken(ObtainAuthToken):
    """
    overriding default serializer class
    of ObtainAuthToken
    """
    serializer_class = AuthTokenSerializer
