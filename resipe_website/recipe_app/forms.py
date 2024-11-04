from django import forms
from .models import Recipe, Category, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RecipeForm(forms.ModelForm):
    categories = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Выберите категорию",
        label = "Категория"
    )
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'preparation_steps', 'preparation_time', 'image', 'categories', 'ingredients']


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Электронная почта")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Имя пользователя',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': 'Ваш комментарий'}
