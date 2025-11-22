
from django.shortcuts import render
from django.views.generic import ListView, DetailView #To display list & detail views
from django.contrib.auth.mixins import LoginRequiredMixin #To protect views
from .models import Recipe  #Access to Recipe model

# Create your views here.

#View function for the recipe application homepage
def homepage(request):
    return render(request, 'recipes/home.html')

#Class for recipes list
class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/listing.html'

#Class for recipe details
#🔒 PROTECTED VIEW
class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe
    template_name = 'recipes/detail.html'