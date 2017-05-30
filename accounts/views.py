from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm


@login_required(login_url="login")
def profile(request):
    return render(request, 'accounts/profile.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
