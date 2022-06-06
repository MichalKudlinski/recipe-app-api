"""Views for the user api"""
from django.shortcuts import render
from . import serializers
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


# Create your views here.

class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer

class CreateTokenView(ObtainAuthToken):
    """
    Crete a new auth token for user
        """

    serializer_class = serializers.AuthTokenSerializer
    renderer_classes= api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class=serializers.UserSerializer
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_object(self):
         """Retrieve and return the authetnicated user"""
         return self.request.user