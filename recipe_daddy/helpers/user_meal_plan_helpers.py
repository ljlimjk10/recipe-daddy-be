from recipe_daddy.models.user_meal_plan_models import UserMealPlan

def handling_meal_type_existence(user, meal_type, meal_date):
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


def get_target_meal(user, meal_type, meal_date):
    """
    retrieve user meal plan, if any, given user, meal_type and, meal_date
    """

    target_meal_plan = UserMealPlan.objects.filter(
        user=user,
        meal_type=meal_type,
        meal_date=meal_date
    ).first()

    return target_meal_plan if target_meal_plan else None