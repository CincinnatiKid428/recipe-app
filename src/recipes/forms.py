from django import forms
from .models import Recipe

#Form will take an ingredient from user
class IngredientSearchForm(forms.Form):
    ingredient = forms.CharField(
        max_length = 255, 
        required=False)

#Form for adding new recipes in app
class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        # Fields you want to include in the form
        fields = ['name', 'pic', 'cooking_time', 'ingredients', 'instructions', 'difficulty']

        # Optional: customize widgets for styling
        widgets = {
            'name': forms.TextInput(attrs={'class': 'recipe-form-input'}),
            'cooking_time': forms.NumberInput(attrs={'class': 'recipe-form-input'}),
            'ingredients': forms.TextInput(attrs={'class': 'recipe-form-input'}),
            'instructions': forms.Textarea(attrs={'class': 'recipe-form-textarea'}),
            'difficulty': forms.Select(attrs={'class': 'recipe-form-select'}),
        }
