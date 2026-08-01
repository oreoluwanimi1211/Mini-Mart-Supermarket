from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from .models import CustomUser
from django.contrib import messages, auth
from django.contrib.auth import login, logout
from .utils import send_verification_email, send_notification
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage






def registeruser(request):
    if request.user.is_authenticated:
        messages.warning(request, 'you are already logged in!')
        return redirect('dashboard')
    elif request.method == 'POST':
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

            #send email
            mail_subject = 'please activate your account'
            email_template = 'accounts/emails/account_verification_email.html'
            send_verification_email(request, user, mail_subject, email_template)
            messages.success(request, 'your account has been register succesfully!')


            return redirect('login')
        else:
            print('invalid form')
            print(form.errors)
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

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'congratulations! Your account is activated')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']

        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email__exact=email)

            # send reset password email
            mail_subject = 'Reset Your Password'
            email_template = 'accounts/emails/reset_password_email.html'
            send_verification_email(request, user, mail_subject, email_template)

            messages.success(request, 'password reset link has been sent to your email address!')
            return redirect('login')
        else:
            messages.error(request, 'Accounts does not exist')
            return redirect('forgotpassword')
    return render(request, 'accounts/forgotpassword.html')


def resetpasswordvalidate(request, uidb64, token):
    # Validate the user by decoding the and user pk
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'please reset your password')
        return redirect('resetpassword')
    else:
        messages.error(request, 'this link has been expired!')
        return redirect('forgotpassword')

def resetpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = CustomUser.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'password does not match')
            return redirect('resetpassword')
    return render(request, 'accounts/resetpassword.html')