from rest_framework import serializers
from django.utils import timezone

from recipe_daddy.models.user_meal_plan_models import UserMealPlan

class UserMealPlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserMealPlan
        fields = "__all__"
        read_only_fields = ["created_at"]
    
    # def create(self, validated_data):
    #     validated_data["created_at"] = timezone.now()
    #     user_meal_plan_instance = UserMealPlan.objects.create(**validated_data)
    #     return user_meal_plan_instance