from dal import autocomplete
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Value, F
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic.base import View
from django.views.generic import DetailView, ListView
from .models import Recipe, Ingredient, Goods, CuisineType, DepartmentType, GoodsType, ProductQuantity
from .forms import AddProduct, AddRecipe, AddIngredient, IngredientFormSet
from django.views.generic.edit import CreateView, UpdateView, DeleteView, DeletionMixin
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.db import transaction
from django.forms import inlineformset_factory
from .utils import DataMixin, CUISINE_INFO, DEP_INFO, MENU


class HomePageView(DataMixin, TemplateView):
    # Home page
    template_name = 'yummy/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Домашняя страница')
        context['recipes'] = Recipe.objects.all()[:5]
        context['cuisines'] = {CuisineType[i]: CUISINE_INFO[i][0] for i in CuisineType._member_names_[:5]}
        context['departments'] = {DepartmentType[i]: DEP_INFO[i] for i in DepartmentType._member_names_[:5]}
        print(context)
        return dict(list(context.items()) + list(c_def.items()))


class AllRecipesView(DataMixin, ListView):
    # List of all recipes
    context_object_name = 'all_recipes'
    model = Recipe
    template_name = 'yummy/recipes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Все рецепты')
        return dict(list(context.items()) + list(c_def.items()))


class AllCuisinesView(DataMixin, TemplateView):
    # List of all recipes
    template_name = 'yummy/cuisines.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_cuisines'] = {CuisineType[i]: CUISINE_INFO[i][0] for i in CuisineType._member_names_}
        c_def = self.get_user_context(title='Все кухни')
        return dict(list(context.items()) + list(c_def.items()))


class AllDepartmentsView(DataMixin, TemplateView):
    # List of all recipes
    template_name = 'yummy/departments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_departments'] = {DepartmentType[i]: DEP_INFO[i] for i in DepartmentType._member_names_}
        c_def = self.get_user_context(title='Виды блюд')
        return dict(list(context.items()) + list(c_def.items()))


class DepartmentRecipesView(DataMixin, ListView):
    model = Recipe
    template_name = 'yummy/dep_recipes.html'

    def get_context_data(self, **kwargs):
        dep = DepartmentType[self.kwargs['dep']]
        context = super().get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.filter(department=dep)
        c_def = self.get_user_context(title=dep)
        return dict(list(context.items()) + list(c_def.items()))


class CuisineRecipesView(DataMixin, ListView):
    model = Recipe
    template_name = 'yummy/cuisine_recipes.html'

    def get_context_data(self, **kwargs):
        cus = CuisineType[self.kwargs['cntr']]
        context = super().get_context_data(**kwargs)
        context['cus_recipes'] = Recipe.objects.filter(cuisine=cus)
        context['info'] = CUISINE_INFO[cus.name][1]
        context['img'] = CUISINE_INFO[cus.name][0]
        c_def = self.get_user_context(title=cus)
        return dict(list(context.items()) + list(c_def.items()))


class AllGoodsView(DataMixin, ListView):
    # List of all goods
    model = Goods
    template_name = 'yummy/goods.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goods'] = {GoodsType[i]: Goods.objects.filter(type=GoodsType[i]) for i in GoodsType._member_names_}
        c_def = self.get_user_context(title='Продукты, используемые в рецептах')
        return dict(list(context.items()) + list(c_def.items()))


class AddGoodsView(DataMixin, SuccessMessageMixin, CreateView):
    # Add one product
    model = Goods
    form_class = AddProduct
    template_name = 'yummy/add_product.html'
    success_url = reverse_lazy('goods')
    success_message = 'Продукт успешно добавлен!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавить новый продукт')
        return dict(list(context.items()) + list(c_def.items()))


class UpdateGoodsView(DataMixin, SuccessMessageMixin, UpdateView):
    # Update one product
    model = Goods
    form_class = AddProduct
    template_name = 'yummy/update_product.html'
    success_url = reverse_lazy('goods')
    success_message = 'Продукт успешно изменен!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['object'])
        return dict(list(context.items()) + list(c_def.items()))


