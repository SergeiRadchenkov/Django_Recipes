from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название блюда")
    description = models.TextField(verbose_name="Описание")
    preparation_steps = models.TextField(verbose_name="Шаги приготовления")
    preparation_time = models.PositiveIntegerField(verbose_name="Время приготовления в минутах")
    image = models.ImageField(upload_to='recipes/images/', verbose_name="Добавьте фото")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    categories = models.ManyToManyField(Category, through='RecipeCategory', verbose_name="Категория")
    ingredients = models.TextField(blank=True, null=True, verbose_name="Ингредиенты")

    def __str__(self):
        return self.title

class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('recipe', 'category')
