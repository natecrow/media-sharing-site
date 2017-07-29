from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render

from apps.accounts.models import Profile


def profiles_directory(request):
    profile_list = Profile.objects.all()

    paginator = Paginator(profile_list, 25)  # Show 25 profiles per page

    page = request.GET.get('page')
    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        profiles = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        profiles = paginator.page(paginator.num_pages)

    context = {'profiles': profiles}

    return render(request, 'social/profiles_directory.html', context)
