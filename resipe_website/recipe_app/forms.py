from django import forms
from .models import Recipe, Category, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


# Форма для создания и редактирования рецептов
class RecipeForm(forms.ModelForm):
    # Поле для выбора категории рецепта (ModelChoiceField позволяет выбрать из существующих категорий)
    categories = forms.ModelChoiceField(
        queryset=Category.objects.all(),  # Все категории из базы данных
        empty_label="Выберите категорию",  # Текст по умолчанию в выпадающем списке
        label = "Категория"  # Подпись для поля
    )
    class Meta:
        model = Recipe  # Модель, с которой связана форма
        # Поля, которые будут отображаться в форме
        fields = ['title', 'description', 'preparation_steps', 'preparation_time', 'image', 'categories', 'ingredients']


# Форма для регистрации нового пользователя
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Электронная почта")  # Поле для ввода адреса электронной почты

    class Meta:
        model = User  # Модель, с которой связана форма
        fields = ['username', 'email', 'password1', 'password2']  # Поля формы для регистрации
        labels = {
            'username': 'Имя пользователя',  # Подпись для поля 'username'
            'password1': 'Пароль',  # Подпись для поля 'password1'
            'password2': 'Подтверждение пароля',  # Подпись для поля 'password2'
        }



# Форма для добавления комментария
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment  # Модель, с которой связана форма
        fields = ['text']  # Поле, которое будет отображаться в форме (текст комментария)
        labels = {'text': 'Ваш комментарий'}  # Подпись для поля 'text'
