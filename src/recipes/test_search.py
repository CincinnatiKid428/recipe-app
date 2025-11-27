from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

#Import models, views, forms
from .models import Recipe
from .views import homepage, search_view
from .forms import IngredientSearchForm

# Create your tests here.

class RecipeFormTest(TestCase):

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

    #=== IngredientSearchForm Input Tests ==============================================
    
    def test_valid_form_input(self):
        form = IngredientSearchForm(data={'ingredient':'cheese'})
        assert form.is_valid()
        assert form.cleaned_data['ingredient'] == 'cheese'

    def test_empty_form_input(self):
        form = IngredientSearchForm(data={'ingredient':''})
        assert form.is_valid()
   
    def test_whitespace_form_input(self):
        form = IngredientSearchForm(data={'ingredient':'  '})
        assert form.is_valid()
        assert form.cleaned_data['ingredient'].strip() == ''

    def test_special_chars_form_input(self):
        form = IngredientSearchForm(data={'ingredient':'!@#$%'})
        assert form.is_valid()

    def test_long_form_input(self):
        form = IngredientSearchForm(data={'ingredient':'z'*255})
        assert form.is_valid()

    #=== IngredientSearchForm Input Tests ==============================================

    def test_search_view_protected(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        assert response.status_code == 302 #unauthorized
        assert 'login/' in response.url #check that url was redirected to login

    def test_authorized_user_access_to_search_view(self):
        #Django allows client.login() to simulate user auth
        self.client.login(username="Zoey", password='test456')

        url = reverse('recipes:search')
        response = self.client.get(url)

        #Assert proper status code and check content bytes for heading in search view template
        assert response.status_code == 200 #request success
        assert b"Search Recipes by Ingredient" in response.content #b'string' checks bytes vs unicode string

    def test_search_returns_results(self):
        #Login user
        self.client.login(username="Zoey", password="test456")

        #Send POST request with search form field "ingredient"
        response = self.client.post(reverse('recipes:search'),{'ingredient':'cheese'})
        assert b'Tacos' in response.content #'Tacos' formatted with title() in html output

    def test_search_returns_no_results(self):
        #Login
        self.client.login(username="Saffron", password="test123")
        
        #Send POST request with ingredient not in recipes
        response = self.client.post(reverse('recipes:search'),{'ingredient':'xyz'})
        assert b'No results' in response.content

    def test_blank_search_returns_all(self):
        #Login
        self.client.login(username="Saffron",password="test123")
        
        #POST request
        response = self.client.post(reverse('recipes:search'),{'ingredient':''})
        
        #Assert all 3 recipes are in the response.content
        assert b'Tea' in response.content
        assert b'Tacos' in response.content
        assert b'Porkchops' in response.content