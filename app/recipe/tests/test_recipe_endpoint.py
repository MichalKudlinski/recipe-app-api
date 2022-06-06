"""Tests recipe apis"""
from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core import models

from recipe.serializers import RecipeSerializer, RecipeDetailSerializer


RECIPES_URL=reverse('recipe:recipe-list')

def detail_url(recipe_id):
    """Create and returna recipe detail URL."""
    return reverse('recipe:recipe-detail',args=[recipe_id])
def create_recipe(user, **params):
    """Create and return a sample recipe."""
    defaults={
        'title': 'Sample recipe title',
        'time_minutes':22,
        'price':Decimal('5.25'),
        'description':'sample desc',
        'link':'http://example.com/recipe.pdf',
    }
    defaults.update(params)
    recipe=models.Recipe.objects.create(user=user, **defaults)

    return recipe

class PublicRecipeAPITests(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self):
        self.client=APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res=self.client.get(RECIPES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivateRecipeAPITests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.client=APIClient()
        self.user =get_user_model().objects.create_user('user@example.com','pass1234')
        self.client.force_authenticate(self.user)

    def test_retrive_recipes(self):
        """Test retrieving a list of recipes"""
        create_recipe(user=self.user)
        create_recipe(user=self.user)

        res=self.client.get(RECIPES_URL)
        recipes=models.Recipe.objects.all().order_by('-id')
        serializer=RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)
    def test_reipe_list_limited_to_user(self):
        '''Tests retrieving a list of recipes for a specified user'''
        other_user=get_user_model().objects.create_user('user2@example.com','testpass12345')
        create_recipe(user=other_user)
        create_recipe(user=self.user)

        res = self.client.get(RECIPES_URL)
        recipes = models.Recipe.objects.filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)
    def test_recipe_detail(self):
        """Test get recipe detial"""
        recipe = create_recipe(user=self.user)
        url=detail_url(recipe.id)
        res=self.client.get(url)

        serializer=RecipeDetailSerializer(recipe)
        self.assertEqual(res.data,serializer.data)
    def test_create_recipe(self):
        """Test creating a recipe"""
        payload={
        'title': 'Sample recipe title1',
        'time_minutes':23,
        'price':Decimal('5.27'),
        'description':'sample desc1',
        'link':'http://example.com/recipe1.pdf',
         }
        res =self.client.post(RECIPES_URL, payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        recipe = models.Recipe.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(recipe,k),v)

        self.assertEqual(recipe.user,self.user)