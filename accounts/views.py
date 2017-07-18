from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import SignUpForm, UploadProfilePictureForm
from .models import Profile


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


def upload_file(request):

    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        Profile(user=request.user)

    if request.method == 'POST':
        form = UploadProfilePictureForm(
            request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        form = UploadProfilePictureForm(instance=profile)
    return render(request, 'accounts/upload_profile_picture.html',
                  {'form': form})
