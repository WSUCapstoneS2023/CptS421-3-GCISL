from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.views.generic import TemplateView, CreateView
import datetime
from .forms import RegistrationForm, LoginAuthForm
from .models import GCISLUser

# Create your views here.
# home view
# Note to Ali, to access user data, call {{ user.(datafield) }} - data fields could be the first name or other attributes
def landing_view(request):
    if request.user.is_authenticated:
        return render(request, 'landing-logged.html', {'user': request.user})
    else:
        return render(request, 'landing.html')

# Get Involved
def getinvolved_view(request):
    if request.user.is_authenticated:
        return render(request, 'getinvolved-logged.html', {'user': request.user})
    else:
        return render(request, 'getinvolved.html')

# Survey
def survey_view(request):
    return render(request, 'survey.html')

# Contact
def contact_view(request):
    if request.user.is_authenticated:
        return render(request, 'contact-logged.html', {'user': request.user})
    else:
        return render(request, 'contact.html')

# About
def about_view(request):
    if request.user.is_authenticated:
        return render(request, 'about-logged.html', {'user': request.user})
    else:
        return render(request, 'about.html')

# Register
def registration_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()     
        return redirect('/login')
    else:
        form = RegistrationForm()
        return render(request, 'registration.html', {'rform': form})


# Login
# citation: (documentation for user login that I followed) https://docs.djangoproject.com/en/4.1/topics/auth/default/
def login_view(request):
    if request.method == 'POST':
        form = LoginAuthForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_Resident:
                    # these will be different in future based off status
                    return redirect('landing')
                if user.is_Faculty:
                    # these will be different in future based off status
                    return redirect('landing')
            else:
                messages.error(request,'Username or password not correct!')
                return redirect('/login')
        else:
            messages.error(request,'Please fill in all fields!')
            return redirect('/login')
    else:
        form = LoginAuthForm()
        return render(request, 'login.html', {'lform':form})
    
def logout_view(request):
    logout(request)
    return redirect('landing')
