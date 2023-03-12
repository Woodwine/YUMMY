from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageRecipes.as_view(), name='home'),
    path('goods/', views.AllGoods.as_view(), name='goods'),
    path('goods/<int:pk>', views.OneProduct.as_view(), name='product-details'),
    path('add_product/', views.AddProductView.as_view(), name='add_product'),
    path('done', views.DoneView.as_view(), name='product_done'),
    path('update/<int:pk>', views.UpdateProductView.as_view(), name='update_product'),
    path('update_done/', views.UpdateDoneView.as_view(), name='update_done'),
    path('delete/<int:pk>', views.DeleteProductView.as_view(), name='delete_product'),
    path('delete_done', views.DeleteDoneView.as_view(), name='delete_done'),
    path('recipes/', views.AllRecipes.as_view(), name='recipes'),
    path('recipes/<slug:slug>', views.OneRecipe.as_view(), name='recipe-details'),
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    # path('update_recipe/<int:pk>', views.RecipeUpdate.as_view(), name='update_recipe'),
    path('recipe_done/', views.add_recipe, name='recipe_done')
    # path('delete_ingredient/<int:pk>', views.delete_ingredient, name='delete_ingredient'),
]

