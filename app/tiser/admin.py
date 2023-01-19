from django.contrib import admin

from .models import Category, Tiser


@admin.register(Tiser)
class TiserAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ("title", "desc", "author", "status")

    # Фильтрация в списке
    list_filter = ("category", "status")

    # Поиск по полям
    search_fields = ("title", "description", "author")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Отображение полей в списке
    list_display = ("title", )

    # Поиск по полям
    search_fields = ("title", )
