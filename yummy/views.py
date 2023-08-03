from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, Avg
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from .models import Recipe, Ingredient, Goods, Comments, CUISINE_TYPE, DEPARTMENT_TYPE, GOODS_TYPE
from .forms import AddProduct, AddRecipe, IngredientFormSet, AddComment
from django.views.generic.edit import CreateView, UpdateView, DeletionMixin
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.db import transaction
from .utils import CUISINE_INFO, DEP_INFO, MENU


class HomePageView(TemplateView):
    """
    Represents a home page
    """
    template_name = 'yummy/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = MENU
        context['title'] = 'Домашняя страница'
        context['recipes'] = Recipe.objects.all()[:5]
        context['cuisines'] = [(i[0], i[1], CUISINE_INFO[i[0]][0]) for i in CUISINE_TYPE[:5]]
        context['departments'] = [(i[0], i[1], DEP_INFO[i[0]]) for i in DEPARTMENT_TYPE[:5]]
        return context


class AllRecipesView(ListView):
    """
    Represents a list of all recipes.
    """
    context_object_name = 'all_recipes'
    model = Recipe
    template_name = 'yummy/recipes.html'
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['const_rating'] = (1, 2, 3, 4, 5)
        context['title'] = 'Все рецепты'
        context['menu'] = MENU
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        full_qs = [{'recipe': i, 'rating': i.comments_set.aggregate(Avg('rating'))['rating__avg']} for i in qs]
        return full_qs


class AllCuisinesView(TemplateView):
    """
    Represents a list of all cuisine types.
    """

    template_name = 'yummy/cuisines.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_cuisines'] = [(i[0], i[1], CUISINE_INFO[i[0]][0]) for i in CUISINE_TYPE]
        context['title'] = 'Кухни мира'
        context['menu'] = MENU
        return context


class AllDepartmentsView(TemplateView):
    """
    Represents a list of all types of dishes.
    """
    template_name = 'yummy/departments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_departments'] = [(i[0], i[1], DEP_INFO[i[0]]) for i in DEPARTMENT_TYPE]
        context['title'] = 'Виды блюд'
        context['menu'] = MENU
        return context


class DepartmentRecipesView(ListView):
    """
    Represents a list of all recipes for each dish type.
    """

    model = Recipe
    template_name = 'yummy/dep_recipes.html'
    paginate_by = 12
    context_object_name = 'recipes'

    def get_context_data(self, **kwargs):
        dep = [value for key, value in DEPARTMENT_TYPE if key == self.kwargs['dep']][0]
        context = super().get_context_data(**kwargs)
        context['const_rating'] = (1, 2, 3, 4, 5)
        context['title'] = dep
        context['menu'] = MENU
        return context

    def get_queryset(self):
        recipes = super().get_queryset()
        dep = self.kwargs['dep']
        qs = recipes.filter(department=dep)
        full_qs = [{'recipe': i, 'rating': i.comments_set.aggregate(Avg('rating'))['rating__avg']} for i in qs]
        return full_qs


class CuisineRecipesView(ListView):
    """
    Represents a list of all recipes for each cuisine type.
    """
    model = Recipe
    template_name = 'yummy/cuisine_recipes.html'
    paginate_by = 12
    context_object_name = 'cus_recipes'

    def get_context_data(self, **kwargs):
        cus = self.kwargs['cntr']
        context = super().get_context_data(**kwargs)
        context['info'] = CUISINE_INFO[cus][1]
        context['img'] = CUISINE_INFO[cus][0]
        context['const_rating'] = (1, 2, 3, 4, 5)
        context['title'] = [value for key, value in CUISINE_TYPE if key == cus][0]
        context['menu'] = MENU
        return context

    def get_queryset(self):
        recipes = super().get_queryset()
        cus = self.kwargs['cntr']
        qs = recipes.filter(cuisine=cus)
        full_qs = [{'recipe': i, 'rating': i.comments_set.aggregate(Avg('rating'))['rating__avg']} for i in qs]
        return full_qs


class AllGoodsView(ListView):
    """
    Represents a list of all products used for cooking.
    """
    model = Goods
    template_name = 'yummy/goods.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['goods'] = {i: Goods.objects.filter(type=i[0]) for i in GOODS_TYPE}
        context['title'] = 'Продукты, используемые в рецептах'
        context['menu'] = MENU
        return context


class AddGoodsView(SuccessMessageMixin, CreateView):
    """
    Creates a new product. Can only be used by staff.
    """
    model = Goods
    form_class = AddProduct
    template_name = 'yummy/add_product.html'
    success_url = reverse_lazy('goods')
    success_message = 'Продукт успешно добавлен!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавить новый продукт'
        context['menu'] = MENU
        return context


class UpdateGoodsView(DeletionMixin, SuccessMessageMixin, UpdateView):
    """
    Updates an existing product. Can only be used by staff.
    """
    model = Goods
    form_class = AddProduct
    template_name = 'yummy/update_product.html'
    success_url = reverse_lazy('goods')
    success_message = 'Продукт успешно изменен!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['object']
        context['menu'] = MENU
        return context


