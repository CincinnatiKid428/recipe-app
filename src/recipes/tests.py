from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from .models import Recipe

# Create your tests here.


class RecipeTestClass(TestCase):

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
            name='spaghetti',
            cooking_time=12,
            ingredients='pasta,tomato sauce,water,salt',
            difficulty='hard',
            created_by=cls.user1
        )

        cls.recipe1b = Recipe.objects.create(
            name='tea',
            cooking_time=5,
            ingredients='tea leaves,water,sugar',
            difficulty='easy',
            created_by=cls.user1
        )

        cls.recipe2a = Recipe.objects.create(
            name='tacos',
            cooking_time=15,
            ingredients='taco shells,ground beef,lettuce,onion,cheese',
            difficulty='hard',
            created_by=cls.user2
        )

        cls.recipe2b = Recipe.objects.create(
            name='porkchops',
            cooking_time=10,
            ingredients='porkchops,olive oil,salt,pepper',
            difficulty='hard',
            created_by=cls.user2
        )

    #===User Creation Tests==============================================
    
    def test_user_username(self):
        test_user1 = User.objects.get(id=1)
        #Get the metadata for 'username' field
        field_label = test_user1._meta.get_field('username').verbose_name
        #Assertion
        self.assertEqual(field_label,'username')

    def test_user_password(self):
        test_user1 = User.objects.get(id=1)
        #Get the metadata for 'password' field
        field_label = test_user1._meta.get_field('password').verbose_name
        #Assertion
        self.assertEqual(field_label,'password')

      #Django should handle validation of input for username/password through its User model

    #===Recipe Creation Tests============================================
    
    def test_recipe_name(self):
        test_recipe1 = Recipe.objects.get(id=1)
        #Get the metadata for 'name' field
        field_label = test_recipe1._meta.get_field('name').verbose_name
        #Assertion
        self.assertEqual(field_label,'name')

    def test_recipe_name_length(self):
        test_recipe1 = Recipe.objects.get(id=1)
        #Get the metadata for 'name' field
        field_length = test_recipe1._meta.get_field('name').max_length
        #Assertion compare max_length of field, expect 50
        self.assertEqual(field_length,50)
    
    def test_recipe_cooking_time(self):
        test_recipe1 = Recipe.objects.get(id=1)
        #Get the metadata for 'cooking_time' field
        field_label = test_recipe1._meta.get_field('cooking_time').verbose_name
        #Assertion (Django verbose_name replaces "_" with " ")
        self.assertEqual(field_label,'cooking time') 

    def test_recipe_cooking_time_field_type(self):
        test_recipe1 = Recipe.objects.get(id=1)
        #Get metadata for 'cooking_time' field 
        field = test_recipe1._meta.get_field('cooking_time')
        #Assertion
        self.assertIsInstance(field, models.PositiveIntegerField)

    def test_recipe_ingredients(self):
        test_recipe1 = Recipe.objects.get(id=1)
        #Get the metadata for 'ingredients' field
        field_label = test_recipe1._meta.get_field('ingredients').verbose_name
        #Assertion
        self.assertEqual(field_label,'ingredients')

    def test_recipe_ingredients_length(self):
        test_recipe1 = Recipe.objects.get(id=1)
        #Get the metadata for 'ingredients' field
        field_length = test_recipe1._meta.get_field('ingredients').max_length
        #Assertion
        self.assertEqual(field_length,255)

    def test_recipe_difficulty(self):
        test_recipe1 = Recipe.objects.get(id=1)
        #Get the metadata for 'difficulty' field
        field_label = test_recipe1._meta.get_field('difficulty').verbose_name
        #Assertion
        self.assertEqual(field_label,'difficulty')

    def test_recipe_difficulty_length(self):
        test_recipe1 = Recipe.objects.get(id=1)
        #Get the metadata for 'difficulty' field
        field_length = test_recipe1._meta.get_field('difficulty').max_length
        #Assertion
        self.assertEqual(field_length,12)

    def test_recipe_last_update(self):
        test_recipe1 = Recipe.objects.get(id=1)
        #Get the metadata for 'last_update' field
        field_label = test_recipe1._meta.get_field('last_update').verbose_name
        #Assertion (Django verbose_name replaces "_" with " ")
        self.assertEqual(field_label,'last update') 

    def test_recipe_created_by(self):
        test_recipe1 = Recipe.objects.get(id=1)
        #Get metadata for 'created_by' field 
        field_label = test_recipe1._meta.get_field('created_by').verbose_name
        #Assertion (Django verbose_name replaces "_" with " ")
        self.assertEqual(field_label,'created by')

    def test_recipe_created_by_field_type(self):
        test_recipe1 = Recipe.objects.get(id=1)
        #Get metadata for 'created_by' field 
        field = test_recipe1._meta.get_field('created_by')
        #Assertion
        self.assertIsInstance(field, models.ForeignKey)