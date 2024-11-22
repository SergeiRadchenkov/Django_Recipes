from django.urls import path
from .views import recipe_list, recipe_detail, add_recipe, profile, edit_recipe, delete_recipe
from . import views

# Список URL-маршрутов для приложения
urlpatterns = [
    path('', recipe_list, name='recipe_list'),  # Главная страница: список всех рецептов, вызывается view 'recipe_list'
    path('recipe/<int:recipe_id>/', recipe_detail, name='recipe_detail'),  # Страница отдельного рецепта, в URL передается ID рецепта
    path('recipe/add/', add_recipe, name='add_recipe'),  # Страница для добавления нового рецепта
    path('register/', views.register, name='register'),  # Страница регистрации нового пользователя
    path('accounts/profile/', profile, name='profile'),  # Страница профиля пользователя (связана с аккаунтом пользователя)
    path('recipe/<int:pk>/edit/', edit_recipe, name='edit_recipe'),  # Страница редактирования рецепта, где pk — это первичный ключ рецепта
    path('recipe/<int:pk>/delete/', delete_recipe, name='delete_recipe'),  # Страница удаления рецепта, где pk — это первичный ключ рецепта
]
