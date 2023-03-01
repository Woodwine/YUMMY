from django.shortcuts import render
from django.views.generic.base import View
from django.views.generic import DetailView, ListView
from .models import Recipe, Ingredient, Goods
from .forms import AddProduct
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView


class HomePageRecipes(ListView):
    # Home page
    context_object_name = 'homepage_recipes'
    model = Recipe
    queryset = Recipe.objects.all()[:11]
    template_name = 'yummy/home.html'


class AllRecipes(ListView):
    # List of all recipes
    context_object_name = 'all_recipes'
    model = Recipe
    template_name = 'yummy/recipes.html'


class AllGoods(ListView):
    # List of all goods
    context_object_name = 'goods'
    model = Goods
    template_name = 'yummy/goods.html'


class OneRecipe(DetailView):
    # One recipe with details
    template_name = 'yummy/one_recipe.html'
    model = Recipe
    context_object_name = 'recipe'


class OneProduct(DetailView):
    # One product with details
    template_name = 'yummy/one_product.html'
    model = Goods
    context_object_name = 'product'


class AddProductView(CreateView):
    # Add one product
    model = Goods
    form_class = AddProduct
    template_name = 'yummy/add_product.html'
    success_url = '/done'


class UpdateProductView(UpdateView):
    # Update one product
    model = Goods
    form_class = AddProduct
    template_name = 'yummy/update_product.html'
    success_url = '/update_done'


class DoneView(TemplateView):
    # Success adding products
    template_name = 'yummy/done.html'


class UpdateDoneView(TemplateView):
    template_name = 'yummy/update_done.html'


class DeleteProductView(DeleteView):
    template_name = 'yummy/delete_product.html'
    model = Goods
    success_url = '/delete_done'


class DeleteDoneView(TemplateView):
    template_name = 'yummy/delete_done.html'