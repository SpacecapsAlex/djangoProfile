from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect

from usermanager.models import Profile


def index(request):
    return render(request, 'usermanager/index.html')


def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        about = request.POST['about']

        user = User.objects.create_user(username=username, password=password, email=email)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        profile = Profile(user=user, about=about)
        profile.save()

        return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, 'usermanager/register.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'usermanager/login.html')
    else:
        return render(request, 'usermanager/login.html')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def profile_user(request):
    if request.user.is_authenticated:
        user = request.user
        profile = Profile.objects.get(user=user)

        data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'about': profile.about
        }

        return render(request, 'usermanager/profile.html', {'data': data})
    else:
        return HttpResponseRedirect(reverse('login'))
