from django.shortcuts import render, redirect
from .forms import SignupForm, ChangeUserData, UserProfileForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import UserProfile
from tuitions.models import Tuition,TuitionApplication
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode
from .tokens import EmailConfirmationTokenGenerator
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from .tokens import email_confirmation_token




def home(request):
    return render(request, 'home.html')

def signup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignupForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                UserProfile.objects.create(user=user, bio=form.cleaned_data['bio'],
                location=form.cleaned_data['location'],
                gender=form.cleaned_data['gender'],
                expertise=form.cleaned_data['expertise'],
                profile_img=form.cleaned_data['profile_img'])

                send_verification_email(request, user)

                login(request, user)

                return HttpResponse('Please confirm your email address to complete the registration')
        else:
            form = SignupForm()
        return render(request, 'signup.html', {'form': form})
    else:
        return redirect('profile')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                name = form.cleaned_data['username']
                userpass = form.cleaned_data['password']
                user = authenticate(username=name, password=userpass)
                if user is not None:
                    login(request, user)
                    return redirect('homepage')
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})
    else:
        return redirect('homepage')


@login_required
def profile(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = ChangeUserData(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')

    else:
        user_form = ChangeUserData(instance=user)
        profile_form = UserProfileForm(instance=user_profile)

    tuitions = Tuition.objects.filter(tuitionapplication__user=user, tuitionapplication__is_accepted=True)

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form, 'tuitions': tuitions})

def user_logout(request):
    logout(request)
    return redirect('login')


def pass_change(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('profile')
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request, 'passchange.html', {'form': form})
    else:
        return redirect('login')


def pass_change2(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = SetPasswordForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                return redirect('profile')
        else:
            form = SetPasswordForm(user=request.user)
        return render(request, 'passchange.html', {'form': form})
    else:
        return redirect('login')



def send_verification_email(request, user):
    token = EmailConfirmationTokenGenerator().make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_url = f"{request.build_absolute_uri('/')}verify-email/{uid}/{token}/"

    subject = 'Verify Your Email'
    message = render_to_string('email_verification_email.html', {'verification_url': verification_url})
    from_email = 'soaibahmed8021@gmail.com'
    to_email = user.email

    send_mail(subject, message, from_email, [to_email])

@login_required
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and email_confirmation_token.check_token(user, token):
        user.userprofile.email_confirmed = True
        user.userprofile.save()
        return render(request, 'email_verified.html') 
    else:
        return render(request, 'email_verification_failed.html')