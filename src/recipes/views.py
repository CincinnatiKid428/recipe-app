
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView #To display list & detail views
from django.contrib.auth.mixins import LoginRequiredMixin #To protect class-based views
from django.contrib.auth.decorators import login_required #To protect function-based views
from django.urls import reverse #For building links in DataFrame

from .models import Recipe  #Access to Recipe model
from .forms import IngredientSearchForm, RecipeForm
from .utils import recipe_queryset_to_html, get_chart
import pandas as pd
from django.db.models import Count

DEBUG_LOG = False

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

#FBV for searching recipes based on ingredient
@login_required #🔒 PROTECTED VIEW
def search_view(request):

    #Create form instance
    form = IngredientSearchForm(request.POST or None)
    recipes_df = None
    recipes_df_html = '' #Initialize DataFrames html to empty string
    
    #Graph variables
    bar_graph = ''
    pie_graph = ''
    line_graph = ''

    #Returns counts for each difficulty as list of dictionaries in
    # the format [{'difficulty':'easy' , 'count':7}, {}, {}]
    difficulty_qs = (
        Recipe.objects
        .values("difficulty")
        .annotate(count=Count("difficulty"))
    )

    line_df = pd.DataFrame(list(difficulty_qs))

    #Line chart: Shows recipe difficulties and totals
    line_graph = get_chart(
        chart_type = "line",
        data = line_df
    )

    #Get all creators and counts for recipes created by each
    creator_qs = (
        Recipe.objects
        .values("created_by__username")
        .annotate(count=Count("created_by"))
    )

    bar_df = pd.DataFrame(list(creator_qs))

    DEBUG_LOG and print(f'*** bar_df["created_by__username"] is\n',bar_df['created_by__username'])
    DEBUG_LOG and print(f'*** bar_df["count"] is\n',bar_df['count'])

    #Bar graph: Shows number of recipes created per user
    bar_graph = get_chart(
        chart_type = "bar",
        data = bar_df
    )

    #Handle form submits
    if request.method == 'POST':
        ingredient = request.POST.get('ingredient')
        #print(f'🥕 Searching for {ingredient}')

        #Empty search returns all recipes
        if ingredient == '':
            qs = Recipe.objects.all()
            recipes_df_html = recipe_queryset_to_html(qs)

        #Otherwise filter recipes to search inredient
        else:
            qs = Recipe.objects.filter(ingredients__icontains=ingredient)

            if qs.exists():
                recipes_df_html = recipe_queryset_to_html(qs)

                #Pie chart: portion of recipes containing the ingredient
                total_recipes = Recipe.objects.count()
                matching_recipes = qs.count()
                non_matching_recipes = total_recipes - matching_recipes

                #Create a DataFrame with labels/values (see utils.py)
                pie_df = pd.DataFrame({
                    'label': [f'{matching_recipes} Contain {ingredient}', f'{non_matching_recipes} Do not contain {ingredient}'],
                    'value': [matching_recipes, non_matching_recipes]
                })

                pie_graph = get_chart(
                    chart_type='pie',
                    data=pie_df,
                )

    #Create context for template
    context = {
        'form':form,
        'recipes_df_html':recipes_df_html,
        'bar_graph':bar_graph,
        'pie_graph':pie_graph,
        'line_graph':line_graph,
        'hide_search_menu':True,
    }

    #Load search template w/context data
    return render(request, 'recipes/search.html', context)


#FBV for adding new recipes for authenticated users.
@login_required #🔒 PROTECTED VIEW
def add_recipe_view(request):
    #Initializations
    error_message = None
    form = RecipeForm()

    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)  # Important: include request.FILES for image uploads
        if form.is_valid():
            recipe = form.save(commit=False)  # Don't save yet
            recipe.created_by = request.user  # Automatically assign the logged-in user
            recipe.save()
            return redirect(recipe.get_absolute_url())
        else:
            # Collect field and non-field errors
            error_message = form.errors

    context = {
        'form': form,
        'error_message': error_message,
        'hide_add_recipe_menu':True,
    }
    return render(request, 'recipes/add_recipe.html', context)