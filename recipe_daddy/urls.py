from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

urlpatterns = [
    path('user/', views.user_views.UserList.as_view(), name='user_view'),
    path('user/<str:username>/', views.user_views.UserDetails.as_view(), name='user_view'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('test', views.test_views.test, name='test_view'),

    path('user-meal-plan', views.user_meal_plan_views.UserMealPlanViewSet.as_view(), name='user_meal_plan_view'),
]