from django.test import SimpleTestCase
from django.urls import reverse, resolve
from yummy.views import HomePageView, AllRecipesView, AllCuisinesView, AllDepartmentsView, DepartmentRecipesView, \
    CuisineRecipesView, AllGoodsView, AddGoodsView, UpdateGoodsView, OneRecipeView, add_comment, add_favourite_recipe, \
    add_recipe, update_or_delete_recipe, SearchView


class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func.view_class, HomePageView)

    def test_recipes_list_url_is_resolved(self):
        url = reverse('recipes')
        self.assertEquals(resolve(url).func.view_class, AllRecipesView)

    def test_cuisines_url_is_resolved(self):
        url = reverse('cuisines')
        self.assertEquals(resolve(url).func.view_class, AllCuisinesView)

    def test_departments_url_is_resolved(self):
        url = reverse('departments')
        self.assertEquals(resolve(url).func.view_class, AllDepartmentsView)

    def test_dep_recipes_list_url_is_resolved(self):
        url = reverse('dep_recipes', args=[1])
        self.assertEquals(resolve(url).func.view_class, DepartmentRecipesView)

    def test_cus_recipes_list_url_is_resolved(self):
        url = reverse('cus_recipes', args=[1])
        self.assertEquals(resolve(url).func.view_class, CuisineRecipesView)

    def test_goods_list_url_is_resolved(self):
        url = reverse('goods')
        self.assertEquals(resolve(url).func.view_class, AllGoodsView)

    def test_add_goods_url_is_resolved(self):
        url = reverse('add_product')
        self.assertEquals(resolve(url).func.view_class, AddGoodsView)

    def test_update_goods_url_is_resolved(self):
        url = reverse('update_product', args=[1])
        self.assertEquals(resolve(url).func.view_class, UpdateGoodsView)

    def test_add_recipe_url_is_resolved(self):
        url = reverse('add_recipe')
        self.assertEquals(resolve(url).func, add_recipe)

    def test_one_recipe_url_is_resolved(self):
        url = reverse('recipe-details', args=['first-slug'])
        self.assertEquals(resolve(url).func.view_class, OneRecipeView)

    def test_update_recipe_url_is_resolved(self):
        url = reverse('update_recipe', args=[1])
        self.assertEquals(resolve(url).func, update_or_delete_recipe)

    def test_favourite_recipe_url_is_resolved(self):
        url = reverse('add_favourite_recipe')
        self.assertEquals(resolve(url).func, add_favourite_recipe)

    def test_add_comment_url_is_resolved(self):
        url = reverse('add_comment')
        self.assertEquals(resolve(url).func, add_comment)

    def test_searching_url_is_resolved(self):
        url = reverse('search_results')
        self.assertEquals(resolve(url).func.view_class, SearchView)