from django.db import models
from recipe_daddy.models.user_models import User
from recipe_daddy.models.recipe_models import Recipe

class MealTypes(models.IntegerChoices):
    BREAKFAST = 1
    LUNCH = 2
    DINNER = 3

class UserMealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal_date = models.DateTimeField()
    meal_type = models.CharField(max_length=10, choices=MealTypes.choices)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)