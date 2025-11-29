from django.shortcuts import render, redirect

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
                return redirect('recipes:list')

        #If we reach here, form was invalid OR user was invalid
        non_field_errors = form.non_field_errors()
        if non_field_errors:
            error_message = non_field_errors[0]
            print(' ⚠️ Authentication Error:',error_message)

    #Prep data to send from view to template
    context = {
      'form':form,
      'error_message':error_message
    }

    #Load login page with this context
    return render(request, 'auth/login.html', context)


#Logout FBV
def logout_view(request):
    logout(request)
    return render(request, 'auth/logout.html')