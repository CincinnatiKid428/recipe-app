from django.db import models
from django.contrib.auth.models import User

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
    cooking_time = models.PositiveIntegerField()
    ingredients = models.CharField(max_length=255)
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
