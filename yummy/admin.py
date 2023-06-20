from django.contrib import admin
from enumchoicefield.admin import EnumListFilter

from .models import Ingredient, Recipe, Goods, Comments


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'date', 'cuisine', 'department']
    search_fields = ['name', 'author__user__username']
    list_filter = [('cuisine', EnumListFilter), ('department', EnumListFilter)]


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['name', 'type']
    search_fields = ['name']
    list_filter = ['name', ('type', EnumListFilter)]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['ingredient', 'quantity', 'quantity_type', 'recipe']
    search_fields = ['ingredient__name']


@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['comment_author', 'rating', 'recipe', 'date']
    search_fields = ['comment_author__user__username', 'recipe__name']
