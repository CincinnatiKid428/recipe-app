from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

#Import models, views, forms
from .models import Recipe
from .views import homepage, search_view, RecipeListView, RecipeDetailView
from .forms import IngredientSearchForm

# Create your tests here.

class RecipeFormTest(TestCase):
    print(' ✔️ RecipeFormTest')

    @classmethod
    def setUpTestData(cls):

        #Create test users
        cls.user1 = User.objects.create_user(
            username='Saffron',
            password='test123'
        )

        cls.user2 = User.objects.create_user(
            username='Zoey',
            password='test456'
        )

        #Create recipes under the users

        cls.recipe1a = Recipe.objects.create(
            name='tea',
            pic='recipes/tea.jpg',
            cooking_time=5,
            ingredients='tea leaves,water,sugar',
            difficulty='easy',
            instructions='tea instructions',
            created_by=cls.user1
        )

        cls.recipe2a = Recipe.objects.create(
            name='tacos',
            pic='recipes/tacos.jpg',
            cooking_time=15,
            ingredients='taco shells,ground beef,lettuce,onion,cheese',
            difficulty='hard',
            instructions='tacos instructions',
            created_by=cls.user2
        )

        cls.recipe2b = Recipe.objects.create(
            name='porkchops',
            pic='recipes/porkchops.jpg',
            cooking_time=10,
            ingredients='porkchops,olive oil,salt,pepper',
            difficulty='hard',
            instructions='porkchops instructions',
            created_by=cls.user2
        )

    #=== RecipeDetailView Tests ==============================================

    def test_detail_view_protected(self):
        url = reverse('recipes:detail', kwargs={'pk':1})
        response = self.client.get(url)
        assert response.status_code == 302 #unauthorized
        assert 'login/' in response.url #check that url was redirected to login

    def test_authorized_user_access_to_detail_view(self):
        #Django allows client.login() to simulate user auth
        self.client.login(username="Zoey", password='test456')

        url = reverse('recipes:detail', kwargs={'pk':1})
        response = self.client.get(url)

        #Assert proper status code and check content bytes for heading in search view template
        assert response.status_code == 200 #request success
        assert b"Instructions" in response.content #b'string' checks bytes vs unicode string