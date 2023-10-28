from rest_framework import serializers
from recipe_daddy.models.user_models import User

class LeaderboardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["username", "food_saved"]
        