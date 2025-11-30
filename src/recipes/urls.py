from django.urls import path
from .views import homepage, aboutpage, RecipeListView, RecipeDetailView, search_view, add_recipe_view

app_name = 'recipes'

urlpatterns = [
  path('', homepage, name='home'),
  path('about/', aboutpage, name='about'),                              #Home
  path('list/', RecipeListView.as_view(), name='list'),         #RecipeListView
  path('list/<pk>', RecipeDetailView.as_view(), name='detail'), #RecipeDetailView
  path('search/', search_view, name='search'),                #Search View
  path('add/', add_recipe_view, name='add_recipe')
]