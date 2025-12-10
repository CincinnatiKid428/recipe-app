from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from .storage_backends import MediaStorage  # import MediaStorage
import re


DEBUG_LOG = True

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

#Formats recipe titles that may contain ['s] (i.e. Zoey's Casserole)
def smart_title(text):
    # Title-case words
    text = re.sub(r"\b(\w)", lambda m: m.group(1).upper(), text.lower())
    # Correct apostrophe-s (don’t capitalize the s)
    text = re.sub(r"'s\b", "'s", text, flags=re.IGNORECASE)
    return text

# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=50)
    pic = models.ImageField(
        upload_to='recipes', 
        storage=MediaStorage(),   # force Azure storage
        blank=True, 
        null=True
        #default='no_picture.jpg' image handled in templates
    ) 
    cooking_time = models.PositiveIntegerField()
    ingredients = models.CharField(max_length=255)
    instructions = models.TextField(default='1. ')
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
        ingredient_list = sorted(self.ingredients.split(','))
        return ingredient_list

    #Custom defined save() to correct path to Azure blob 'media/recipes/<filename>'
    def save(self, *args, **kwargs):

        #Normalize name field
        if self.name:
            DEBUG_LOG and print(f'>>>>>> starting name is {self.name}')
            #strip whitespace, title case, correct 'S (i.e. Grandma'S Apple Cake) ⚠️ This does not correct 'S issue
            #cleaned = self.name.strip().title().replace("'S","'s") 
 
            cleaned = smart_title(self.name.strip())
            DEBUG_LOG and print(f'>>>>>> cleaned name is {cleaned}')
            self.name = cleaned
    
        #Normalize ingredients field
        if self.ingredients:
            cleaned = [i.strip().title() for i in self.ingredients.split(',') if i.strip()]
            self.ingredients = ",".join(cleaned)

        DEBUG_LOG and print("💾 Saving Recipe:", self.name)

        super().save(*args, **kwargs)
