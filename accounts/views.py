from django.shortcuts import render

def profile(request):
    return render(request, 'accounts/profile.html')

def logged_out(request):
    return render(request, 'logged_out.html')