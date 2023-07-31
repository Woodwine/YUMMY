from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User

from .models import Profile


class ProfileImageInput(forms.ClearableFileInput):
    clear_checkbox_label = 'Удалить'
    input_text = 'Загрузить новый файл'
    template_name = "form_widgets/profile_image_input.html"


class RegisterUserForm(UserCreationForm):
    """
    Registers a new user in the system
    """

    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    email = forms.CharField(label='Адрес электронной почты:', widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'exampleInputPassword1'
    }))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'exampleInputPassword2',
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    """
    Logs the user in the system
    """

    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'id': 'exampleInputPassword1'
    }))


class UserPasswordChangeForm(PasswordChangeForm):
    """
    Changes the user password
    """

    old_password = forms.CharField(label='Старый пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))
    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))
    new_password2 = forms.CharField(label='Подтверждение нового пароля', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))


class UserEditForm(forms.ModelForm):
    """
    Updates user profile information
    """

    email = forms.CharField(label='Адрес электронной почты:', widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = User
        fields = ['email']


class ProfileEditForm(forms.ModelForm):
    """
    Updates user personal information in the profile
    """

    date_of_birth = forms.DateField(required=False, label='Дата рождения', widget=forms.DateInput(attrs={
        'class': 'form-control',
    }))
    photo = forms.ImageField(label='', widget=ProfileImageInput(attrs={
                'class': 'form-control',
                'type': "file",
                'id': 'formFile',
                'placeholder': 'Выберите файл'
            }))

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')
