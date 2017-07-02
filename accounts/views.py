from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.shortcuts import redirect, render

from .forms import SignUpForm


@login_required(login_url='accounts:login')
def profile(request):
    return render(request, 'accounts/profile.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # load profile instance created by the signal
            user.refresh_from_db()
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.profile.gender = form.cleaned_data.get('gender')
            user.profile.location = form.cleaned_data.get('location')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