class DeleteGoodsView(DataMixin, DeleteView):
    template_name = 'yummy/delete_product.html'
    model = Goods
    success_url = reverse_lazy('goods')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['object'])
        return dict(list(context.items()) + list(c_def.items()))


# CRUD for recipes
# class GoodsAutocompleteView(autocomplete.Select2QuerySetView):
#
#     def get_queryset(self):
#         qs = Goods.objects.all()
#         if self.q:
#             qs = qs.filter(name__icontains=self.q)
#         return qs


class OneRecipeView(DataMixin, DetailView):
    # One recipe with details
    template_name = 'yummy/one_recipe.html'
    model = Recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        time_in_hours = context['object'].time // 60
        time_in_minutes = context['object'].time % 60
        if time_in_hours != 0:
            context['time_in_hours'] = time_in_hours
        if time_in_minutes != 0:
            context['time_in_minutes'] = time_in_minutes
        context['ingredients'] = Ingredient.objects.filter(recipe=context['object'].id)
        c_def = self.get_user_context(title=context['object'])
        return dict(list(context.items()) + list(c_def.items()))


def add_recipe(request):
    menu = MENU

    if request.method == 'POST':
        recipe_form = AddRecipe(request.POST or None, request.FILES or None)
        formset = IngredientFormSet(request.POST or None, request.FILES or None)
        with transaction.atomic():
            if recipe_form.is_valid():
                recipe = recipe_form.save(commit=False)
                time_in_hours = int(request.POST['time_in_hours']) if request.POST['time_in_hours'] != '' else 0
                time_in_minutes = int(request.POST['time_in_minutes'])
                time = time_in_hours * 60 + time_in_minutes
                if time > 0:
                    recipe.time = time
                    recipe.save()
                    if formset.is_valid():
                        for form in formset:
                            item = form.save(commit=False)
                            item.recipe = recipe
                            item.save()
                        messages.add_message(request, messages.SUCCESS, 'Рецепт успешно добавлен!')
                        return redirect('recipes')
                else:
                    messages.error(request, 'Время приготовления не может быть равно 0')
    else:
        recipe_form = AddRecipe()
        formset = IngredientFormSet()
    return render(request, 'yummy/add_recipe.html', {'recipe_form': recipe_form, 'formset': formset, 'menu': menu})


def update_recipe(request, pk):
    menu = MENU
    recipe = Recipe.objects.get(id=pk)
    time_in_hours = recipe.time // 60
    time_in_minutes = recipe.time % 60
    q_set = Ingredient.objects.filter(recipe=recipe)

    if request.method == 'POST':
        recipe_form = AddRecipe(request.POST, request.FILES, instance=recipe)
        formset = IngredientFormSet(request.POST, request.FILES, instance=recipe, queryset=q_set)
        with transaction.atomic():
            if recipe_form.is_valid():
                new_recipe = recipe_form.save(commit=False)
                time_in_hours = int(request.POST['time_in_hours']) if request.POST['time_in_hours'] != '' else 0
                time_in_minutes = int(request.POST['time_in_minutes'])
                time = time_in_hours * 60 + time_in_minutes
                if time > 0:
                    new_recipe.time = time
                    new_recipe.save()
                    if formset.is_valid():
                        formset.save()
                    messages.add_message(request, messages.SUCCESS, 'Рецепт успешно обновлен!')
                    return redirect('recipes')
                else:
                    messages.error(request, 'Время приготовления не может быть равно 0')
    else:
        recipe_form = AddRecipe(instance=recipe, initial={'time_in_hours': time_in_hours,
                                                          'time_in_minutes': time_in_minutes})
        formset = IngredientFormSet(instance=recipe, queryset=q_set)
    return render(request, 'yummy/update_recipe.html',
                  {'recipe_form': recipe_form, 'formset': formset, 'recipe_pk': pk, 'menu': menu})


class DeleteRecipeView(DeleteView):
    template_name = 'yummy/delete_recipe.html'
    model = Recipe
    success_url = '/recipes/'


class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'yummy/register.html'
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'yummy/login.html'
