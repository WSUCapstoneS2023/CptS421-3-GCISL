from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.views.generic import TemplateView, CreateView
import datetime
from .forms import RegistrationForm, LoginForm


# Create your views here.
# home view
def landing_view(request):
    return render(request, 'landing.html')

# Register
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # save to the db
            form.save()
            # redirect the user to login (appname is temporary until merge)
            return redirect('landing')
    else:
        form = RegistrationForm()
        return render(request, 'register.html', {'rform': form})


# Login
# citation: (documentation for user login that I followed) https://docs.djangoproject.com/en/4.1/topics/auth/default/
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_Resident():
                # these will be different in future based off status
                return redirect('landing')
            if user.is_Faculty():
                # these will be different in future based off status
                return redirect('landing')
        else:
            messages.error(request,'Username or password not incorrect!')
            return redirect('login')
    else:
        return render(request, 'login.html')
