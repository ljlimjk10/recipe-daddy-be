from django.db import models
from recipe_daddy.models.user_models import User

class MealTypes(models.IntegerChoices):
    BREAKFAST = 1
    LUNCH = 2
    DINNER = 3

class UserMealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_date = models.DateField()
    meal_type = models.CharField(max_length=10, choices=MealTypes.choices)
    recipe_name = models.CharField(max_length=255)
    image_url = models.TextField(null=True, blank=True)
    have_ingredients = models.JSONField(null=True, blank=True)
    no_ingredients = models.JSONField(null=True, blank=True)
    preparation_steps = models.TextField(null=True, blank=True)
    canMake = models.BooleanField(default=False)
    isCompleted = models.BooleanField(default=False)