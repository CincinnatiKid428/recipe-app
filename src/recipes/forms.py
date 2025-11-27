from django import forms

#Form will take an ingredient from user
class IngredientSearchForm(forms.Form):
    ingredient = forms.CharField(
        max_length = 255, 
        required=False)