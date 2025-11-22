from django.shortcuts import render, redirect

#Authentication imports:
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

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
                print(f'✅Login complete for [{user}]')
                return redirect('recipes:list')
            else:
                error_message = form.errors
                print('⚠️Authentication Error:',error_message)

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
    print('✅Logout complete')
    return render(request, 'auth/logout.html')