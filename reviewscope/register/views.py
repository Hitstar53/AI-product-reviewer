from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.models import User

# Create your views here.
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')
            return render(request, 'authenticate/login.html')
    else:
        return render(request, 'authenticate/login.html')

def register_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == password2:
            # check if username already exists
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                return render(request, 'authenticate/register.html')
            else:
                user = User.objects.create_user(email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Password not matching')
            return render(request, 'authenticate/register.html')
    else:
        return render(request, 'authenticate/register.html')