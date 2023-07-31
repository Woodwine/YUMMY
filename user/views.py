from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.models import Avg
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages

from yummy.models import Recipe
from .forms import RegisterUserForm, LoginUserForm, UserPasswordChangeForm, UserEditForm, ProfileEditForm
from .models import Profile
from yummy.utils import MENU


class RegisterUser(CreateView):
    """
    Registers a new user in the system
    """

    form_class = RegisterUserForm
    template_name = 'user/register_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        context['menu'] = MENU
        return context

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    """
    Logs the user in the system
    """

    form_class = LoginUserForm
    template_name = 'user/login_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        context['menu'] = MENU
        return context

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Добро пожаловать!')
        return reverse_lazy('home')


def logout_user(request):
    """
    Logs the user out the system
    """

    logout(request)
    return redirect('home')


class UserPasswordChangeView(PasswordChangeView):
    """
    Changes the user password
    """

    form_class = UserPasswordChangeForm
    template_name = 'user/change_password.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение пароля'
        context['menu'] = MENU
        return context

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, 'Ваш пароль успешно изменен!')
        return reverse_lazy('home')


@login_required
def profile(request):
    """
    Represents a user profile with user favorites recipes, own recipes and profile information
    """

    recipes = Recipe.objects.filter(author=request.user.profile)
    my_recipes = [{'recipe': i, 'rating': i.comments_set.aggregate(Avg('rating'))['rating__avg']} for i in recipes]
    favourites = Recipe.objects.filter(liked_by=request.user.profile)
    my_favourites = [{'recipe': i, 'rating': i.comments_set.aggregate(Avg('rating'))['rating__avg']} for i in favourites]
    return render(request, 'user/profile.html', {'menu': MENU, 'my_recipes': my_recipes,
                                                 'my_favourites': my_favourites, 'const_rating': (1, 2, 3, 4, 5)})


@login_required
def edit(request):
    """
    Edits user information and profile information
    """
    menu = MENU

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.add_message(request, messages.SUCCESS, 'Данные успешно изменены!')
            return redirect('profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'user/edit.html', {'user_form': user_form, 'profile_form': profile_form, 'menu': menu})
