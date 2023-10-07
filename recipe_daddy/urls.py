from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.user_views.UserList.as_view(), name='user_view'),
    path('user/<str:username>/', views.user_views.UserDetails.as_view(), name='user_view'),
]