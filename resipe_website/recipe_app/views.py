from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe, Category, Comment
from .forms import RecipeForm, UserRegisterForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
import random


# Представление для отображения списка рецептов
def recipe_list(request):
    category_id = request.GET.get('category')  # Получаем параметр 'category' из GET-запроса
    random_count = request.GET.get('random')  # Получаем параметр 'random' для отображения случайных рецептов

    if random_count:  # Если выбран параметр случайных рецептов
        recipes = Recipe.objects.all()  # Получаем все рецепты
        # Получаем 5 случайных рецептов
        recipes = random.sample(list(recipes), min(5, len(recipes)))
    elif category_id:  # Если выбрана категория
        recipes = Recipe.objects.filter(categories__id=category_id).order_by('-id')  # Фильтруем рецепты по выбранной категории
    else:  # Если ничего не выбрано, показываем все рецепты
        recipes = Recipe.objects.all().order_by('-id')[:10]  # Получаем первые 10 рецептов

    categories = Category.objects.all()  # Получаем все категории
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes, 'categories': categories})


# Представление для отображения деталей рецепта
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)  # Получаем рецепт по ID или 404, если не найден
    comments = recipe.comments.order_by('-created_at')  # Получаем все комментарии к рецепту и сортируем по дате
    form = CommentForm()  # Создаем форму для нового комментария

    if request.method == "POST":  # Если был отправлен POST-запрос (добавление комментария)
        form = CommentForm(request.POST)  # Заполняем форму данными из POST-запроса
        if form.is_valid():  # Если форма валидна
            comment = form.save(commit=False)  # Сохраняем комментарий без немедленного сохранения в БД
            comment.recipe = recipe  # Привязываем комментарий к рецепту
            comment.author = request.user  # Устанавливаем автора комментария как текущего пользователя
            comment.save()  # Сохраняем комментарий в БД
            return redirect('recipe_detail', recipe_id=recipe.id)  # Перенаправляем на страницу с деталями рецепта

    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe, 'comments': comments, 'form': form}) # Отображаем рецепт с комментариями


# Представление для добавления нового рецепта
@login_required  # Требуется авторизация
def add_recipe(request):
    if request.method == 'POST':  # Если был отправлен POST-запрос (добавление рецепта)
        form = RecipeForm(request.POST, request.FILES)  # Заполняем форму данными из POST-запроса и файлов
        if form.is_valid():  # Если форма валидна
            recipe = form.save(commit=False)  # Сохраняем рецепт без немедленного сохранения в БД
            recipe.author = request.user  # Устанавливаем автора рецепта как текущего пользователя
            recipe.save()  # Сохраняем рецепт в БД
            category = form.cleaned_data['categories']  # Получаем выбранную категорию
            recipe.categories.add(category)  # Добавляем категорию к рецепту
            return redirect('recipe_detail', recipe_id=recipe.id)  # Перенаправляем на страницу с деталями нового рецепта
    else:  # Если метод запроса GET, создаем пустую форму
        form = RecipeForm()

    return render(request, 'recipes/add_recipe.html', {'form': form})  # Отображаем форму добавления рецепта


# Представление для редактирования рецепта
@login_required  # Требуется авторизация
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)  # Получаем рецепт по pk и проверяем, что он принадлежит текущему пользователю
    if request.method == 'POST':  # Если был отправлен POST-запрос (редактирование рецепта)
        form = RecipeForm(request.POST, request.FILES, instance=recipe)  # Заполняем форму данными из POST-запроса и файлами
        if form.is_valid():  # Если форма валидна
            updated_recipe = form.save(commit=False)  # Сохраняем, но не коммитим сразу
            updated_recipe.save()  # Сохраняем рецепт в БД

            selected_category_id = request.POST.get('categories')  # Получаем выбранную категорию
            if selected_category_id:  # Если категория была выбрана
                # Получаем новую категорию по ID
                new_category = get_object_or_404(Category, id=selected_category_id)
                # Очищаем старые категории и добавляем новую
                recipe.categories.clear()  # Удаляем все текущие категории
                recipe.categories.add(new_category)  # Добавляем новую категорию
            return redirect('profile')  # Перенаправляем на профиль пользователя
    else:  # Если метод запроса GET, создаем форму с данными существующего рецепта
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/add_recipe.html', {'form': form})  # Отображаем форму редактирования рецепта


# Представление для удаления рецепта
@login_required  # Требуется авторизация
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk, author=request.user)  # Получаем рецепт по pk и проверяем, что он принадлежит текущему пользователю
    if request.method == 'POST':  # Если был отправлен POST-запрос (подтверждение удаления)
        recipe.delete()  # Удаляем рецепт из БД
        return redirect('profile')  # Перенаправляем на профиль пользователя

    # Отображаем страницу подтверждения удаления для рецепта
    print(f"Отображение страницы подтверждения удаления для рецепта: {recipe.title}")
    return render(request, 'recipes/confirm_delete.html', {'recipe': recipe})


# Представление для регистрации пользователя
def register(request):
    if request.method == 'POST':  # Если был отправлен POST-запрос (регистрация)
        form = UserRegisterForm(request.POST)  # Заполняем форму данными из POST-запроса
        if form.is_valid():  # Если форма валидна
            user = form.save()  # Сохраняем нового пользователя
            login(request, user)  # Входим в систему с новым пользователем
            messages.success(request, 'Вы успешно зарегистрировались!')  # Отображаем сообщение об успешной регистрации
            return redirect('recipe_list')  # Перенаправляем на главную страницу
    else:  # Если метод запроса GET, создаем пустую форму
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})  # Отображаем форму регистрации


# Представление для профиля пользователя
@login_required  # Требуется авторизация
def profile(request):
    user = request.user  # Получаем текущего пользователя
    recipes = Recipe.objects.filter(author=user).order_by('-id')  # Получаем рецепты текущего пользователя
    return render(request, 'registration/profile.html', {'user': user, 'recipes': recipes}) # Отображаем профиль пользователя с его рецептами
