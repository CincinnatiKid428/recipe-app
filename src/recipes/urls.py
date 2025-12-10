from django.urls import path
from .views import homepage, aboutpage, RecipeListView, RecipeDetailView, EditRecipeView, DeleteRecipeView, search_view, add_recipe_view

app_name = 'recipes'

urlpatterns = [
  path('', homepage, name='home'),                              #Home
  path('about/', aboutpage, name='about'),                      #About
  path('list/', RecipeListView.as_view(), name='list'),         #Recipe List
  path('list/<pk>', RecipeDetailView.as_view(), name='detail'), #Recipe Detail
  path('search/', search_view, name='search'),                  #Search Recipe
  path('add/', add_recipe_view, name='add_recipe'),             #Add Recipe
  path('edit/<pk>', EditRecipeView.as_view(), name='edit'),     #Edit Recipe
  path('delete/<pk>', DeleteRecipeView.as_view(), name='delete'),#Delete Recipe
]