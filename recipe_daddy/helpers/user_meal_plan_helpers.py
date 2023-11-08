import os
import requests
import re
import re
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
    
def format_ingredients_to_gram(have_ingredients):

    def input_unit_conversion(input_string):
        unit_conversion = {
            "ml": 1,    
            "l": 1000,  
            "kg": 1000, 
            "qty": 75 
        }
        input_string = input_string.lower()    
        match = re.match(r"(\d+)([a-zA-Z]+)", input_string)

        if match:
            quantity = float(match.group(1))
            unit = match.group(2)

            if unit in unit_conversion:
                grams = quantity * unit_conversion[unit]
                return grams
            else:
                return 75 * quantity
        else:
            parts = input_string.split()
            if len(parts) > 0:
                quantity = float(parts[0])
                return 75 * quantity
            else:
                return 0
        
    h_ingre = {}
    n_ingre = {}
    for ingredient, qty in have_ingredients.items():
        h_ingre[ingredient] = input_unit_conversion(qty)

    # if "no_ingredients" in jsonObject: # check if key is present
    #     # check if null
    #     if jsonObject["no_ingredients"] is None:
    #         n_ingre = None            
    #     else:
    #         for ingredient, qty in jsonObject["have_ingredients"].items():
    #             n_ingre[ingredient] = input_unit_conversion(qty)

    # format back object with have_ingredients and no_ingredients to json Object
    have_ingredients = h_ingre 
    # jsonObject["no_ingredients"] = n_ingre        
    return have_ingredients
