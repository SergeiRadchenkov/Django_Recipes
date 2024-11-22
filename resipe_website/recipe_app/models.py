from django.db import models
from django.contrib.auth.models import User


# Модель категории рецептов
class Category(models.Model):
    name = models.CharField(max_length=50)  # Поле для хранения имени категории, максимальная длина 50 символов

    def __str__(self):
        return self.name  # Строковое представление объекта категории (будет возвращать имя категории)


# Модель рецепта
class Recipe(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название блюда")  # Название рецепта
    description = models.TextField(verbose_name="Описание")  # Описание рецепта
    preparation_steps = models.TextField(verbose_name="Шаги приготовления")  # Шаги приготовления блюда
    preparation_time = models.PositiveIntegerField(verbose_name="Время приготовления в минутах")  # Время приготовления в минутах
    image = models.ImageField(upload_to='recipes/images/', verbose_name="Добавьте фото")  # Изображение рецепта
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")  # Автор рецепта (связь с пользователем)
    categories = models.ManyToManyField(Category, through='RecipeCategory', verbose_name="Категория")  # Категории, связанные с рецептом через промежуточную модель
    ingredients = models.TextField(blank=True, null=True, verbose_name="Ингредиенты")  # Ингредиенты для рецепта, можно оставить пустым

    def __str__(self):
        return self.title  # Строковое представление объекта рецепта (будет возвращать название рецепта)


# Промежуточная модель для связи рецептов и категорий
class RecipeCategory(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)  # Ссылка на рецепт
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Ссылка на категорию

    class Meta:
        unique_together = ('recipe', 'category')  # Обеспечиваем уникальность комбинации рецепт-категория


# Модель комментариев к рецептам
class Comment(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='comments', on_delete=models.CASCADE)  # Ссылка на рецепт, к которому написан комментарий
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Ссылка на автора комментария (пользователь)
    text = models.TextField()  # Текст комментария
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания комментария (устанавливается автоматически)

    class Meta:
        ordering = ['-created_at']  # Сортировка комментариев по убыванию времени создания (новые комментарии сверху)

    def __str__(self):
        return f"Комментарий от {self.user} к рецепту {self.recipe}"  # Строковое представление комментария
