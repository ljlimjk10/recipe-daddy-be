from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated

from recipe_daddy.models.recipe_models import Recipe
from recipe_daddy.serializers.recipe_serializers import RecipeSerializer
from recipe_daddy.helpers.mixins_helpers import MultipleFieldLookupMixin
from recipe_daddy.permissions import OwnerOrNoAccessToRecipe


class RecipeList(generics.GenericAPIView,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RecipeDetails(generics.GenericAPIView,
                    MultipleFieldLookupMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):
    
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated, OwnerOrNoAccessToRecipe]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

