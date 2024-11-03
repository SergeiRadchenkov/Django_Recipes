from django.urls import path
from .views import recipe_list, recipe_detail, add_recipe, profile, edit_recipe, delete_recipe
from . import views

urlpatterns = [
    path('', recipe_list, name='recipe_list'),
    path('recipe/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
    path('recipe/add/', add_recipe, name='add_recipe'),
    path('register/', views.register, name='register'),
    path('accounts/profile/', profile, name='profile'),
    path('recipe/<int:pk>/edit/', edit_recipe, name='edit_recipe'),
    path('recipe/<int:pk>/delete/', delete_recipe, name='delete_recipe'),
]
