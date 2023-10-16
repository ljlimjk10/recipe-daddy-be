from django.db import models
from . import User

class Recipe(models.Model):
    user = models.ForeignKey(User, related_name="recipe", on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=150)
    canMake = models.BooleanField(default=False)
    completionStatus = models.BooleanField(default=False)
    ingredients_possessed = models.JSONField(null=True, blank=True)
    ingredients_not_possessed = models.JSONField(null=True, blank=True)
    preparation_steps = models.TextField()
    created_at = models.DateTimeField()


