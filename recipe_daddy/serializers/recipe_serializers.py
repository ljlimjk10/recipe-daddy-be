from rest_framework import serializers
from recipe_daddy.models.recipe_models import Recipe
from django.utils import timezone

class RecipeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Recipe
        fields = "__all__"
        read_only_fields = ["created_at"]

    def create(self, validated_data):
        validated_data['created_at'] = timezone.now()
        recipe_instance = Recipe.objects.create(**validated_data)
        return recipe_instance