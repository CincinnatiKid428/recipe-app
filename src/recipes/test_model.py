from django.test import TestCase
from django.db import models
from django.contrib.auth.models import User
from .models import Recipe

# Create your tests here.


class RecipeTestClass(TestCase):
    print(' ✔️ RecipeTestClass')

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='Zoey', password='tuna')
        cls.recipe = Recipe.objects.create(
            name="Soup",
            cooking_time=10,
            ingredients="Salt,Pepper",
            instructions="Boil.",
            created_by=cls.user
        )

    #===User Creation Tests==============================================
    
    def test_user_username(self):
        #Get the metadata for 'username' field
        field_label = self.user._meta.get_field('username').verbose_name
        #Assertion
        self.assertEqual(field_label,'username')

    def test_user_password(self):
        #Get the metadata for 'password' field
        field_label = self.user._meta.get_field('password').verbose_name
        #Assertion
        self.assertEqual(field_label,'password')

      #Django should handle validation of input for username/password through its User model

    #===Recipe Creation Tests============================================
    
    def test_recipe_name(self):
        #Get the metadata for 'name' field
        field_label = self.recipe._meta.get_field('name').verbose_name
        #Assertion
        self.assertEqual(field_label,'name')

    def test_recipe_name_length(self):
        #Get the metadata for 'name' field
        field_length = self.recipe._meta.get_field('name').max_length
        #Assertion compare max_length of field, expect 50
        self.assertEqual(field_length,50)
    
    def test_recipe_pic(self):
        #Get the metadata for 'pic' field
        field_label = self.recipe._meta.get_field('pic').verbose_name
        #Assertion
        self.assertEqual(field_label,'pic')

    def test_recipe_pic_field_type(self):
        #Get metadata for 'pic' field 
        field = self.recipe._meta.get_field('pic')
        #Assertion
        self.assertIsInstance(field, models.ImageField)

    def test_recipe_cooking_time(self):
        #Get the metadata for 'cooking_time' field
        field_label = self.recipe._meta.get_field('cooking_time').verbose_name
        #Assertion (Django verbose_name replaces "_" with " ")
        self.assertEqual(field_label,'cooking time') 

    def test_recipe_cooking_time_field_type(self):
        #Get metadata for 'cooking_time' field 
        field = self.recipe._meta.get_field('cooking_time')
        #Assertion
        self.assertIsInstance(field, models.PositiveIntegerField)

    def test_recipe_ingredients(self):
        #Get the metadata for 'ingredients' field
        field_label = self.recipe._meta.get_field('ingredients').verbose_name
        #Assertion
        self.assertEqual(field_label,'ingredients')

    def test_recipe_ingredients_length(self):
        #Get the metadata for 'ingredients' field
        field_length = self.recipe._meta.get_field('ingredients').max_length
        #Assertion
        self.assertEqual(field_length,255)

    def test_recipe_difficulty(self):
        #Get the metadata for 'difficulty' field
        field_label = self.recipe._meta.get_field('difficulty').verbose_name
        #Assertion
        self.assertEqual(field_label,'difficulty')

    def test_recipe_difficulty_length(self):
        #Get the metadata for 'difficulty' field
        field_length = self.recipe._meta.get_field('difficulty').max_length
        #Assertion
        self.assertEqual(field_length,12)

    def test_recipe_instructions(self):
        #Get the metadata for 'instructions' field
        field_label = self.recipe._meta.get_field('instructions').verbose_name
        #Assertion
        self.assertEqual(field_label,'instructions')

    def test_recipe_instructions_field_type(self):
        #Get metadata for 'instructions' field 
        field = self.recipe._meta.get_field('instructions')
        #Assertion
        self.assertIsInstance(field, models.TextField)

    def test_recipe_last_update(self):
        #Get the metadata for 'last_update' field
        field_label = self.recipe._meta.get_field('last_update').verbose_name
        #Assertion (Django verbose_name replaces "_" with " ")
        self.assertEqual(field_label,'last update') 

    def test_recipe_created_by(self):
        #Get metadata for 'created_by' field 
        field_label = self.recipe._meta.get_field('created_by').verbose_name
        #Assertion (Django verbose_name replaces "_" with " ")
        self.assertEqual(field_label,'created by')

    def test_recipe_created_by_field_type(self):
        #Get metadata for 'created_by' field 
        field = self.recipe._meta.get_field('created_by')
        #Assertion
        self.assertIsInstance(field, models.ForeignKey)

    #===Recipe Functions Tests============================================

    def test_get_absolute_url(self):
        self.assertEqual(self.recipe.get_absolute_url(), '/list/1')

    def test_get_ingredients_as_list(self):
        compare_list = sorted(['Salt','Pepper'])
        self.assertEqual(self.recipe.get_ingredients_as_list(), compare_list)