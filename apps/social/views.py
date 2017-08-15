from datetime import date

from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render


def profiles_directory(request):
    user_list = User.objects.all()

    paginator = Paginator(user_list, 20)  # Number of profiles per page

    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        users = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        users = paginator.page(paginator.num_pages)

    context = {'users': users}

    return render(request, 'social/profiles_directory.html', context)


def profile_page(request, username):
    user = User.objects.get(username=username)
    age = calculate_age(user.profile.birth_date, date.today())

    context = {'user': user, 'age': age}

    return render(request, 'social/profile_page.html', context)


def calculate_age(from_date, to_date):
    # interval should range from past to future
    assert(from_date < to_date)

    # subtract a year if the current month and day
    # has not reached the birth month and day
    return to_date.year - from_date.year - \
        ((to_date.month, to_date.day) < (from_date.month, from_date.day))