class OneRecipeView(DeletionMixin, SuccessMessageMixin, DetailView):
    """
    Represents an existing recipe. Be used also for deleting the recipe by its creator or by staff.
    """

    template_name = 'yummy/one_recipe.html'
    model = Recipe
    success_url = reverse_lazy('profile')
    success_message = 'Продукт успешно удален!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        time_in_hours = self.object.time // 60
        time_in_minutes = self.object.time % 60

        if time_in_hours != 0:
            context['time_in_hours'] = time_in_hours

        if time_in_minutes != 0:
            context['time_in_minutes'] = time_in_minutes

        context['ingredients'] = Ingredient.objects.filter(recipe=self.object.id)
        comments = Comments.objects.filter(recipe=self.object.id)

        if self.request.user.is_authenticated and comments.filter(
                comment_author=self.request.user.profile).count() == 0:
            context['comment_form'] = AddComment

        context['comments'] = comments
        context['recipe_rating'] = comments.aggregate(Avg('rating'))['rating__avg']
        context['const_rating'] = (1, 2, 3, 4, 5)
        context['title'] = self.object
        context['menu'] = MENU
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == 'delete':
            recipe = self.get_object()
            recipe.delete()
            messages.add_message(request, messages.SUCCESS, 'Рецепт успешно  удален!')
            return redirect('profile')
        else:
            return HttpResponseNotFound()


@login_required
def add_comment(request):
    """
    Add a new comment and rating for recipe
    """
    comment_form = AddComment(request.POST)
    rating = request.POST.get('selected_rating', 0)
    recipe = get_object_or_404(Recipe, name=request.POST.get('recipe'))
    path = request.META.get('HTTP_REFERER', '/')

    if request.method == 'POST':
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.rating = rating if rating != '' else 0
            comment.recipe = recipe
            comment.comment_author = request.user.profile
            comment.save()
            comments = Comments.objects.filter(recipe=recipe)
            return redirect(path, {'comments': comments})
        else:
            comments = Comments.objects.filter(recipe=recipe)
            comment_form = AddComment()
            return redirect(path, {'comments': comments, 'comment_form': comment_form})


@login_required
def add_favourite_recipe(request):
    """
    Adds the recipe to the list of user favorite recipes
    """

    path = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, name=request.POST.get('recipe'))
        user = request.user.profile
        action = request.POST.get('selected_recipe')
        if action == 'Add':
            recipe.liked_by.add(user)
        elif action == 'Remove':
            recipe.liked_by.remove(user)
        return redirect(path)


def add_recipe(request):
    """
    Creates a new recipe and recipe ingredients. Adds these ingredients to the recipe.
    """
    if request.user.is_authenticated:
        if request.method == 'POST':
            recipe_form = AddRecipe(request.POST or None, request.FILES or None)
            formset = IngredientFormSet(request.POST or None, request.FILES or None)
            return_path = request.GET.get('next') if request.GET.get('next') else ''
            with transaction.atomic():
                if recipe_form.is_valid() and formset.is_valid():
                    recipe = recipe_form.save(commit=False)
                    forms = formset.save(commit=False)
                    recipe.author = request.user.profile
                    recipe.time = recipe_form.cleaned_data['time']
                    recipe.save()
                    for obj in formset.deleted_objects:
                        obj.delete()
                    for form in forms:
                        form.recipe = recipe
                        form.save()
                    messages.add_message(request, messages.SUCCESS, 'Рецепт успешно добавлен!')
                    return redirect(return_path) if return_path != '' else redirect('home')
        else:
            recipe_form = AddRecipe()
            formset = IngredientFormSet()
        return render(request, 'yummy/add_recipe.html', {'recipe_form': recipe_form, 'formset': formset, 'menu': MENU})
    else:
        return redirect('login')


def update_or_delete_recipe(request, pk):
    """
    Updates or deletes the recipe. Be used by creator of the recipe or by staff.
    """

    if request.user.is_authenticated:
        return_path = request.GET.get('next') if request.GET.get('next') else ''
        recipe = get_object_or_404(Recipe, id=pk)
        time_in_hours = recipe.time // 60
        time_in_minutes = recipe.time % 60
        q_set = Ingredient.objects.filter(recipe=recipe)
        recipe_form = AddRecipe(request.POST, request.FILES, instance=recipe)
        formset = IngredientFormSet(request.POST, request.FILES, instance=recipe, queryset=q_set)
        if request.method == 'POST':
            if request.POST.get('action') == 'delete':
                recipe.delete()
                messages.add_message(request, messages.SUCCESS, 'Рецепт успешно  удален!')
                return redirect('profile')
            else:
                with transaction.atomic():
                    if recipe_form.is_valid() and formset.is_valid():
                        new_recipe = recipe_form.save(commit=False)
                        forms = formset.save(commit=False)
                        new_recipe.time = recipe_form.cleaned_data['time']
                        new_recipe.save()
                        for obj in formset.deleted_objects:
                            obj.delete()
                        for form in forms:
                            if not form.recipe:
                                form.recipe = new_recipe
                            form.save()
                        messages.add_message(request, messages.SUCCESS, 'Рецепт успешно обновлен!')
                        return redirect(return_path) if return_path != '' else redirect('home')
        else:
            recipe_form = AddRecipe(instance=recipe, initial={'time_in_hours': time_in_hours,
                                                              'time_in_minutes': time_in_minutes})
            formset = IngredientFormSet(instance=recipe, queryset=q_set)
        return render(request, 'yummy/update_recipe.html',
                      {'recipe_form': recipe_form, 'formset': formset, 'recipe_pk': pk, 'menu': MENU})
    else:
        return redirect('login')


class SearchView(ListView):
    """
    Searches recipes using keywords.
    """
    model = Recipe
    template_name = 'yummy/search_results.html'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            cus = [i[1] for i in CUISINE_TYPE if
                   query.lower() in i[1].lower()]
            dep = [i[1] for i in DEPARTMENT_TYPE if
                   query.lower() in i[1].lower()]
            object_list = Recipe.objects.filter(
                Q(name__icontains=query) | Q(cuisine__in=cus) | Q(department__in=dep))
            return object_list
        else:
            return Recipe.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = f"q={self.request.GET.get('q')}&"
        context['title'] = 'Результат поиска'
        context['menu'] = MENU
        return context
