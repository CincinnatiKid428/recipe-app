from django.shortcuts import render

# Create your views here.

#View function for the recipe application homepage
def homepage(request):
    return render(request, 'recipes/recipes_home.html')