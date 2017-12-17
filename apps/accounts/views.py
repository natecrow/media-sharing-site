from datetime import date

from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import login
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.urls import reverse

from ..images.models import Image
from .forms import ProfilePictureUploadForm, SignUpForm, EditProfileForm
from .models import Profile


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
            return redirect(reverse(
                'accounts:profile_page',
                kwargs={'username': request.user.username})
            )
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


@login_required(login_url='accounts:login')
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.profile.location = form.cleaned_data.get('location')
            user.profile.gender = form.cleaned_data.get('gender')
            user.save()
            return redirect(reverse(
                'accounts:profile_page',
                kwargs={'username': request.user.username})
            )
    else:
        form = EditProfileForm(
            instance=user,
            initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'location': user.profile.location,
                'gender': user.profile.gender
            }
        )
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required(login_url='accounts:login')
def change_profile_picture(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        Profile(user=request.user)

    if request.method == 'POST':
        form = ProfilePictureUploadForm(
            request.POST, files=request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(reverse(
                'accounts:profile_page',
                kwargs={'username': request.user.username})
            )
    else:
        form = ProfilePictureUploadForm(instance=profile)
    return render(request, 'accounts/upload_profile_picture.html',
                  {'form': form})


def profile_redirect(request):
    """
    Used for redirecting to a user's profile page when coming from a static url
    (such as the LOGIN_REDIRECT_URL)
    """
    return redirect(reverse(
        'accounts:profile_page',
        kwargs={'username': request.user.username}))


def profile_page(request, username):
    user = User.objects.get(username=username)
    if (user.profile.birth_date):
        age = calculate_age(user.profile.birth_date, date.today())
    else:
        age = '?'
    picture_list = Image.objects.filter(user=user).order_by('uploaded_date')

    paginator = Paginator(picture_list, 5)  # Number of pictures per page

    page = request.GET.get('page')
    try:
        pictures = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        pictures = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        pictures = paginator.page(paginator.num_pages)

    context = {'user': user, 'age': age, 'pictures': pictures}

    return render(request, 'accounts/profile_page.html', context)


def calculate_age(from_date, to_date):
    # interval should range from past to future
    assert(from_date < to_date)

    # subtract a year if the current month and day
    # has not reached the birth month and day
    return to_date.year - from_date.year - \
        ((to_date.month, to_date.day) < (from_date.month, from_date.day))
