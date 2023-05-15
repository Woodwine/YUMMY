from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView
from django.contrib import messages
from django.views.generic.edit import DeletionMixin

from yummy.models import Recipe
from .forms import RegisterUserForm, LoginUserForm, UserPasswordChangeForm, UserEditForm, ProfileEditForm
from .models import Profile
from yummy.utils import DataMixin, MENU


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'user/register_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        Profile.objects.create(user=user)
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'user/login_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('home')


class UserPasswordChangeView(DataMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'user/change_password.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Изменение пароля')
        return dict(list(context.items()) + list(c_def.items()))


@login_required
def profile(request):
    my_recipes = Recipe.objects.filter(author=request.user.profile)
    # my_favourites =
    return render(request, 'user/profile.html', {'menu': MENU, 'my_recipes': my_recipes})


@login_required
def edit(request):
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
            messages.add_message(request, messages.ERROR, 'Форма заполнена не корректно')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'user/edit.html', {'user_form': user_form, 'profile_form': profile_form, 'menu': menu})
