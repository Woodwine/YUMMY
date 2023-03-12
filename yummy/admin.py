from django.contrib import admin, messages
from .models import Ingredient, Recipe, Goods

# Register your models here.


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'date']
    ordering = ['date']
    search_fields = ['name']
    list_filter = ['cuisine', 'department']


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    ordering = ['name']
    search_fields = ['name', 'type']
    list_filter = ['name', 'type']


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['ingredient', 'quantity', 'quantity_type', 'recipe']
    ordering = ['ingredient']
    search_fields = ['ingredient']
