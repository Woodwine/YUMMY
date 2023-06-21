from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse, resolve
import json

from user.models import Profile
from yummy.models import Goods, Recipe, Ingredient, Comments


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='User001',
            email='q@qqq.ru'
        )
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.recipe = Recipe.objects.create(
            name='рецепт',
            image='media/recipes/food.jpeg',
            time=15,
            description='bla-bla',
            author=self.profile,
        )
        self.goods = Goods.objects.create(
            name='Молоко',
            type='ML',
        )

    def test_home_page_GET(self):
        response = self.client.get(reverse('home'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'yummy/home.html')

    def test_all_recipes_GET(self):
        response = self.client.get(reverse('recipes'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'yummy/recipes.html')

    def test_all_cuisines_GET(self):
        response = self.client.get(reverse('cuisines'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'yummy/cuisines.html')

    def test_all_departments_GET(self):
        response = self.client.get(reverse('departments'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'yummy/departments.html')

    def test_department_recipes_GET(self):
        response = self.client.get(reverse('dep_recipes', args=['soups']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'yummy/dep_recipes.html')

    def test_cuisine_recipes_GET(self):
        response = self.client.get(reverse('cus_recipes', args=['russia']))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'yummy/cuisine_recipes.html')

    def test_all_goods_GET(self):
        response = self.client.get(reverse('goods'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'yummy/goods.html')

    def test_one_recipe_GET(self):
        response = self.client.get(reverse('recipe-details', args=[self.recipe.slug]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'yummy/one_recipe.html')

    def test_one_recipe_POST_delete_recipe(self):
        response = self.client.post(reverse('recipe-details', args=[self.recipe.slug]), {'action': 'delete'})

        self.assertEquals(response.status_code, 302)

    def test_add_goods_POST(self):
        response = self.client.post(reverse('add_product'), {
            'name': 'Морковь',
            'type': 'V'
        })

        self.assertEquals(response.status_code, 302)

    def test_update_product_POST(self):
        product = Goods.objects.create(
            name='Сметана',
            type='ML'
        )
        response = self.client.post(reverse('update_product', args=[product.pk]), {
            'name': 'Творог',
            'type': 'ML'
        })

        self.assertEquals(response.status_code, 302)

    def test_add_comment_POST(self):
        response = self.client.post(reverse('add_comment'), {
            'recipe': self.recipe,
            'comment_author': self.profile,
            'comment': 'comment',
        })

        self.assertEquals(response.status_code, 302)

    def test_add_favourite_recipe_POST(self):
        response = self.client.post(reverse('add_favourite_recipe'), {
            'recipe': self.recipe,
            'user': self.profile,
            'selected_recipe': 'Add',
        })

        self.assertEquals(response.status_code, 302)

    def test_add_recipe_POST(self):
        response = self.client.post(reverse('add_recipe'), {
            'name': 'рецепт1',
            'image': 'media/recipes/food.jpeg',
            'time': 15,
            'description': 'bla-bla',
            'author': self.profile,
        })

        self.assertEquals(response.status_code, 302)

    def test_update_recipe_POST(self):
        response = self.client.post(reverse('update_recipe', args=[self.recipe.pk]), {
            'name': 'рецепт3',
            'image': 'media/recipes/food.jpeg',
            'time': 20,
            'description': 'bla-bla',
            'author': self.profile,
        })

        self.assertEquals(response.status_code, 302)

    def test_search_GET(self):
        response = self.client.get(reverse('search_results'), {'q': 'ффф'})

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'yummy/search_results.html')