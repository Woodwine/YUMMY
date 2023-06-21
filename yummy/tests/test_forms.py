from django.contrib.auth.models import User
from django.test import TestCase

from user.models import Profile
from yummy.forms import AddProduct, AddIngredient, AddRecipe, AddComment
from yummy.models import Goods, Recipe


class TestForms(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            username='User001',
            email='q@qqq.ru'
        )
        self.profile = Profile.objects.create(
            user=self.user
        )
        self.product = Goods.objects.create(
            name='Творог',
            type='ML'
        )
        self.recipe = Recipe.objects.create(
            name='рецепт',
            image='media/recipes/food.jpeg',
            time=15,
            description='bla-bla',
            author=self.profile,
        )

    def test_product_form_valid_data(self):
        form = AddProduct(data={
            'name': 'Сметана',
            'type': 'ML'
        })

        self.assertTrue(form.is_valid())

    def test_product_form_no_data(self):
        form = AddProduct(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_ingredient_form_valid_data(self):
        form = AddIngredient(data={
            'ingredient': self.product,
            'quantity': 100,
            'quantity_type': 'GR'
        })

        self.assertTrue(form.is_valid())

    def test_ingredient_form_no_data(self):
        form = AddIngredient(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_recipe_form_no_data(self):
        form = AddRecipe(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 7)

    def test_comment_form_valid_data(self):
        form = AddComment(data={
            'recipe': self.recipe,
            'rating': 4,
            'comment_author': self.profile,
            'comment': 'bla-bla',
        })

        self.assertTrue(form.is_valid())

    def test_comment_form_no_data(self):
        form = AddComment(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 1)
