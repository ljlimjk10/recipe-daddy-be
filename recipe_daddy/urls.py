from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('user', views.user_views.UserViewSet.as_view(), name='user_view'),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('get-ai-prompt', views.ai_prompt.get_ai_prompt, name='test_view'),

    path('user-meal-plan', views.user_meal_plan_views.UserMealPlanViewSet.as_view(), name='user_meal_plan_view'),

    path('leaderboard', views.leaderboard_views.LeaderboardViewSet.as_view(), name='leaderboard_view'),
]