from django.contrib import admin, messages
from .models import Cuisine, Ingredient, Recipe, Department

# Register your models here.


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'author']
    ordering = ['date']
    search_fields = ['name', 'author']
    list_filter = ['cuisine', 'department']


@admin.register(Cuisine)
class CuisineAdmin(admin.ModelAdmin):
    ordering = ['cuisine_name']
    search_fields = ['cuisine_name']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    ordering = ['department_name']
    search_fields = ['department_name']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    ordering = ['ingredient']
    search_fields = ['ingredient']
