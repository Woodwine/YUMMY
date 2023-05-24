from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q, Avg
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from .models import Recipe, Ingredient, Goods, CuisineType, DepartmentType, GoodsType, Comments
from .forms import AddProduct, AddRecipe, IngredientFormSet, AddComment
from django.views.generic.edit import CreateView, UpdateView, DeletionMixin
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.db import transaction
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
        return dict(list(context.items()) + list(c_def.items()))


class AllRecipesView(DataMixin, ListView):
    # List of all recipes
    context_object_name = 'all_recipes'
    model = Recipe
    template_name = 'yummy/recipes.html'
    paginate_by = 12

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
        c_def = self.get_user_context(title='Кухни мира')
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
    paginate_by = 12
    context_object_name = 'recipes'

    def get_context_data(self, **kwargs):
        dep = DepartmentType[self.kwargs['dep']]
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=dep)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        recipes = super().get_queryset()
        dep = DepartmentType[self.kwargs['dep']]
        return recipes.filter(department=dep)


class CuisineRecipesView(DataMixin, ListView):
    model = Recipe
    template_name = 'yummy/cuisine_recipes.html'
    paginate_by = 12
    context_object_name = 'cus_recipes'

    def get_context_data(self, **kwargs):
        cus = CuisineType[self.kwargs['cntr']]
        context = super().get_context_data(**kwargs)
        context['info'] = CUISINE_INFO[cus.name][1]
        context['img'] = CUISINE_INFO[cus.name][0]
        c_def = self.get_user_context(title=cus)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        cus_recipes = super().get_queryset()
        cus = CuisineType[self.kwargs['cntr']]
        return cus_recipes.filter(cuisine=cus)


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


class UpdateGoodsView(DataMixin, DeletionMixin, SuccessMessageMixin, UpdateView):
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


class OneRecipeView(DataMixin, DeletionMixin, SuccessMessageMixin, DetailView):
    # One recipe with details
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
        if self.request.user.is_authenticated and comments.filter(comment_author=self.request.user.profile).count() == 0:
            context['comment_form'] = AddComment

        context['comments'] = comments
        context['recipe_rating'] = comments.aggregate(Avg('rating'))['rating__avg']
        context['const_rating'] = (1, 2, 3, 4, 5)
        c_def = self.get_user_context(title=self.object)
        return dict(list(context.items()) + list(c_def.items()))

    def post(self, request, *args, **kwargs):
        comment_form = AddComment(request.POST)
        path = request.META.get('HTTP_REFERER', '/')

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.rating = request.POST.get('selected_rating', 0)
            comment.recipe = self.get_object()
            comment.comment_author = request.user.profile
            comment.save()
            self.object = self.get_object()
            context = super(OneRecipeView, self).get_context_data(**kwargs)
            context['comments'] = Comments.objects.filter(recipe=self.object.id)
            return redirect(path, context=context)
        else:
            self.object = self.get_object()
            context = super(OneRecipeView, self).get_context_data(**kwargs)
            context['comments'] = Comments.objects.filter(recipe=self.object.id)
            return self.render_to_response(context=context)


@login_required
def add_favourite_recipe(request):
    path = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        recipe = Recipe.objects.get(name=request.POST.get('recipe'))
        user = request.user.profile
        action = request.POST.get('selected_recipe')
        if action == 'Add':
            recipe.liked_by.add(user)
        elif action == 'Remove':
            recipe.liked_by.remove(user)
        return redirect(path)


def add_recipe(request):
    return_path = request.GET.get('next') if request.GET.get('next') else ''

    if request.user.is_authenticated:
        if request.method == 'POST':
            recipe_form = AddRecipe(request.POST or None, request.FILES or None)
            formset = IngredientFormSet(request.POST or None, request.FILES or None)
            with transaction.atomic():
                if recipe_form.is_valid() and formset.is_valid():
                    recipe = recipe_form.save(commit=False)
                    recipe.author = request.user.profile
                    time_in_hours = int(request.POST['time_in_hours']) if request.POST['time_in_hours'] != '' else 0
                    time_in_minutes = int(request.POST['time_in_minutes']) if request.POST[
                                                                                  'time_in_minutes'] != '' else 0
                    time = time_in_hours * 60 + time_in_minutes
                    if time > 0:
                        recipe.time = time
                        recipe.save()
                        for form in formset:
                            if form.is_valid():
                                item = form.save(commit=False)
                                item.recipe = recipe
                                item.save()
                        messages.add_message(request, messages.SUCCESS, 'Рецепт успешно добавлен!')
                        return redirect(return_path) if return_path != '' else redirect('home')
                    else:
                        messages.add_message(request, messages.ERROR, 'Время приготовления не может быть равно 0')
                        return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            recipe_form = AddRecipe()
            formset = IngredientFormSet()
        return render(request, 'yummy/add_recipe.html', {'recipe_form': recipe_form, 'formset': formset, 'menu': MENU})
    else:
        return redirect('login')


def update_recipe(request, pk):
    menu = MENU
    return_path = request.GET.get('next') if request.GET.get('next') else ''
    recipe = Recipe.objects.get(id=pk)
    time_in_hours = recipe.time // 60
    time_in_minutes = recipe.time % 60
    q_set = Ingredient.objects.filter(recipe=recipe)

    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.POST.get('action') == 'delete':
                recipe.delete()
                messages.add_message(request, messages.SUCCESS, 'Рецепт успешно  удален!')
                return redirect('profile')
            else:
                recipe_form = AddRecipe(request.POST, request.FILES, instance=recipe)
                formset = IngredientFormSet(request.POST, request.FILES, instance=recipe, queryset=q_set)
                with transaction.atomic():
                    if recipe_form.is_valid() and formset.is_valid():
                        new_recipe = recipe_form.save(commit=False)
                        time_in_hours = int(request.POST['time_in_hours']) if request.POST[
                                                                                  'time_in_hours'] != '' else 0
                        time_in_minutes = int(request.POST['time_in_minutes']) if request.POST[
                                                                                      'time_in_minutes'] != '' else 0
                        time = time_in_hours * 60 + time_in_minutes
                        if time > 0:
                            new_recipe.time = time
                            new_recipe.save()
                            formset.save()
                            messages.add_message(request, messages.SUCCESS, 'Рецепт успешно обновлен!')
                            return redirect(return_path) if return_path != '' else redirect('home')
                        else:
                            messages.add_message(request, messages.ERROR,
                                                 'Время приготовления не может быть равно 0')
                            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            recipe_form = AddRecipe(instance=recipe, initial={'time_in_hours': time_in_hours,
                                                              'time_in_minutes': time_in_minutes})
            formset = IngredientFormSet(instance=recipe, queryset=q_set)
        return render(request, 'yummy/update_recipe.html',
                      {'recipe_form': recipe_form, 'formset': formset, 'recipe_pk': pk, 'menu': menu})
    else:
        return redirect('login')


class SearchView(DataMixin, ListView):
    model = Recipe
    template_name = 'yummy/search_results.html'
    paginate_by = 12

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            cus = [CuisineType[i] for i in CuisineType._member_names_ if query.lower() in CuisineType[i].verbose_name.lower()]
            dep = [DepartmentType[i] for i in DepartmentType._member_names_ if query.lower() in DepartmentType[i].verbose_name.lower()]
            object_list = Recipe.objects.filter(
                Q(name__icontains=query) | Q(cuisine__in=cus) | Q(department__in=dep))
            return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = f"q={self.request.GET.get('q')}&"
        c_def = self.get_user_context(title='Результат поиска')
        return dict(list(context.items()) + list(c_def.items()))
