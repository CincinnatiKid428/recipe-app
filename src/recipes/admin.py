from django.contrib import admin
from .models import Recipe
from recipe_app import __version__

# Register your models here.
admin.site.register(Recipe)

# Expose version number in admin panel:
admin.site.site_header = f'Django - Simmer Administration (v{__version__})'