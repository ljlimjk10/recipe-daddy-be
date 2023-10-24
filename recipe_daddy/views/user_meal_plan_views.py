from rest_framework import mixins, generics, status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from recipe_daddy.models.user_models import User
from recipe_daddy.models.user_meal_plan_models import UserMealPlan, MealTypes
from recipe_daddy.serializers.user_meal_plan_serializers import UserMealPlanSerializer
from recipe_daddy.helpers.mixins_helpers import MultipleFieldLookupMixin
from recipe_daddy.helpers.user_meal_plan_helpers import handling_meal_type_existence, get_target_meal, generate_meal_image
from recipe_daddy.permissions import OwnerOrNoAccessToMealPlan


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
            curr_username = User.objects.get(email=self.request.user.email).username
            if self.request.user.is_authenticated and curr_username == username:
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
        meal_plan_data = request.data

        if isinstance(meal_plan_data, list):
            meal_plans = []
            user = request.user
            user_id = user.id
            for meal_plan_item in meal_plan_data:
                meal_type = meal_plan_item.get("meal_type")
                meal_date = meal_plan_item.get("meal_date")

                handling_meal_type_existence(user, meal_type, meal_date)

                serializer = UserMealPlanSerializer(
                    data={
                        "user": user_id,
                        "meal_type": meal_type,
                        "meal_date": meal_date,
                        "recipe_name": meal_plan_item.get("recipe_name"),
                        "have_ingredients": meal_plan_item.get("have_ingredients"),
                        "no_ingredients": meal_plan_item.get("no_ingredients"),
                        "preparation_steps": meal_plan_item.get("preparation_steps"),
                        "canMake": meal_plan_item.get("canMake"),
                    }
                )
                if serializer.is_valid():
                    recipe_name = meal_plan_item.get("recipe_name")
                    image_url, status_code = generate_meal_image(recipe_name)

                    if image_url:
                        serializer.validated_data["image_url"] = image_url

                    serializer.save()
                    meal_plans.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(meal_plans, status=status.HTTP_201_CREATED)
        else:
            meal_type = meal_plan_data.get("meal_type")
            meal_date = meal_plan_data.get("meal_date")
            user_id = request.user.id

            handling_meal_type_existence(user_id, meal_type, meal_date)
            serializer = UserMealPlanSerializer(
                data={
                    "user": user_id,
                    "meal_type": meal_type,
                    "meal_date": meal_date,
                    "recipe_name": meal_plan_data.get("recipe_name"),
                    "have_ingredients": meal_plan_data.get("have_ingredients"),
                    "no_ingredients": meal_plan_data.get("no_ingredients"),
                    "preparation_steps": meal_plan_data.get("preparation_steps"),
                    "canMake": meal_plan_data.get("canMake"),
                }
            )
            if serializer.is_valid():
                recipe_name = meal_plan_data.get("recipe_name")
                image_url, status_code = generate_meal_image(recipe_name)

                if image_url:
                    serializer.validated_data["image_url"] = image_url

                serializer.save()
                return super().create(request, *args, **kwargs)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # if update isCompleted to True
        is_completed = serializer.validated_data.get("isCompleted", False)
        meal_type = serializer.validated_data.get("meal_type", None)
        meal_date = serializer.validated_data.get("meal_date", None)

        if is_completed:
            curr_completion_status = instance.isCompleted
            if not curr_completion_status:
                have_ingredients = instance.have_ingredients
                additional_food_saved = sum(have_ingredients.values())

                user = request.user
                user.food_saved += additional_food_saved
                user.save()
                instance.isCompleted = True
                instance.save()
        
        if meal_type and not meal_date:
            curr_meal_type = instance.meal_type
            curr_meal_date = instance.meal_date
            if curr_meal_type != meal_type:
                target_meal_plan_instance = get_target_meal(request.user, meal_type, curr_meal_date)
                if target_meal_plan_instance:
                    target_meal_completion_status = target_meal_plan_instance.isCompleted 
                    if target_meal_completion_status:
                        return Response(
                            f"Unable to change meal_type to {MealTypes(meal_type).name} "
                            f"as it is already marked as complete",
                            status=status.HTTP_400_BAD_REQUEST
                        )
                handling_meal_type_existence(request.user, meal_type, curr_meal_date)
                serializer = UserMealPlanSerializer(instance, data={'meal_type': meal_type}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        if meal_type and meal_date:
            curr_meal_type = instance.meal_type
            curr_meal_date = instance.meal_date
            if curr_meal_date != meal_date:
                target_meal_plan_instance = get_target_meal(request.user, meal_type, meal_date)
                if target_meal_plan_instance:
                    target_meal_completion_status = target_meal_plan_instance.isCompleted
                    if target_meal_completion_status:
                        return Response(
                            f"Unable to change meal_type to {MealTypes(meal_type).name} "
                            f"as it is already marked as complete",
                            status=status.HTTP_400_BAD_REQUEST
                        )
                handling_meal_type_existence(request.user, meal_type, curr_meal_date)
                serializer = UserMealPlanSerializer(instance, data={'meal_type': meal_type}, partial=True)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
