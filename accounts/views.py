from django.shortcuts import render

def user_profile(request):
    return render(request, 'accounts/user_profile.html')

def logged_out(request):
    return render(request, 'accounts/logged_out.html')