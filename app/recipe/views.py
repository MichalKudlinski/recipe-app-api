"""Views for recipe endpoints"""
from django.shortcuts import render
from core.models import Recipe
from .serializers import RecipeSerializer, RecipeDetailSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class =RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes= [TokenAuthentication]
    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        """Retrieve queryset for authenticated user"""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """ return serialzier class for request."""
        if self.action == 'list':
            return RecipeSerializer

        return self.serializer_class