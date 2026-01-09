from django.shortcuts import render, redirect

from django.views.generic import UpdateView, DeleteView #To allow editing on a User

from django.contrib.auth.models import User
from django.views.generic import DetailView #To display user's recipes in profile view
from recipes.models import Recipe
from django.http import Http404

#Protected view imports:
from django.contrib.auth.mixins import LoginRequiredMixin   #To protect class-based views
from django.contrib.auth.decorators import login_required   #To protect function-based views

#Authentication imports:
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .forms import CustomUserCreationForm

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
        
        #Add hide value for menubar
        #context["hide_profile_menu"] = True

        return context