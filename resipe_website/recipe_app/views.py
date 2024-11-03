from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe
from .forms import RecipeForm, UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages



def recipe_list(request):
    recipes = Recipe.objects.order_by('-id')[:10]
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


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
            form.save()
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
