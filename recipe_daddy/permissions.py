from rest_framework import permissions
from django.shortcuts import get_object_or_404
from recipe_daddy.models.user_models import User

class OwnerOrNoAccessToUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.method == "PUT" or request.method == "DELETE" or request.method == "GET":
            if obj.email == request.user.email:
                return True
        
            return False
            
class OwnerOrNoAccessToRecipe(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.method == "PUT" or request.method == "DELETE" or request.method == "GET":
            if obj.user.email == request.user.email:
                return True
        
            return False
