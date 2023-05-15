
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('change_password/', views.UserPasswordChangeView.as_view(), name='change_password'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit, name='edit_profile'),
]
