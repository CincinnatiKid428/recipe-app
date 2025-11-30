from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

#Imports for testing image file upload:
from django.core.files.uploadedfile import SimpleUploadedFile #Test upload file
from PIL import Image
from io import BytesIO

from .models import Recipe
from .forms import RecipeForm
from .views import add_recipe_view

class AddRecipeViewTests(TestCase):
    print(' ✔️ AddRecipeViewTests')

    def setUp(self):
        # Create a test user and log in
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

    def create_test_image(self):
        """Returns a real image file to use for test uploads."""
        file = BytesIO()
        image = Image.new('RGB', (50, 50), color='red')
        image.save(file, 'PNG')
        file.seek(0)
        return SimpleUploadedFile(
            name='test.png',
            content=file.getvalue(),
            content_type='image/png'
        )

    def test_add_recipe_view_get(self):
        """Test GET request to add a new recipe page."""
        response = self.client.get(reverse('recipes:add_recipe'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/add_recipe.html')


    def test_add_recipe_view_post_valid(self):
        """Test valid POST request to add a new recipe."""
        data = {
            'name': 'Pasta',
            'cooking_time': 30,
            'ingredients': 'flour,water,salt',
            'instructions': '1. Mix. 2. Boil. 3. Serve.',
            'difficulty': 'easy',  # Assuming 'easy' is a valid choice for difficulty
        }
        response = self.client.post(reverse('recipes:add_recipe'), data)

        # Ensure the recipe was created
        self.assertEqual(response.status_code, 302)  # 302 indicates a redirect
        recipe = Recipe.objects.get(name='Pasta')
        self.assertEqual(recipe.name, 'Pasta')
        self.assertEqual(recipe.cooking_time, 30)
        self.assertEqual(recipe.created_by, self.user)
        self.assertRedirects(response, recipe.get_absolute_url())  # Ensure redirect to the recipe's detail page


    def test_add_recipe_view_post_invalid(self):
        """Test invalid POST request (e.g., missing required fields)."""
        data = {
            'name': '',  # Missing name, which is required
            'cooking_time': 30,
            'ingredients': 'flour,water,salt',
            'instructions': '1. Mix. 2. Boil. 3. Serve.',
            'difficulty': 'easy',
        }

        response = self.client.post(reverse('recipes:add_recipe'), data)

        self.assertEqual(response.status_code, 200)

        # Ensure the form is re-rendered with errors from context 'form'
        form = response.context['form']
        self.assertTrue(form.errors)
        self.assertIn('name', form.errors)
        self.assertEqual(form.errors['name'], ['This field is required.'])


    def test_add_recipe_view_with_image(self):
        """Test POST request with image upload."""
        #Create a sample file
        image = self.create_test_image()

        data = {
            'name': 'Salad',
            'cooking_time': 10,
            'ingredients': 'lettuce,tomato,cucumber',
            'instructions': '1. Mix. 2. Serve.',
            'difficulty': 'easy',
            'pic': image,
        }



        response = self.client.post(reverse('recipes:add_recipe'), 
            data, 
            follow=False, #This allows checking on the 302 explicity
        )

        # Check the image upload is handled
        self.assertEqual(response.status_code, 302)  # 302 indicates redirect
        
        recipe = Recipe.objects.get(name='Salad')
        self.assertTrue(recipe.pic.name) #Ensure a file actually exists
        
        #print("☑️ Saved image name:", recipe.pic.name)

        self.assertIn('test', recipe.pic.name)
        self.assertTrue(recipe.pic.name.lower().endswith('.png'))  # Ensure file was saved


    def test_add_recipe_view_not_logged_in(self):
        """Test that an unauthenticated user is redirected to login."""
        self.client.logout()  # Log out the user
        response = self.client.get(reverse('recipes:add_recipe'))

        # Check the user is redirected to the login page
        self.assertRedirects(response, f'/login/?next={reverse("recipes:add_recipe")}')