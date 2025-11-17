from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse

difficulty_choices = (
  #(actual_db_value,human_readable_label)
  ('easy','Easy'),
  ('intermediate','Intermediate'),
  ('hard','Hard')
)

#Function suggestion by ChatGPT for issue of preserving recipes should a user be deleted.
#Gets User row with username 'Deleted User' if exists, else creates it and stores in 'user'.
#Boolen 'created' True if record found, False if record created.
def getDeletedUser():
    user, created = User.objects.get_or_create(
        username='Deleted User', 
        defaults={'password': '','is_active':False}) #setting inactive prevents 'Deleted User' from login
    return user

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=50)
    pic = models.ImageField(upload_to='recipes', blank=True, null=True) #Default 'no_picture.jpg' image handled in templates
    cooking_time = models.PositiveIntegerField()
    ingredients = models.CharField(max_length=255)
    instructions = models.TextField(default='- None entered')
    difficulty = models.CharField(max_length=12, choices=difficulty_choices, default='intermediate')
    last_update = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET(getDeletedUser),
        null=True, #allows for temporary setting field to Null during reassignment
        blank=True #allows for temporary setting field to Null during reassignment
        )

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('recipes:detail', kwargs={'pk': self.pk})

    def get_ingredients_as_list(self):
        ingredient_list = self.ingredients.split(',')
        return ingredient_list