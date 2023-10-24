import os
import requests
from dotenv import load_dotenv
from urllib.parse import quote

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


def generate_meal_image(meal_name):
    load_dotenv()
    EDAMAM_APPLICATION_ID = os.getenv("EDAMAM_APPLICATION_ID")
    EDAMAM_APPLICATION_KEY = os.getenv("EDAMAM_APPLICATION_KEY")
    print(EDAMAM_APPLICATION_ID, EDAMAM_APPLICATION_KEY)
    BASE_URL = "https://api.edamam.com/api/recipes/v2"
    query_params = {
        "type": "public",
        "q": meal_name,
        "app_id": EDAMAM_APPLICATION_ID,
        "app_key": f"{quote(EDAMAM_APPLICATION_KEY)}",
        "mealType": "Breakfast",
        "imageSize": "REGULAR",
        "random": "true",
    }
    headers = {
            "Content-Type": "application/json"
        }
    try:
        response = requests.get(BASE_URL, headers=headers, params=query_params)
        if not response.status_code == 200:
            raise Exception("Unsuccessful request to edamam.")
        data = response.json()
        if "hits" in data and data["hits"]:
            first_hit = data["hits"][0]
            image_url = first_hit["recipe"]["image"]
            return image_url, response.status_code
        else:
            return None, response.status_code
        
    except Exception as _:
        return None, 404