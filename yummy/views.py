from django.shortcuts import render
from django.views.generic.base import View
from .models import Recipe, Ingredient, Department, Cuisine


class HomePageView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'yummy/home.html')

