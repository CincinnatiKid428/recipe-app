from django.urls import path
from .views import homepage

app_name = 'recipes'

urlpatterns = [
  path('', homepage)
]