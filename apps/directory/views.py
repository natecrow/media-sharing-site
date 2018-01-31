from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render


def profiles_directory(request):
    # order users by latest to earlier joined
    user_list = User.objects.order_by('-date_joined')

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

    return render(request, 'directory/profiles_directory.html', context)
