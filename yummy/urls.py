from django.template.defaulttags import url
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('recipes/', views.AllRecipesView.as_view(), name='recipes'),
    path('cuisines/', views.AllCuisinesView.as_view(), name='cuisines'),
    path('departments/', views.AllDepartmentsView.as_view(), name='departments'),
    path('departments/<str:dep>', views.DepartmentRecipesView.as_view(), name='dep_recipes'),
    path('cuisines/<str:cntr>', views.CuisineRecipesView.as_view(), name='cus_recipes'),
    path('goods/', views.AllGoodsView.as_view(), name='goods'),
    path('goods/add', views.AddGoodsView.as_view(), name='add_product'),
    path('goods/update/<int:pk>', views.UpdateGoodsView.as_view(), name='update_product'),
    path('recipes/add', views.add_recipe, name='add_recipe'),
    path('recipes/<slug:slug>', views.OneRecipeView.as_view(), name='recipe-details'),
    path('update_recipe/<int:pk>', views.update_recipe, name='update_recipe'),
    path('add_favourite_recipe/', views.add_favourite_recipe, name='add_favourite_recipe'),
    path('search/', views.SearchView.as_view(), name='search_results'),
]