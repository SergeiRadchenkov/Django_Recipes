from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Category, Comment
from .forms import RecipeForm, UserRegisterForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
import random


def recipe_list(request):
    category_id = request.GET.get('category')
    random_count = request.GET.get('random')

    if random_count:  # Если выбран параметр случайных рецептов
        recipes = Recipe.objects.all()
        # Получаем 5 случайных рецептов
        recipes = random.sample(list(recipes), min(5, len(recipes)))
    elif category_id:  # Если выбрана категория
        recipes = Recipe.objects.filter(categories__id=category_id).order_by('-id')
    else:  # Если ничего не выбрано, показываем все рецепты
        recipes = Recipe.objects.all().order_by('-id')[:10]

    categories = Category.objects.all()  # Получаем все категории
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes, 'categories': categories})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    comments = recipe.comments.order_by('-created_at')
    form = CommentForm()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.recipe = recipe
            comment.author = request.user
            comment.save()
            return redirect('recipe_detail', recipe_id=recipe.id)

    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, 'comments': comments, 'form': form})


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            category = form.cleaned_data['categories']
            recipe.categories.add(category)
            return redirect('recipe_detail', recipe_id=recipe.id)
    else:
        form = RecipeForm()

    return render(request, 'recipes/add_recipe.html', {'form': form})


@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():

            updated_recipe = form.save(commit=False)  # Сохраняем, но не коммитим сразу
            updated_recipe.save()  # Сохраняем рецепт в БД

            selected_category_id = request.POST.get('categories')  # Получаем выбранную категорию
            if selected_category_id:
                # Получаем новую категорию по ID
                new_category = get_object_or_404(Category, id=selected_category_id)
                # Очищаем старые категории и добавляем новую
                recipe.categories.clear()  # Удаляем все текущие категории
                recipe.categories.add(new_category)  # Добавляем новую категорию
            return redirect('profile')
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/add_recipe.html', {'form': form})


@login_required
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)
    if request.method == 'POST':
        recipe.delete()
        return redirect('profile')

    print(f"Отображение страницы подтверждения удаления для рецепта: {recipe.title}")  # Отладочная строка
    return render(request, 'recipes/confirm_delete.html', {'recipe': recipe})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались!')
            return redirect('recipe_list')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    recipes = Recipe.objects.filter(author=user).order_by('-id')  # Получаем рецепты текущего пользователя
    return render(request, 'registration/profile.html', {'user': user, 'recipes': recipes})
