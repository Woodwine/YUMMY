from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import DetailView, ListView
from .models import Recipe, Ingredient, Goods
from .forms import AddProduct, AddRecipe
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.db import transaction
from django.forms import inlineformset_factory
from dal import autocomplete


# CRUD for Goods
class AllGoods(ListView):
    # List of all goods
    context_object_name = 'goods'
    model = Goods
    template_name = 'yummy/goods.html'


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


class DoneView(TemplateView):
    # Success adding products
    template_name = 'yummy/done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Goods.objects.order_by('id').last()
        context['product_name'] = product.name
        context['product_type'] = product.type
        return context


class UpdateProductView(UpdateView):
    # Update one product
    model = Goods
    form_class = AddProduct
    template_name = 'yummy/update_product.html'
    success_url = '/update_done'


class UpdateDoneView(TemplateView):
    template_name = 'yummy/update_done.html'


class DeleteProductView(DeleteView):
    template_name = 'yummy/delete_product.html'
    model = Goods
    success_url = '/delete_done'


class DeleteDoneView(TemplateView):
    template_name = 'yummy/delete_done.html'


# CRUD for recipes

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


class OneRecipe(DetailView):
    # One recipe with details
    template_name = 'yummy/one_recipe.html'
    model = Recipe

    def get_context_data(self, **kwargs):
        context = super(OneRecipe, self).get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.filter(recipe=self.object)
        return context


def add_recipe(request):
    recipe_form = AddRecipe(request.POST or None, request.FILES or None)
    IngredientFormSet = inlineformset_factory(Recipe, Ingredient, fields=('ingredient', 'quantity', 'quantity_type'),
                                              extra=1, validate_max=False, can_delete=True, can_delete_extra=True)

    if request.method == 'POST':
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.save()
            formset = IngredientFormSet(request.POST or None, request.FILES or None)

            if formset.is_valid():
                for form in formset:
                    item = form.save(commit=False)
                    item.recipe = recipe
                    item.save()

            return render(request, 'yummy/recipe_done.html', context={'recipe_name': recipe.name})

    else:
        recipe_form = AddRecipe()
        formset = IngredientFormSet()
        return render(request, 'yummy/add_recipe.html', {'recipe_form': recipe_form, 'formset': formset})


def update_recipe(request, pk):
    recipe = Recipe.objects.get(id=pk)
    q_set = Ingredient.objects.filter(recipe=recipe)
    num = len(q_set)
    IngredientFormSet = inlineformset_factory(Recipe, Ingredient, fields=('ingredient', 'quantity', 'quantity_type'),
                                              extra=0, validate_max=False, can_delete=True, can_delete_extra=True)

    if request.method == 'POST':
        recipe_form = AddRecipe(request.POST, request.FILES, instance=recipe)
        if recipe_form.is_valid():
            new_recip = recipe_form.save(commit=False)
            new_recip.save()
            formset = IngredientFormSet(request.POST, request.FILES, instance=recipe, queryset=q_set)
            if formset.is_valid():
                formset.save()
            return render(request, 'yummy/update_recipe_done.html', context={'recipe_name': recipe.name})
    else:
        recipe_form = AddRecipe(instance=recipe)
        formset = IngredientFormSet(instance=recipe, queryset=q_set)
        return render(request, 'yummy/update_recipe.html', {'recipe_form': recipe_form, 'formset': formset, 'recipe_pk': pk})


class RecipeUpdateDoneView(TemplateView):
    template_name = 'yummy/update_recipe_done.html'


class DeleteRecipeView(DeleteView):
    template_name = 'yummy/delete_recipe.html'
    model = Recipe
    success_url = '/delete_recipe_done'


class DeleteRecipeDoneView(TemplateView):
    template_name = 'yummy/delete_recipe_done.html'




