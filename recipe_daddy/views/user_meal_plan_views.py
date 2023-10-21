from rest_framework import mixins, generics
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied

from recipe_daddy.models.user_meal_plan_models import UserMealPlan
from recipe_daddy.serializers.user_meal_plan_serializers import UserMealPlanSerializer
from recipe_daddy.helpers.mixins_helpers import MultipleFieldLookupMixin
from recipe_daddy.permissions import OwnerOrNoAccessToMealPlan

# TODO user shld only have 1 breafast lunch dinner per day max

class UserMealPlanViewSet(
                        MultipleFieldLookupMixin,
                        generics.GenericAPIView,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin):
    
    queryset = UserMealPlan.objects.all()
    serializer_class = UserMealPlanSerializer
    lookup_fields = ['user__username', 'meal_date']

    def get_permissions(self):
        if self.request.method == "GET" or self.request.method == "POST":
            return [IsAuthenticated()]
        else:
            return [OwnerOrNoAccessToMealPlan()]
        
    def get_queryset(self):
        queryset = UserMealPlan.objects.all()
        username = self.request.query_params.get("username")
        meal_date = self.request.query_params.get("meal_date")
        pk = self.request.query_params.get("id")

        if pk is not None:
            return queryset.filter(pk=pk)

        if username is not None:
            if self.request.user.is_authenticated and self.request.user.email == username:
                if meal_date is not None:
                    queryset = queryset.filter(user__username=username, meal_date=meal_date)
                else:
                    queryset = queryset.filter(user__username=username)
            else:
                raise PermissionDenied()

        return queryset


    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        meal_type = request.data.get("meal_type")
        meal_date = request.data.get("meal_date")
        user = request.user

        existing_meal_plan = UserMealPlan.objects.filter(
                                user=user,
                                meal_type=meal_type,
                                meal_date=meal_date
                            ).first()
        if existing_meal_plan:
            try:
                existing_meal_plan.delete()
            except Exception as e:
                print(f"Error deleting meal plan: {e}")

        return super().create(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
