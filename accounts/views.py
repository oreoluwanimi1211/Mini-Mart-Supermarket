from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import CustomUser
from django.contrib import messages, auth
from django.contrib.auth import login, logout




def registeruser(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            if not username:
                username = email.split('@')[0]
            user = CustomUser.objects.create_user(
            name=name,
            username=username,
            phone_number=phone_number,
            email=email,
            password=password
            )
            print(user)
            user.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {
        'form':form,
    }
    return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'you are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credential')
            return redirect('login')
    return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')