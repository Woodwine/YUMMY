from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import DetailView, ListView
from .models import Recipe, Ingredient, Goods
from .forms import AddProduct, AddRecipe, IngredientFormSet
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.db import transaction


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
    if request.method == 'POST':
        if recipe_form.is_valid():
            recipe_form.save()
            recipe = Recipe.objects.last()
            formset = IngredientFormSet(request.POST or None, request.FILES or None)
            print('>>>>', formset.get_form_error())

            print(formset.data)
            print(formset.non_form_errors())

            if formset.is_valid():
                print('>>>> ФОРМСЕТ ВАЛИДЕН!')
                instances = formset.save(commit=False)

                for instance in instances:
                    instance.recipe = recipe
                    instance.save()

            return render(request, 'yummy/recipe_done.html', context={'recipe_name': recipe.name})

    else:
        recipe_form = AddRecipe()
        formset = IngredientFormSet()
        return render(request, 'yummy/add_recipe.html', {'recipe_form': recipe_form, 'formset': formset})


# class AddRecipeView(CreateView):
#     model = Recipe
#     form_class = AddRecipe
#
#     def get_context_data(self, **kwargs):
#         data = super(AddRecipeView, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['ingredients'] = IngredientFormSet(self.request.POST)
#             # data['ingredients_2'] = IngredientFormSet_2(self.request.POST)
#         else:
#             data['ingredients'] = IngredientFormSet()
#         return data
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         ingredients = context['ingredients']
#         with transaction.atomic():
#             self.object = form.save()
#
#             if ingredients.is_valid():
#                 ingredients.instance = self.object
#                 ingredients.save()




# class AddRecipeView(CreateView):
#     model = Recipe
#     form_class = AddRecipe
#     template_name = 'yummy/add_recipe.html'
#     success_url = '/recipe_done'
#
#
# class RecipeDoneView(TemplateView):
#     template_name = 'yummy/recipe_done.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         recipe = Recipe.objects.order_by('id').last()
#         context['recipe_name'] = recipe.name
#         return context
#

# def delete_ingredient(request, pk):
#     try:
#         ingredient = Ingredient.objects.get(id=pk)
#     except Ingredient.DoesNotExist:
#         messages.success(request, 'Object Does not exit')
#         return redirect('update_recipe', slug=ingredient.recipe.slug)
#
#     ingredient.delete()
#     messages.success(request, 'Ингредиент успешно удален')
#
