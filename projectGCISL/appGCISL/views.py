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
def landing_view(request):
    return render(request, 'landing.html')

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
            user = GCISLUser.objects.get(username=username)
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
        form = LoginAuthForm()
        return render(request, 'login.html', {'lform':form})
