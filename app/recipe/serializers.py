from rest_framework import serializers
from core.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    """Serialzier for recipes"""
    class Meta:
        model= Recipe
        fields=['id','title','time_minutes','price','link']
        read_only_fields=['id']
class RecipeDetailSerializer(RecipeSerializer): # we use enharitance because we want to use everying in recipeseriliazer
    class Meta(RecipeSerializer.Meta):
        fields= RecipeSerializer.Meta.fields +['description']