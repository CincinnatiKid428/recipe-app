from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, JsonResponse

#Model/View imports
from django.contrib.auth import get_user_model
from recipes.models import Recipe, UserProfile
from django.views.generic import UpdateView, DeleteView, DetailView

#Protected view imports:
from django.contrib.auth.mixins import LoginRequiredMixin   #To protect class-based views
from django.contrib.auth.decorators import login_required   #To protect function-based views

#Authentication imports:
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CustomUserCreationForm

#Used for subqueries to determine favorite status in UserProfileView
from django.db.models import Count, Exists, OuterRef

User = get_user_model()

DEBUG_LOG = False

#Presents Register template and handles user registration.
def register_view(request):
    form = CustomUserCreationForm()
    field_errors = {}      # Dictionary to hold field-level errors
    non_field_errors = []  # List for form-level errors

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()       # creates the new user
            login(request, user)     # optional: automatically log them in
            DEBUG_LOG and print(f'✅ Registration complete for [{user}]')
            return redirect('recipes:list')
        else:
            # Capture field-level errors (ChatGPT assistance used in error extraction)
            for field, errors in form.errors.items():
                if field != '__all__':  # '__all__' holds non-field errors
                    field_errors[field] = errors
                else:
                    non_field_errors.extend(errors)

            DEBUG_LOG and print('⚠️ Field Errors:', field_errors)
            DEBUG_LOG and print('⚠️ Non-field Errors:', non_field_errors)

    context = {
        'form': form,
        'field_errors': field_errors,
        'non_field_errors': non_field_errors,
    }

    return render(request, 'auth/register.html', context)


#Presents Login template and handles login form submit.
def login_view(request):
    #Initializations
    error_message = None
    form = AuthenticationForm()

    #Capture ?next=... from GET or POST
    next_url = request.GET.get('next') or request.POST.get('next')

    if request.method == 'POST':
        #Read the form data via POST request
        form = AuthenticationForm(data=request.POST)

        #Check if form is valid & get fields
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            #Django authentication:
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user) #Django function
                DEBUG_LOG and print(f'✅ Login complete for [{user}]')

                if next_url:
                    return redirect(next_url)
                return redirect('recipes:list')

        #If we reach here, form was invalid OR user was invalid
        non_field_errors = form.non_field_errors()
        if non_field_errors:
            error_message = non_field_errors[0]
        
        else: #else missing credentials
            error_message = "Please enter both username and password."

    #Prep data to send from view to template
    context = {
      'form':form,
      'error_message':error_message
    }

    #Debug printing error if one was found
    DEBUG_LOG and print(' ⚠️ Authentication Error:',error_message)

    #Load login page with this context
    return render(request, 'auth/login.html', context)


#Logout FBV
def logout_view(request):
    logout(request)
    return render(request, 'auth/logout.html')


#Function view for deleting a user.
#🔒 PROTECTED VIEW
@login_required
def delete_user(request):
    #If POST then delete the user
    if request.method == "POST":
        user = request.user
        DEBUG_LOG and print(f' ⚠️ Deleting user [{user}]')
        logout(request)                 # End session first
        user.delete()                   # Triggers SET(getDeletedUser)
        DEBUG_LOG and print(f' ✅ Deleted [{user}] successfully!')
        return redirect("recipes:home") # Go to login after delete

    #Show template for confirmation for non-POST request
    return render(request, "auth/confirm_delete_user.html")


#Class-based view for user's profile containg DetailView of their recipes.
#🔒 PROTECTED VIEW
class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "auth/profile.html"
    context_object_name = "profile_user"
    slug_field = "username"
    slug_url_kwarg = "username"

    #Helps protect against inactive user / "Deleted User" profile
    def get_object(self):
        user = super().get_object()
        if not user.is_active:
            raise Http404("User not found")
        return user

    def get_context_data(self, **kwargs):
        #Preserve Django context data
        context = super().get_context_data(**kwargs)

        #Add "recipes" list to context data 
        context["recipes"] = Recipe.objects.filter(
            created_by=self.object
        ).order_by("-last_update")

        #Check if authenticated user is owner of profile
        context["is_owner"] = self.request.user == self.object
        
        #Add UserProfile data to context for the selected user
        context["user_profile"] = self.object.profile

        DEBUG_LOG and print(f' 🟩 recipe_app/views.py|context[favorite_recipes] is {context["user_profile"]}')

        #Favorite recipes/cooks for the selected user
        context["favorite_recipes"] = self.object.profile.favorite_recipes.all()
        context["favorite_cooks"] = self.object.profile.favorite_cooks.all()

        DEBUG_LOG and print(f' 💚 recipe_app/views.py|context[favorite_recipes] is {context["favorite_recipes"]}')
        DEBUG_LOG and print(f' 💚 recipe_app/views.py|context[favorite_cooks] is {context["favorite_cooks"]}')

        cook = self.object #The user whose profile we are viewing

        if not context["is_owner"]:
            context["cook_favorited"] = (self.request.user.profile.favorite_cooks.filter(pk=cook.pk).exists())
        else:
            context["cook_favorited"] = False

        return context


#Function-based view allowing toggling of favorite recipes/cooks per user profile
#🔒 PROTECTED VIEW
@login_required
def toggle_favorite(request):

    #Get the favorite type and id & user profile
    fav_type = request.POST.get("type")
    fav_id = request.POST.get("id")
    profile = request.user.profile

    #Values to be returned in a JSON object to update UI
    favorited = None
    count = None

    if fav_type == "recipe":

        recipe = get_object_or_404(Recipe, pk=fav_id)

        #Toggle fav recipe on/off & get new count
        if profile.favorite_recipes.filter(pk=recipe.pk).exists():
            profile.favorite_recipes.remove(recipe)
            favorited = False
        else:
            profile.favorite_recipes.add(recipe)
            favorited = True

        count = recipe.recipe_fans.count()

    elif fav_type == "cook":

        cook = get_object_or_404(User, username=fav_id)

        #Cannot favorite yourself (toggle should be hidden in template too)
        if cook == request.user:
            return JsonResponse({"error": "Cannot favorite yourself"}, status=400)

        #Toggle fav cook on/off & get new count
        if profile.favorite_cooks.filter(pk=cook.pk).exists():
            profile.favorite_cooks.remove(cook)
            favorited = False
        else:
            profile.favorite_cooks.add(cook)
            favorited = True

        count = cook.cook_fans.count()

    else:
        return JsonResponse({"error": "Invalid type"}, status=400)

    return JsonResponse({
        "favorited": favorited,
        "count": count
    })