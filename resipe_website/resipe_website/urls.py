"""
URL configuration for resipe_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Путь для страницы входа в систему (используется стандартное представление Django)
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    # Путь для страницы выхода из системы (используется стандартное представление Django)
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Включение URL-ресурсов приложения 'recipe_app' для аутентификации
    path('accounts/', include('recipe_app.urls')),
    # Включение URL-ресурсов приложения 'recipe_app' для остальных страниц сайта
    path('', include('recipe_app.urls')),
    # Путь для доступа к админ-панели Django
    path('admin/', admin.site.urls),
]

# Включаем обработку статических файлов (например, изображений) в режиме DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
