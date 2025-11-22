from django.urls import path
from .views import homepage, RecipeListView, RecipeDetailView

app_name = 'recipes'

urlpatterns = [
  path('', homepage, name='home'),                              #Home
  path('list/', RecipeListView.as_view(), name='list'),         #RecipeListView
  path('list/<pk>', RecipeDetailView.as_view(), name='detail')  #RecipeDetailView
]