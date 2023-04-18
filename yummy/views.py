from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db.models import Value
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.views.generic import DetailView, ListView
from .models import Recipe, Ingredient, Goods, CuisineType, DepartmentType
from .forms import AddProduct, AddRecipe, AddIngredient
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.db import transaction
from django.forms import inlineformset_factory


CUISINE_IMG = {
    'RU': '/static/img/cuisine/russia.png',
    'FR': '/static/img/cuisine/france.png',
    'GR': '/static/img/cuisine/georgia.png',
    'IT': '/static/img/cuisine/italia.png',
    'JP': '/static/img/cuisine/japan.png',
    'IND': '/static/img/cuisine/india.png',
    'CHN': '/static/img/cuisine/china.png',
    'AS': '/static/img/cuisine/asia.png',
    'MX': '/static/img/cuisine/mexico.png',
    'EUR': '/static/img/cuisine/euro.png',
    'KVZ': '/static/img/cuisine/caucas.png',
    'UZ': '/static/img/cuisine/uzbec.png',
    'TR': '/static/img/cuisine/turky.png',
    'AMR': '/static/img/cuisine/america.png',
    'SP': '/static/img/cuisine/spain.png',
    'GRC': '/static/img/cuisine/greek.png'
}


DEP_IMG = {
    'B': '/static/img/departments/bakery.png',
    'D': '/static/img/departments/deserts.png',
    'M': '/static/img/departments/main_dish.png',
    'S': '/static/img/departments/sandwich.png',
    'SL': '/static/img/departments/salad.png',
    'SP': '/static/img/departments/soup.png',
    'DR': '/static/img/departments/drink.png',
    'SS': '/static/img/departments/sous.png',
    'CAN': '/static/img/departments/jar.png',
}


# MENU = {
#     {'menu_title': 'Домашняя страница', 'url': '{% url "home" %}'},
#     {'menu_title': 'Рецепты', 'url': '{% url "recipes" %}', 'dropdown': {
#         {'name': 'выпечка', 'url': '#'},
#         {'name': 'десерты', 'url': '#'},
#         {'name': 'вторые блюда', 'url': '#'},
#         {'name': 'закуски', 'url': '#'},
#         {'name': 'салаты', 'url': '#'},
#         {'name': 'первые блюда', 'url': '#'},
#         {'name': 'напитки', 'url': '#'},
#         {'name': 'соусы', 'url': '#'},
#         {'name': 'заготовки на зиму', 'url': '#'},
#     }},
#     {'menu_title': 'Кухни мира', 'url': '#', 'dropdown': {
#         {'name': 'русская кухня', 'url': '#'},
#         {'name': 'французская кухня', 'url': '#'},
#         {'name': 'грузинская кухня', 'url': '#'},
#         {'name': 'итальянская кухня', 'url': '#'},
#         {'name': 'японская кухня', 'url': '#'},
#         {'name': 'индийская кухня', 'url': '#'},
#         {'name': 'китайская кухня', 'url': '#'},
#         {'name': 'азиатская кухня', 'url': '#'},
#         {'name': 'мексиканская кухня', 'url': '#'},
#         {'name': 'европейская кухня', 'url': '#'},
#         {'name': 'кавказская кухня', 'url': '#'},
#         {'name': 'узбекская кухня', 'url': '#'},
#         {'name': 'турецкая кухня', 'url': '#'},
#         {'name': 'американская кухня', 'url': '#'},
#         {'name': 'испанская кухня', 'url': '#'},
#         {'name': 'греческая кухня', 'url': '#'},
#     }},
#     {'menu_title': 'Ингредиенты', 'url': '{% url "goods" %}'},
#     {'menu_title': 'Блог', 'url': '#'},
#     {'menu_title': 'О нас', 'url': '#'},
#
# }


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
    success_url = reverse_lazy('')


class UpdateProductView(UpdateView):
    # Update one product
    model = Goods
    form_class = AddProduct
    template_name = 'yummy/update_product.html'
    success_url = reverse_lazy('goods/')


class DeleteProductView(DeleteView):
    template_name = 'yummy/delete_product.html'
    model = Goods
    success_url = reverse_lazy('goods/')


# CRUD for recipes
# class GoodsAutocompleteView(autocomplete.Select2QuerySetView):
#
#     def get_queryset(self):
#         qs = Goods.objects.all()
#         if self.q:
#             qs = qs.filter(name__icontains=self.q)
#         return qs
#


class HomePageView(ListView):
    # Home page
    template_name = 'yummy/home.html'
    model = Recipe

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.all()[:8]
        context['cuisines'] = {CuisineType.__getitem__(i): CUISINE_IMG[i] for i in CuisineType._member_names_[:3]}
        context['departments'] = {DepartmentType.__getitem__(i): DEP_IMG[i] for i in DepartmentType._member_names_[:3]}
        return context


class AllRecipes(ListView):
    # List of all recipes
    context_object_name = 'all_recipes'
    model = Recipe
    template_name = 'yummy/recipes.html'


class OneRecipe(DetailView):
    # One recipe with details
    template_name = 'yummy/one_recipe.html'
    model = Recipe

    def get_context_data(self, slug, **kwargs):
        context = super(OneRecipe, self).get_context_data(**kwargs)
        recipe = Recipe.objects.get(slug=slug)
        context['recipe'] = recipe
        context['ingredients'] = Ingredient.objects.filter(recipe=recipe.id)
        return context


def add_recipe(request):
    recipe_form = AddRecipe(request.POST or None, request.FILES or None)
    IngredientFormSet = inlineformset_factory(Recipe, Ingredient, form=AddIngredient,
                                              fields=('ingredient', 'quantity', 'quantity_type'), extra=1,
                                              validate_max=False, can_delete=True, can_delete_extra=True)

    if request.method == 'POST':
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.time = request.POST['time_in_hours'] * 60 + request.POST['time_in_minutes']
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
    recipe = recipe.annotate(time_in_hours=Value(recipe.time // 60),
                             time_in_minutes=Value(recipe.time % 60))
    q_set = Ingredient.objects.filter(recipe=recipe)
    IngredientFormSet = inlineformset_factory(Recipe, Ingredient, fields=('ingredient', 'quantity', 'quantity_type'),
                                              extra=0, validate_max=False, can_delete=True, can_delete_extra=True)

    if request.method == 'POST':
        recipe_form = AddRecipe(request.POST, request.FILES, instance=recipe)
        if recipe_form.is_valid():
            new_recipe = recipe_form.save(commit=False)
            new_recipe.time = request.POST['time_in_hours'] * 60 + request.POST['time_in_minutes']
            new_recipe.save()
            formset = IngredientFormSet(request.POST, request.FILES, instance=recipe, queryset=q_set)
            if formset.is_valid():
                formset.save()
            return render(request, 'yummy/update_recipe_done.html', context={'recipe_name': recipe.name})
    else:
        recipe_form = AddRecipe(instance=recipe)
        formset = IngredientFormSet(instance=recipe, queryset=q_set)
        return render(request, 'yummy/update_recipe.html',
                      {'recipe_form': recipe_form, 'formset': formset, 'recipe_pk': pk})


class DeleteRecipeView(DeleteView):
    template_name = 'yummy/delete_recipe.html'
    model = Recipe
    success_url = '/delete_recipe_done'


class RegisterUser(CreateView):
    form_class = UserCreationForm
    template_name = 'yummy/register.html'
    success_url = reverse_lazy('login')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'yummy/login.html'
